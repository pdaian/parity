(function() {var implementors = {};
implementors["ethcore"] = ["impl CheckedDiv for BigUint","impl CheckedDiv for BigInt",];implementors["ethsync"] = ["impl CheckedDiv for BigUint","impl CheckedDiv for BigInt",];implementors["ethcore_rpc"] = ["impl CheckedDiv for BigUint","impl CheckedDiv for BigInt",];implementors["ethcore_dapps"] = ["impl CheckedDiv for BigUint","impl CheckedDiv for BigInt",];implementors["parity"] = ["impl CheckedDiv for BigUint","impl CheckedDiv for BigInt",];

            if (window.register_implementors) {
                window.register_implementors(implementors);
            } else {
                window.pending_implementors = implementors;
            }
        
})()
