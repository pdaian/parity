(function() {var implementors = {};
implementors["ethcore"] = ["impl CheckedAdd for BigUint","impl CheckedAdd for BigInt",];implementors["ethsync"] = ["impl CheckedAdd for BigUint","impl CheckedAdd for BigInt",];implementors["ethcore_rpc"] = ["impl CheckedAdd for BigUint","impl CheckedAdd for BigInt",];implementors["ethcore_dapps"] = ["impl CheckedAdd for BigUint","impl CheckedAdd for BigInt",];implementors["parity"] = ["impl CheckedAdd for BigUint","impl CheckedAdd for BigInt",];

            if (window.register_implementors) {
                window.register_implementors(implementors);
            } else {
                window.pending_implementors = implementors;
            }
        
})()
