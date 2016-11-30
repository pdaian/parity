(function() {var implementors = {};
implementors["ethsync"] = [];implementors["ethcore_rpc"] = [];implementors["ethcore_dapps"] = [];implementors["parity"] = [];

            if (window.register_implementors) {
                window.register_implementors(implementors);
            } else {
                window.pending_implementors = implementors;
            }
        
})()
