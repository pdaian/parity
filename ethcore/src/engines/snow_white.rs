// Copyright 2015, 2016 Ethcore (UK) Ltd. & Philip Daian
// This file is part of Parity.

// Parity is free software: you can redistribute it and/or modify
// it under the terms of the GNU General Public License as published by
// the Free Software Foundation, either version 3 of the License, or
// (at your option) any later version.

// Parity is distributed in the hope that it will be useful,
// but WITHOUT ANY WARRANTY; without even the implied warranty of
// MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
// GNU General Public License for more details.

// You should have received a copy of the GNU General Public License
// along with Parity.  If not, see <http://www.gnu.org/licenses/>.

//! A blockchain engine that supports the SnowWhite PoS protocol described in https://eprint.iacr.org/2016/919

extern crate time;
extern crate crypto;

use ethkey::{recover, public_to_address};
use account_provider::AccountProvider;
use block::*;
use builtin::Builtin;
use spec::CommonParams;
use engines::Engine;
use env_info::EnvInfo;
use error::{BlockError, Error};
use evm::Schedule;
use ethjson;
use header::Header;
use transaction::SignedTransaction;
use std::process;
use ethereum::ethash::Ethash;
use self::crypto::digest::Digest;
use self::crypto::sha3::Sha3;

use util::*;

/// `SnowWhite` params.
#[derive(Debug, PartialEq)]
pub struct SnowWhiteParams {
	/// Gas limit divisor.
	pub gas_limit_bound_divisor: U256,
	/// Block duration.
	pub duration_limit: u64,
	/// Valid signatories.
	pub authorities: HashSet<Address>,
	// Permissioned operation mode
	permissioned: bool,
	// Time interval, in seconds
	time_interval: u64,
	// Kappa (max allowable clock drift + network delay) TODO doublecheck proof spec, simulate allowable parameters
	kappa: i64,
}

impl From<ethjson::spec::SnowWhiteParams> for SnowWhiteParams {
	fn from(p: ethjson::spec::SnowWhiteParams) -> Self {
		SnowWhiteParams {
			gas_limit_bound_divisor: p.gas_limit_bound_divisor.into(),
			duration_limit: p.duration_limit.into(),
			authorities: p.authorities.into_iter().map(Into::into).collect::<HashSet<_>>(),
			permissioned: true,
			time_interval : 5,
			kappa : 60,
		}
	}
}

/// Engine using `SnowWhite` proof-of-stake consensus algorithm, suitable for Ethereum
/// mainnet chains in the Olympic, Frontier and Homestead eras.
pub struct SnowWhite {
	params: CommonParams,
	our_params: SnowWhiteParams,
	builtins: BTreeMap<Address, Builtin>,
}

impl SnowWhite {
	/// Create a new instance of SnowWhite engine
	pub fn new(params: CommonParams, our_params: SnowWhiteParams, builtins: BTreeMap<Address, Builtin>) -> Self {
		SnowWhite {
			params: params,
			our_params: our_params,
			builtins: builtins,
		}
	}
}

impl Engine for SnowWhite {
	fn name(&self) -> &str { "SnowWhite" }
	fn version(&self) -> SemanticVersion { SemanticVersion::new(1, 0, 0) }
	// One field - the signature
	fn seal_fields(&self) -> usize { 1 }

	fn params(&self) -> &CommonParams { &self.params }
	fn builtins(&self) -> &BTreeMap<Address, Builtin> { &self.builtins }

	/// Additional engine-specific information for the user/developer concerning `header`.
	fn extra_info(&self, _header: &Header) -> BTreeMap<String, String> { map!["signature".to_owned() => "todo".to_owned()] }

	fn schedule(&self, _env_info: &EnvInfo) -> Schedule {
		Schedule::new_homestead()
	}

	fn populate_from_parent(&self, header: &mut Header, parent: &Header, gas_floor_target: U256, _gas_ceil_target: U256) {
		// Adjust the timestamp to reflect 1 timestep every 5s
		let current_timestamp = header.timestamp().clone();
		let adjusted_timestamp = current_timestamp - (current_timestamp % self.our_params.time_interval); 
		header.set_timestamp(adjusted_timestamp);

		// Get expected difficulty and populate header
		let new_difficulty = self.get_difficulty_from_parent(header, parent);
		header.set_difficulty(new_difficulty.clone());

		// Standard gas adjustment in permissionless setting, otherwise stick with hardcoded parameter
		header.set_gas_limit({
			if !self.our_params.permissioned {
				let gas_limit = parent.gas_limit().clone();
				let bound_divisor = self.our_params.gas_limit_bound_divisor;
				if gas_limit < gas_floor_target {
					min(gas_floor_target, gas_limit + gas_limit / bound_divisor - 1.into())
				} else {
					max(gas_floor_target, gas_limit - gas_limit / bound_divisor + 1.into())
				}
			}
			else {
				parent.gas_limit().clone()
			}
		});

		info!("[{}] Created new block from parent @ time {}.  Difficulty: {}, Timestamp: {}, #{}", time::get_time().sec, parent.timestamp(), header.difficulty(), header.timestamp(), header.number());
	}

