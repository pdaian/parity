(function() {var implementors = {};
implementors["ethcore"] = ["impl&lt;T&gt; Num for Ratio&lt;T&gt; <span class='where'>where T: <a class='trait' href='https://doc.rust-lang.org/nightly/core/clone/trait.Clone.html' title='core::clone::Clone'>Clone</a> + Integer</span>","impl Num for BigUint","impl Num for BigInt",];implementors["ethsync"] = ["impl&lt;T&gt; Num for Ratio&lt;T&gt; <span class='where'>where T: <a class='trait' href='https://doc.rust-lang.org/nightly/core/clone/trait.Clone.html' title='core::clone::Clone'>Clone</a> + Integer</span>","impl Num for BigUint","impl Num for BigInt",];implementors["ethcore_rpc"] = ["impl Num for BigUint","impl Num for BigInt","impl&lt;T&gt; Num for Ratio&lt;T&gt; <span class='where'>where T: <a class='trait' href='https://doc.rust-lang.org/nightly/core/clone/trait.Clone.html' title='core::clone::Clone'>Clone</a> + Integer</span>",];implementors["ethcore_dapps"] = ["impl Num for BigUint","impl Num for BigInt","impl&lt;T&gt; Num for Ratio&lt;T&gt; <span class='where'>where T: <a class='trait' href='https://doc.rust-lang.org/nightly/core/clone/trait.Clone.html' title='core::clone::Clone'>Clone</a> + Integer</span>",];implementors["parity"] = ["impl&lt;T&gt; Num for Ratio&lt;T&gt; <span class='where'>where T: <a class='trait' href='https://doc.rust-lang.org/nightly/core/clone/trait.Clone.html' title='core::clone::Clone'>Clone</a> + Integer</span>","impl Num for BigUint","impl Num for BigInt",];

            if (window.register_implementors) {
                window.register_implementors(implementors);
            } else {
                window.pending_implementors = implementors;
            }
        
})()
