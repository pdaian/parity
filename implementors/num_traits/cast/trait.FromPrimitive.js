(function() {var implementors = {};
implementors["ethcore"] = ["impl FromPrimitive for BigUint","impl FromPrimitive for BigInt",];implementors["ethsync"] = ["impl FromPrimitive for BigUint","impl FromPrimitive for BigInt",];implementors["ethcore_rpc"] = ["impl FromPrimitive for BigUint","impl FromPrimitive for BigInt",];implementors["ethcore_dapps"] = ["impl FromPrimitive for BigUint","impl FromPrimitive for BigInt",];implementors["parity"] = ["impl FromPrimitive for BigUint","impl FromPrimitive for BigInt",];

            if (window.register_implementors) {
                window.register_implementors(implementors);
            } else {
                window.pending_implementors = implementors;
            }
        
})()