	fn on_close_block(&self, _block: &mut ExecutedBlock) {}

	fn is_sealer(&self, author: &Address) -> Option<bool> {
		Some(self.our_params.authorities.contains(author))
	}

	/// Attempt to seal the block internally.
	///
	/// This operation is synchronous and may (quite reasonably) not be available, in which `false` will
	/// be returned.
	fn generate_seal(&self, block: &ExecutedBlock, accounts: Option<&AccountProvider>) -> Option<Vec<Bytes>> {
		info!("Attempting to mine a block...");
		trace!(target: "snowwhite", "generate_seal: Attempting to seal");
		if let Some(ap) = accounts {
			let header = block.header();
			let message = header.bare_hash();
			// account should be pernamently unlocked, otherwise sealing will fail
			if let Ok(signature) = ap.sign(*block.header().author(), None, message) {
				return Some(vec![::rlp::encode(&(&*signature as &[u8])).to_vec()]);
			} else {
				trace!(target: "snowwhite", "generate_seal: FAIL: accounts secret key unavailable");
			}
		} else {
			trace!(target: "snowwhite", "generate_seal: FAIL: accounts not provided");
		}
		None
	}

	fn verify_block_basic(&self, header: &Header, _block: Option<&[u8]>) -> result::Result<(), Error> {
		// check the seal fields.
		// TODO: pull this out into common code.
		if header.seal().len() != self.seal_fields() {
			return Err(From::from(BlockError::InvalidSealArity(
				Mismatch { expected: self.seal_fields(), found: header.seal().len() }
			)));
		}
		Ok(())
	}

	fn verify_block_unordered(&self, header: &Header, _block: Option<&[u8]>) -> result::Result<(), Error> {
		use rlp::{UntrustedRlp, View};

		// check the signature is legit.
		let sig = try!(UntrustedRlp::new(&header.seal()[0]).as_val::<H520>());
		let signer = public_to_address(&try!(recover(&sig.into(), &header.bare_hash())));
		if !self.our_params.authorities.contains(&signer) {
			return try!(Err(BlockError::InvalidSeal));
		}

		let timestamp = header.timestamp().clone();
		// Make sure timestamp represents a valid seal
		if timestamp % self.our_params.time_interval != 0 {
			return try!(Err(BlockError::InvalidSeal));
		}

		Ok(())
	}

	fn verify_block_family(&self, header: &Header, parent: &Header, _block: Option<&[u8]>) -> result::Result<(), Error> {
		// we should not calculate difficulty for genesis blocks
		if header.number() == 0 {
			return Err(From::from(BlockError::RidiculousNumber(OutOfBounds { min: Some(1), max: None, found: header.number() })));
		}

		// Check that, if we are syncd with latest head, block time remains within parameters
		// TODO : What is supposed to happen on rejection here?  Queueing, waiting, discard?  Analyze potential for accidental chain fork.

		let timestamp = header.timestamp().clone();
		let parent_timestamp = parent.timestamp().clone();

		// Make sure block is mined correctly off parent (not in same time interval) TODO check protocol interactions w.r.t. time interval
                if timestamp == parent_timestamp {
                        return try!(Err(BlockError::InvalidSeal));
                }

		// Make sure that the timestamp is within the kappa bound TODO unit test this
		let signed_curr_time = time::get_time().sec as i64;
		let signed_parent_time = parent_timestamp as i64;
		let signed_header_time = timestamp as i64;

		if signed_header_time < 0 {
			// handle potential for overflow into negative values (parent was already verified)
                        return try!(Err(BlockError::InvalidSeal));
		}
		if (signed_curr_time - signed_parent_time).abs() < 30 { // TODO bootstrap checkpoints
			// We only care about kappa if we're syncd to head; check this by checking parent block timestamp TODO proof interaction here?
			if (signed_curr_time - signed_header_time).abs() > self.our_params.kappa {
				process::exit(68);
				return try!(Err(BlockError::InvalidSeal));
			}
		}

		// Check difficulty is correct given the two timestamps.
		let appropriate_difficulty = self.get_difficulty_from_parent(header, parent);
		if (header.difficulty().clone()) != appropriate_difficulty {
			return Err(From::from(BlockError::InvalidDifficulty(Mismatch { expected: appropriate_difficulty, found: *header.difficulty() })))
		}
		let gas_limit_divisor = self.our_params.gas_limit_bound_divisor;
		let min_gas = parent.gas_limit().clone() - parent.gas_limit().clone() / gas_limit_divisor;
		let max_gas = parent.gas_limit().clone() + parent.gas_limit().clone() / gas_limit_divisor;
		if header.gas_limit() <= &min_gas || header.gas_limit() >= &max_gas {
			return Err(From::from(BlockError::InvalidGasLimit(OutOfBounds { min: Some(min_gas), max: Some(max_gas), found: header.gas_limit().clone() })));
		}
		if self.our_params.permissioned & (header.gas_limit() != parent.gas_limit()) {
			// Enforce no adjustment on gas limit (to prevent gas-based attacks due to lack of gas based rules in block generation)
			return Err(From::from(BlockError::InvalidGasLimit(OutOfBounds { min: Some(parent.gas_limit().clone()), max: Some(parent.gas_limit().clone()), found: header.gas_limit().clone() })));			
		}

		// PoW check (similar to ETHHash, using SHA3 rather than memory hard function, modified as described in paper)
		// First we SHA Unix Time || pub key || h0
		let time_string = &header.timestamp().clone().to_string(); // TODO fix reliance on consistency of rust string method
		let signer_string = &header.author().clone().to_string();
		let h0_string = &(if self.our_params.permissioned { 0.to_string() } else { 1.to_string() });  // TODO h0 gather to generalize to permissionless
		let mut hasher = Sha3::sha3_256();
		hasher.input_str(time_string);
		hasher.input_str(signer_string);
		hasher.input_str(h0_string);
		let hex = hasher.result_str();
	        let difficulty = Ethash::boundary_to_difficulty(&H256::from_str(&hex).unwrap()) * U256::from(100000); // convert result to difficulty

                if &difficulty < header.difficulty() { // make sure header has validated correctly
                        return Err(From::from(BlockError::InvalidProofOfWork(OutOfBounds { min: Some(header.difficulty().clone()), max: None, found: difficulty })));
                }
		Ok(())
	}

