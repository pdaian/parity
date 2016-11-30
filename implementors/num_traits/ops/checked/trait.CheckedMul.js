(function() {var implementors = {};
implementors["ethcore"] = ["impl CheckedMul for BigUint","impl CheckedMul for BigInt",];implementors["ethsync"] = ["impl CheckedMul for BigUint","impl CheckedMul for BigInt",];implementors["ethcore_rpc"] = ["impl CheckedMul for BigUint","impl CheckedMul for BigInt",];implementors["ethcore_dapps"] = ["impl CheckedMul for BigUint","impl CheckedMul for BigInt",];implementors["parity"] = ["impl CheckedMul for BigUint","impl CheckedMul for BigInt",];

            if (window.register_implementors) {
                window.register_implementors(implementors);
            } else {
                window.pending_implementors = implementors;
            }
        
})()
