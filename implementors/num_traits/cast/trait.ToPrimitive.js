(function() {var implementors = {};
implementors["ethcore"] = ["impl ToPrimitive for BigUint","impl ToPrimitive for BigInt",];implementors["ethsync"] = ["impl ToPrimitive for BigUint","impl ToPrimitive for BigInt",];implementors["ethcore_rpc"] = ["impl ToPrimitive for BigUint","impl ToPrimitive for BigInt",];implementors["ethcore_dapps"] = ["impl ToPrimitive for BigUint","impl ToPrimitive for BigInt",];implementors["parity"] = ["impl ToPrimitive for BigUint","impl ToPrimitive for BigInt",];

            if (window.register_implementors) {
                window.register_implementors(implementors);
            } else {
                window.pending_implementors = implementors;
            }
        
})()