	fn verify_transaction_basic(&self, t: &SignedTransaction, _header: &Header) -> result::Result<(), Error> {
		// This is the same as authority chain 
		try!(t.check_low_s());
		Ok(())
	}

	fn verify_transaction(&self, t: &SignedTransaction, _header: &Header) -> Result<(), Error> {
		// This is the same as authority chain 
		t.sender().map(|_|()) // Perform EC recovery and cache sender
	}
}

impl Header {
	/// Get the none field of the header.
	pub fn signature(&self) -> H520 {
		// This is the same as authority chain
		::rlp::decode(&self.seal()[0])
	}
}

#[cfg(test)]
mod tests {
	use util::*;
	use block::*;
	use util::trie::TrieSpec;
	use env_info::EnvInfo;
	use error::{BlockError, Error};
	use tests::helpers::*;
	use account_provider::AccountProvider;
	use header::Header;
	use spec::Spec;

	/// Create a new test chain spec with `SnowWhite` consensus engine.
	fn new_test_authority() -> Spec {
		let bytes: &[u8] = include_bytes!("../../res/test_swhite.json");
		Spec::load(bytes).expect("invalid chain spec")
	}

	#[test]
	fn has_valid_metadata() {
		let engine = new_test_authority().engine;
		assert!(!engine.name().is_empty());
		assert!(engine.version().major >= 1);
	}

	#[test]
	fn can_return_schedule() {
		let engine = new_test_authority().engine;
		let schedule = engine.schedule(&EnvInfo {
			number: 10000000,
			author: 0.into(),
			timestamp: 0,
			difficulty: 0.into(),
			last_hashes: Arc::new(vec![]),
			gas_used: 0.into(),
			gas_limit: 0.into(),
		});

		assert!(schedule.stack_limit > 0);
	}

	#[test]
	fn can_do_seal_verification_fail() {
		let engine = new_test_authority().engine;
		let header: Header = Header::default();

		let verify_result = engine.verify_block_basic(&header, None);

		match verify_result {
			Err(Error::Block(BlockError::InvalidSealArity(_))) => {},
			Err(_) => { panic!("should be block seal-arity mismatch error (got {:?})", verify_result); },
			_ => { panic!("Should be error, got Ok"); },
		}
	}

	#[test]
	fn can_do_signature_verification_fail() {
		let engine = new_test_authority().engine;
		let mut header: Header = Header::default();
		header.set_seal(vec![::rlp::encode(&H520::default()).to_vec()]);

		let verify_result = engine.verify_block_unordered(&header, None);
		assert!(verify_result.is_err());
	}

	#[test]
	fn can_generate_seal() {
		let tap = AccountProvider::transient_provider();
		let addr = tap.insert_account("".sha3(), "").unwrap();
		tap.unlock_account_permanently(addr, "".into()).unwrap();

		let spec = new_test_authority();
		let engine = &*spec.engine;
		let genesis_header = spec.genesis_header();
		let mut db_result = get_temp_state_db();
		let mut db = db_result.take();
                spec.ensure_db_good(&mut db, &TrieFactory::new(TrieSpec::Secure)).unwrap();
		let last_hashes = Arc::new(vec![genesis_header.hash()]);
		let b = OpenBlock::new(engine, Default::default(), false, db, &genesis_header, last_hashes, addr, (3141562.into(), 31415620.into()), vec![]).unwrap();
		let b = b.close_and_lock();
		let seal = engine.generate_seal(b.block(), Some(&tap)).unwrap();
		assert!(b.try_seal(engine, seal).is_ok());
	}

	#[test]
	fn seals_internally() {
		let tap = AccountProvider::transient_provider();
		let authority = tap.insert_account("".sha3(), "").unwrap();

		let engine = new_test_authority().engine;
		assert!(!engine.is_sealer(&Address::default()).unwrap());
		assert!(engine.is_sealer(&authority).unwrap());
	}
}
