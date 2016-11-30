(function() {var implementors = {};
implementors["ethcore"] = ["impl Integer for BigUint","impl Integer for BigInt",];implementors["ethsync"] = ["impl Integer for BigUint","impl Integer for BigInt",];implementors["ethcore_rpc"] = ["impl Integer for BigUint","impl Integer for BigInt",];implementors["ethcore_dapps"] = ["impl Integer for BigUint","impl Integer for BigInt",];implementors["parity"] = ["impl Integer for BigUint","impl Integer for BigInt",];

            if (window.register_implementors) {
                window.register_implementors(implementors);
            } else {
                window.pending_implementors = implementors;
            }
        
})()
