# Naive Chain

The goal of this exercise is to understand the principles of blockchain technology and how mining works. You will create a simple blockchain network in JavaScript and add proof-of-work mining by modifying the existing code to add a proof-of-work calculation (via adding nonce + timestamp in the blocks). The basic concept of blockchain is quite simple: a distributed ledger that maintains a continuously growing list of ordered records (blocks). Most of the code is based on this project: [naivechain](https://github.com/lhartikk/naivechain). Thanks to the original authors. 

For this exercise, you will need Linux or Linux-like command-line environment. We use Ubuntu distribution, but each other will work fine in most cases. Also, you will need "node.js", "npm" and "cURL" installed.  

## Block Structure
To keep things as simple as possible, the blockchain contains only the most necessary elements: index, timestamp, data, hash and previous hash. Following the blockchain concept, the hash of the previous block must be found in the block to preserve the chain integrity. 

## Genesis Block
An in-memory JavaScript array is used to store the blockchain. The first block of the blockchain is always a so-called “genesis-block” and is hardcoded. We take it with the function which returns a new Block with usual attributes. The Block index is 0, the “previousHash” don’t exist in reality and we give him a string value “0”. The current Block hash is hardcoded and data field contains the string “my genesis block”. 

## Latest Block
The getLatestBlock function returns the latest element in the blockchain array.

## Calculate the Hashes
Create the “calculateHash” function in the code. This function is the moment of mining when the miner calculates the hash for the next block. For now, we are only calculating the hash given the input data. The actual mining process will be implemented later in this exercise. 

When we want to calculate the hash for the block we will use the calculateHashForBlock function. It will execute the calculateHash function for a given block and return SHA256 hash of a string which is the result of concatenating block.index, block.previousHash, block.timestamp and block.data. 

## Next Block
When we want to generate a block, we must first know the hash of the previous block because this is the link between chains of the blockchain.  Next, we must create the rest of the required content (index, hash, data and timestamp). The Block data (message text) is something that is provided by the end-user.

## Validations
At any given time, we must be able to validate if a block or a chain of blocks are valid in terms of integrity. This is true especially when we receive new blocks from other nodes and must decide whether to accept them or not.

The addBlock function is used for adding new blocks. It will also use the isValidNewBlock function. 

To be sure that the block is working how is expected, create an isValidChain function which will perform some elementary checks for network validity. 

## Node Synchronization
In purpose of modeling the blockchain and mining blocks, the program has a system of communication between nodes. An essential part of a node is to share and sync the blockchain with other nodes. The following rules are used to keep the network in sync. 
* When a node generates a new block, it broadcasts it to the network 
* When a node connects to a new peer it queries for the latest block 
* When a node encounters a block that has an index larger than the current known block, it either adds the block to its current chain or queries for the full blockchain. 
No automatic peer discovery is used. The location (URLs) of peers must be manually added. 

## Servers
The node in the program actually exposes two web servers: One for the user to control the node (HTTP server) and one for the peer-to-peer communication between the nodes (Websocket server).

Using the environment variables is the way to specify communication ports. The process.env global variable is injected by the Node at runtime for the application to use and it represents the state of the system environment the application is in when it starts. 
 
We will use: 
*	HTTP interface to control the node 
*	Websockets to communicate with other nodes (P2P) 

### HTTP Server
With implemented REST API the user is able to interact with the node in the following ways: 
* Command /blocks will make a get request and list all blocks in the existing blockchain 
* Command /mineBlock will send a post request which will create a new block with a content given by the user, calculate the new block’s hash and add this new block to the blockchain. Then later it will broadcast a message to other peers. 
* Command /peers will make a get request and take an array with existing peers. If there are no peers, we will receive an empty array. 
* Command /addPeer will send a post request and connect peer to the given one.

The most straightforward way to control the node is with Curl: To get all blocks from the node enter: 
```bash
$ curl http://localhost:3001/blocks
```
### P2P Websocket HTTP Server
Now we need two more variables for p2p_port and one to initialize the peers. 
Create a variable for message types. We will use the MessageTypes to handle messages. 

We will receive message of: 
*	QUERY_LATEST - Query for the last block 
*	QUERY_ALL - Query for all the blocks 
*	RESPONSE_BLOCKCHAIN - Response message with the requested data (last block or all the blocks)

## Connect Nodes and Mine a Block 
First, establish the first node. The node will listen for signals from other nodes by WebSocket interface on port 6001 and will listen for commands via HTTP interface on port 3001. We can see the node's info on address: localhost:3001.
* Linux
```bash
HTTP_PORT=3001 P2P_PORT=6001 npm start
```
* Windows
```bash
set HTTP_PORT=3001 && set P2P_PORT=6001 && npm start
```
Now open a second terminal window and set the second peer in the chain. The second peer will listen for signals from other nodes on port 
6002 and will listen for commands via HTTP interface on port 3002. This node will receive information from the first peer via P2P communication by port 6001. We can see the node,s info on address: localhost:3002. Here on the picture are both nodes terminals. 
 
* Linux
```bash
HTTP_PORT=3002 P2P_PORT=6002 PEERS=ws://localhost:6001 npm start 
```
 
* Windows
```bash
set HTTP_PORT=3002 && set P2P_PORT=6002 && set PEERS=http://localhost:6001 && npm start
```
Now comes the most interesting part. With this, we command the first node to mine new block. His index will be the index of the previous block and it contains data "Some data to the first block”. 
 
* Linux
```bash
curl -H "Content-type:application/json" --data '{"data" : "Some data to the first block"}' http://localhost:3001/mineBlock 
```
* Windows

Postman API: POST request to http://localhost:3001/mineBlock.
```json
{
    "data" : "Some data to the first block"
}
```
Now mine the third block. Pay attention that the first node is the emitter of the block so he reports that new blocks sequence is no longer than existing blockchain and “Received blockchain is not longer than received blockchain. Do nothing”. But the other node reports that “We can append the received block to our chain”. 

* Linux
```bash
curl -H "Content-type:application/json" --data '{"data" : "Data to the third block"}' http://localhost:3001/mineBlock
```
* Windows

Postman API: POST request to http://localhost:3001/mineBlock.
```json
{
    "data" : "Data to the third block"
}
```
The next task is to create a third node. This is the screen before executing the command. 
* Linux: 
```bash
HTTP_PORT=3003 P2P_PORT=6003 PEERS=ws://localhost:6001 npm start
```
 
* Windows
```bash
set HTTP_PORT=3003 && set P2P_PORT=6003 && set PEERS=http://localhost:6001 && npm start
```
Open the third node address in the browser and compare with one of the old nodes. The third node has the same blocks.

## Proof-of-Work Mining

In real blockchains, a Proof Of Work is a piece of data which is difficult (costly, time-consuming) to produce but easy for others to verify and which satisfies certain requirements. Producing a Proof Of Work can be a random process with low probability so that a lot of trial and error is required on average before a valid proof of work is generated. In order for a block to be accepted by network participants, miners must complete a Proof Of Work which covers all of the data in the block. Due to the very low probability of successful generation, this makes it unpredictable which worker computer in the network will be able to generate the next block. In our example, this competition is not presented and any generated block is valid. 

* Difficulty
This variable is the required number of zeroes at the beginning of the next block’s hash. The difficulty is important because without its value nobody will be able to prove that the found hash is valid or not.

* Nonce
This variable is the number which we will increase in an attempt to find the appropriate proof-of-work hash and mine the next block. The miner will start mining and increment thenonce searching for the hash satisfying the difficulty requirements. 

Note the following results: 
*	Block mining takes some time (a few seconds). This is due to the proof-of-work algorithm. 
* The last block hash has several leading zeroes depends on difficulty. This is the proof-of-work result. 

### Module
MI1: Module 7: E1/E2 
