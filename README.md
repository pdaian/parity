Snow White
----------

Snow White is the first provably secure proof of stake algorithm implemented on top of Ethereum, currently for the *permissioned* setting
(fixed set of participants known a priori).  We plan on generalizing Snow White to the permissionless setting for USENIX Security '17.

Snow White relies on the "honest participant/coin majority" assumption.  There is some debate on the vulnerability of this model to attack
in the permissionless context: https://blog.ethereum.org/2016/12/06/history-casper-chapter-1/ and more research is needed before deploying
a live financial system with this algorithm.

Code Changes / Diff Description
-------------------------------

Our system is based off of Parity (github.com/ethcore/parity), the fastest and most robust Ethereum blockchain implementation available.

A full diff of our system to Parity is available here: https://github.com/ethcore/parity/compare/master...pdaian:snowwhite

The "core changes" (changes to mining algorithms, consensus, and their tests) are approximately 600-800 lines of code.

The "auxilliary changes" (including management scripts, experiments, etc.) are approximately 1200 lines of code.

The full diff is larger, as it includes "explorer", a modified version of EtherParty (see the explorer section below) that 
*we modified but did not write*.  

The key changes are as follows (in order of importance):

- ethcore/src/engines/snow_white.rs : The Core Snow White algorithm.  Some code/tests borrowed from engines/basic_authority.rs; in these cases,
   a comment is included indicating that the code is "the same as BasicAuthority".  These are the core consensus algorithm changes, and
   represent a robust core of extensively tested (through deployment clusters) code.
-  ethcore/src/engines/mod.rs : The generic Ethcore engines framework.  Here, we reintroduce the difficulty adjustment algorithm used in
   Ethereum, which previously was not required for permissioned engines.
- pyrpc : this folder contains an interface for interacting with SnowWhite through RPC, and several useful scripts described later in this doc
- automated_install.py : auto install utility described later in this document.
- graphs : selection of scripts used in data collection and graph generation
- skeleton : example configuration files described later in this document.

There are several smaller changes to infrastructure that are procedural / uninteresting.

Please don't hestitate to contact me about any questions or confusions regarding either the diff provided or its description.

Prerequisites
-------------

To build and run SnowWhite, you must:

- Install git, make, gcc, and g++.  On Ubuntu, you can ``sudo apt-get update --fix-missing`` then
    ``sudo apt-get install git make build-essential g++`` to satsify these 
    dependencies. 
