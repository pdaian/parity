(function() {var implementors = {};
implementors["ethcore_dapps"] = ["impl WebApp for App",];implementors["parity"] = ["impl WebApp for App",];

            if (window.register_implementors) {
                window.register_implementors(implementors);
            } else {
                window.pending_implementors = implementors;
            }
        
})()
