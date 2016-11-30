(function() {var implementors = {};
implementors["ethcore"] = ["impl Unsigned for BigUint",];implementors["ethsync"] = ["impl Unsigned for BigUint",];implementors["ethcore_rpc"] = ["impl Unsigned for BigUint",];implementors["ethcore_dapps"] = ["impl Unsigned for BigUint",];implementors["parity"] = ["impl Unsigned for BigUint",];

            if (window.register_implementors) {
                window.register_implementors(implementors);
            } else {
                window.pending_implementors = implementors;
            }
        
})()
