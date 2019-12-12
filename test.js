Web3 = require('web3')
const async = require('async');
var web3 = new Web3(new Web3.providers.HttpProvider('https://ropsten.infura.io/v3/66092b83a4de4330b7cc5df887e3ae4b'));
var abi = require('./abi.json')
var addressContract = "0x3C2C8752FD54E5C72a0365B9F402234949d03f8a"
const contract = new  web3.eth.Contract(abi,addressContract)
const address1 = "0x5D227b6bF92C669df6E2bD47dB065D30C88F3225"
const privateKey = "e6b62e897fb1cadc8bf2dac2ab657757497e5ef1921342d2c6acdb68fd5cb5ee"



var myBalanceWei = web3.eth.getBalance(address1)
console.log(myBalanceWei);
// async function getbalance(){
// 	var balance = await web3.eth.getBalance(address1)
// 	// var myBalance = await web3.fromWei(balance, 'ether')
// 	console.log(balance);
// 	return balance
// }

// console.log(getbalance());

// // async sendETHtoAddress(address_from,address_to,value){

// // }

// console.log(getbalance(address1));

// const address2 = "0x102340A8b2766D280416539732fce638eEd18795"
// // balance = web3.toDecimal(balance);


// async function create_txt(){
// 	tuan = await web3.eth.sendTransaction({
// 		from:address1,
// 		data: "0x7f7465737432000000000000000000000000000000000000000000000000000000600057"
// 	})
// 	console.log(tuan);
// }

// async function sendETHtoSmartContract(){
// 	web3.eth.sendTransaction({
// 	  from: address1,
// 	  to: contractAddress,
// 	  value: 100
// 	})
// }
// create_txt()
// // console.log(web3);
// console.log(web3);