- Install stable Rust through rustup (https://www.rustup.rs/).  On Linux, simply run ``curl https://sh.rustup.rs -sSf | sh -s -- -y`` 
    in the command line.
- Restart your shell to complete the rustup install, or run ``source ~/.cargo/env``


Running the System - One Node
-----------------------------

For isolation we recommend running and building SnowWhite in its own account, as several files/directories inside the home folder are required.

To build Snow White on a single node (we call this first node the "anchor node" in a multiple node system):

- If you are not installing from tarball, clone snowwhite.  ``cd ~ && git clone https://github.com/pdaian/parity && cd parity && git checkout snowwhite``
- Build snowwhite.  Run ``cargo build --release`` in the ``parity`` folder generated from either this tarball or the git clone above.
- Copy the "skeleton files", including chain configuration.  From the ``parity/skeleton`` folder: ``cp -a . /home/[your user]``
    (cat ~/.parity/address to make sure this copied as well)
- Run Parity using ``[path to parity folder] /target/release/parity --jsonrpc-apis "parity_set,parity,eth,parity_accounts,personal" -l info --rpccorsdomain "http://0.0.0.0:8000" --jsonrpc-interface all --jsonrpc-hosts="all" --max-peers 200``
    (replace 0.0.0.0 in the RPC CORS domain with the public IP of your machine if you wish to use the block explorer feature (see below))

You will know you are running SnowWhite correctly when you see something like this in the console:
````
2016-12-09 19:42:39 UTC Operating mode: active
2016-12-09 19:42:39 UTC Configured for ProofOfStakeTest using SnowWhite engine
2016-12-09 19:42:44 UTC Public node URL: enode://790...
````

You can also run SnowWhite as a daemon.  Simply add ``daemon /tmp/pid`` after the path to the Parity binary.

To run with extended debug log information, change ``-l info`` to ``-l debug`` in the above command.  This is verbose and not
generally recommended unless debugging network issues.

To stop SnowWhite/Parity, simply run ``killall -9 parity``.

To compile in debug mode (with debug symbols, stacktraces, but lower performance) run ``cargo build --debug".  Then, replace any commands
in this document or related scripts that use ``target/release`` with ``target/debug``.  This is not recommended due to a far lower level
of performance (~20x slower in our testing).

To start generating transactions and mining blocks on a node, run ``python parity.py`` in the ``pyrpc`` subfolder.
To mine in the background, the command would look something like:
``nohup python [path to]/parity/pyrpc/parity.py </dev/null > /dev/null 2>&1 &``
To mine with multiple processes, you may run the command multiple times.

You should see output that looks like:
````
{u'jsonrpc': u'2.0', u'result': u'0xba7757361234d58004753ad3b9bcfa8ae9e9e94dbbffb515168ed830c37d8b30', u'id': 83}
{u'jsonrpc': u'2.0', u'result': u'0x2', u'id': 83}
{u'jsonrpc': u'2.0', u'result': u'0x68418a1d93d8001d87b01eb955cdd93fff04c1409ce91d11a2f074fc3bf4da08', u'id': 83}
{u'jsonrpc': u'2.0', u'result': u'0x3', u'id': 83}
````

The first line in the alternating sequence means that you've generated and submitted a transaction.  The second
shows the current latest blocknumber, in hex.  Seeing this second number increment means your system has mined a block.  This should
be confirmed by viewing the output of the Parity command.

If blocks are being mined, congratulations, your instance is running successfully!


Running the Block Explorer
--------------------------

SnowWhite comes with a minorly modified version of EtherParty (https://github.com/pdaian/explorer/), a blockchain explorer that
allows you to visualize the chain generated by SnowWhite.  

To download the explorer, clone https://github.com/pdaian/explorer/ into snowwhite.  To run the block explorer, simply install ``npm nodejs``,
and make sure the ``node`` CLI command opens node.js (on some distros, including Ubuntu 14.04, bundled with AWS, this may require 
creating a symlink like ``ln -s /usr/bin/nodejs /usr/bin/node``).

If you receive an error about running Parity with an RPC CORS domain, check the RPC CORS parameter described above and make sure 
it is accurate, then restart your Parity node.
		

Connecting Multiple Nodes
-------------------------

1. Run a single "anchor node" as in the "one node" instructions.  When the software starts up, it will give you an enode 
    address.  Copy and save this as your "anchor enode".  Make sure the port Parity is listening on is open, and the IP
    in the enode is not a private or internal IP.
2. Start a "key distribution server" on the anchor node.  The purpose of this server is to distribute one
    unique key to every instance of SnowWhite you spawn, ensuring that each node is mining and making transactions on its own
    account.  To do this, go to the ``parity/listener`` directory and run ``python run.py [HOME DIRECTORY PATH]``
    (eg for AWS - ``python run.py /home/ubuntu/``).  Note the IP of this machine.
3. For the remainder of the installs, we provide a script, ``automated_install.py" that will download, build, and provision
    mining credentials for SnowWhite.  To run it, you must run 
    ``python automated_install.py [path to machine home directory] [IP of key distribution server above] [anchor enode]``
    The script assumes the presence of and packages on apt-get that have been tested on Ubuntu (AWS/14.04 image).
    Example arguments: ``python automated_install.py /home/ubuntu/ 172.31.13.94 enode://k93...``
    You can also download this script from https://pdaian.com/automated_install.py
4. After ``automated_install.py`` finishes on a node, you can confirm Parity is running on the node by running
    ``ps x | grep [p]arity``.
5. Before mining, make sure you run the peering script described in the next section, and it executes with no errors.
6. To start generating transactions and mining blocks on a node, run ``python parity.py`` in the ``pyrpc`` subfolder.
    To mine in the background, the command would look something like:
    ``nohup python [path to]/parity/pyrpc/parity.py </dev/null > /dev/null 2>&1 &``
    To mine with multiple processes, you may run the command multiple times.


Management - RPC and SSH
------------------------

Once either a single or multiple node instance of SnowWhite is spawned, you can connect to its RPC control on port 8545.
RPC functionality is described on the Parity Wiki (eg - https://github.com/ethcore/parity/wiki/JSONRPC-eth-module)

We also provide several management utilities that can be run from the anchor node in the ``pyrpc`` folder.  They are as follows:
- ``forcepeer.py`` - Run this once all nodes are started and listening.  This fully peers the network, forcing all nodes
    to connect directly to each other and enforcing full connectivity of the nodes.
- ``status.py`` - Run this when mining on child nodes.  This will show the current status of every node in the network
    (every node that runs ``automated_install.py`` also runs ``provision_credentials.py``, which pings the anchor node,
    records the child node's IP, and gives the child node the address it should use to mine)
- ``churn.py`` is used to induce network churn.  Edit the global parameters to define a cool off period, sample size in nodes,
    and downtime period for introducing the churn used in the project evaluation.
- ``blockstats.py`` crawls the blockchain and generates a ``chaindata`` file in home with a summary of all blocks and their
    timestamps, size in bytes, and number of transactions contained.  This is used to generate graphs later.

All of these utilities require a full nodes list in ~/nodes, and can thus **only be run from the anchor node**.  

All anchor node scripts are also hardcoded for AWS, where the default home directory is ``/home/ubuntu``.  
They may need to be edited if Parity lives in a directory other than ``/home/ubuntu``.


Running Tests
-------------

To run unit tests of Snow White only, run:
	cargo test snow -p ethcore

in the root of the project directory.

Any test with "NEW" as a prefix in the name was added specifically for SnowWhite.  Any test without "NEW" as a prefix was carried over
from the BasicAuthority module described in the "Code Changes" section.


Gathering Graphs/Data
---------------------

To gather the graphs and data in the final report, the following process was used:

1. Start a multi-node mining network as described in the "Connecting Multiple Nodes" section.  Do not begin mining yet. 
2. Run ``graphs/gather_resources.py``.  This will begin gathering data for the resource consumption (CPU, memory) graphs drawn.
3. Start mining on a single node as described in "Connecting Multiple Nodes".
4. Wait a minute or so.
5. Start mining on multiple nodes as described in "Connecting Multiple Nodes".  Do not mine on the node gathering data.
6. Optionally, start mining on the node gathering data.
7. Stop mining on all nodes.
8. To gather a summary of the blockchain generated by these nodes, add the node IPs to a file "~/nodes", one IP per line.
9. Run "blockstats.py" in the "pyrpc" folder.  This will gather the blockchain statistics used in the first graphs.
   Preferably, do this on the same machine used to gather CPU/memory data (in case of blockchain forks), but any machine should do.
10. For the average graphs, do the above on all nodes in your cluster.
11. Aggregate the resulting data with ``graphs/gather_all_data.py``
12. Draw the graphs with ``graphs/draw_graphs.py``.  Data must be in the form of ``parity/graphs/data/[node ID]/chaindata`` (and
    resources).  You must manually edit the nodes and/or top_nodes array (both are provided as an example) to include the node data
    you want to use in the graph.
12. Enjoy the graphs!


Modifying the Chain Spec
-------------------------

To modify the chain specification, including adding or removing authorities mid-chain, simply modify the ``chain_spec.json`` file as desired.
This file is copied into the home directory of the node you are running as part of copying the skeleton or the automated install.

Specifically, accounts can easily be added or removed from the ``authorities`` field to enable these accounts to mine.  Note that if two nodes
in a multiple node network have different ``authorities`` sets, their chains may diverge, leading to consensus failure.

Other parameters of the chain that can be modified are covered in the Parity documentation here: 
     https://github.com/ethcore/parity/wiki/Private-chains


Original README
---------------

The original Parity README is included in PARITY_README.md and contains general information on Parity, the upstream system of SnowWhite.


Assistance?
-----------

This project represents a modification to an extremely complex and experimental distributed consensus system.  While I believe the above 
instructions are comprehensive and should be workable, please don't hesitate to contact me with any questions / requests for clarification.

While I have also tried to test this system extensively (on both AWS clusters and with some unit testing), it is possible that consensus bugs
may result in the blockchain forking permanently at some point or ceasing to process new blocks (in case of the violation of a fundamental
time constraint).  If this rare scenario occurs, I am happy to do a postmorterm and explain how to proceed.

E-mail me any time at pad242@cornell.edu.  I will also be on campus until at least Thursday, Dec. 15 and can walk through setup or
experiments in person.
