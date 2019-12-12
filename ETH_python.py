from web3 import Web3
from eth_account import Account
import datetime
from web3.auto import w3
import random
f = open("abi.json", "r")
abi = f.read()

web3 = Web3(Web3.HTTPProvider('https://ropsten.infura.io/v3/66092b83a4de4330b7cc5df887e3ae4b'))
# web3 = Web3(Web3.HTTPProvider('http://127.0.0.1:7545'))
addressContract = '0x8AfAa36c086CE8C77089Dd846E8Cfe771446281b'  
contract = web3.eth.contract(address= addressContract, abi=abi)
address1 = "0x5D227b6bF92C669df6E2bD47dB065D30C88F3225"
privateKey1 = "e6b62e897fb1cadc8bf2dac2ab657757497e5ef1921342d2c6acdb68fd5cb5ee"
   

def privateKeytoAddress(private_key):
	acct = Account.privateKeyToAccount(private_key)
	return acct.address
# print("trancanhtuan " ,privateKeytoAddress("4491afbdf42a09657e00290398ae28eb91181328483494ecf7bb3de7548c2ac9"))

def send_eth_to_smart_contract(private_key,amount):
	address = privateKeytoAddress(private_key)
	print(private_key,address)
	signed_txn = web3.eth.account.signTransaction(dict(
	    nonce=web3.eth.getTransactionCount(address),
	    gasPrice = web3.toWei('50', 'gwei'), 
	    gas = 800000,
	    to= addressContract,
	    value=web3.toWei(amount,'ether')
	  ),private_key)
	txt = web3.eth.sendRawTransaction(signed_txn.rawTransaction)
	return (web3.toHex(txt))
# print(send_eth_to_smart_contract("4491afbdf42a09657e00290398ae28eb91181328483494ecf7bb3de7548c2ac9",0.1))

def postDataToBlockchain(private_key,data):
	address = privateKeytoAddress(private_key)
	print(private_key,address)
	signed_txn = web3.eth.account.signTransaction(dict(
	    nonce=web3.eth.getTransactionCount(address),
	    gasPrice = web3.toWei('50', 'gwei'), 
	    gas = 800000,
	    value=web3.toWei(0.1,'ether'),
	    data = data
	  ),private_key)
	txt = web3.eth.sendRawTransaction(signed_txn.rawTransaction)
	return (web3.toHex(txt))

# print(postDataToBlockchain(privateKey,"7b276e756d626572273a20273838272c2027616d6f756e74273a2027302e31272c202779656172273a20323031392c20276d6f6e7468273a2031322c2027646179273a2031322c2027686f7572273a20302c20276d696e757465273a20362c20277365636f6e64273a2031317d"))

# def privateKeytoAddress(privatekey):
# 	acct = Account.privateKeyToAccount(privatekey)
# 	return acct.address
# # tuan = privateKeytoAddress("e6b62e897fb1cadc8bf2dac2ab657757497e5ef1921342d2c6acdb68fd5cb5ee")
# # print(tuan)

def getBalance(address):
	balance = web3.eth.getBalance(address)
	return balance


def checkBalanceContract():
	balance = contract.functions.getBalance().call()
	return balance
# tuan = checkBalanceContract();
# print(tuan)
#-------------------
def set_numberWin(number,private_key):
	address = privateKeytoAddress(private_key)
	nonce =  web3.eth.getTransactionCount(address)
	tx_dict = contract.functions.set_number_win(number).buildTransaction({
        'from': address,
        'gas': 800000,
        'gasPrice': web3.toWei('50', 'gwei'),
        'nonce': nonce,
        'chainId': 3
    })
	signed_tx =  web3.eth.account.signTransaction(tx_dict, private_key)
	tx_hash =  web3.eth.sendRawTransaction(signed_tx.rawTransaction)
	return (web3.toHex(tx_hash))
# tuan = set_numberWin(12,privateKey)
# print(tuan)



#--------------------------------------------
def submitSmartContract(number,private_key,amount,tx_hash):
	address = privateKeytoAddress(private_key)
	money = web3.toWei(amount, 'ether')
	nonce =  web3.eth.getTransactionCount(address)
	tx_dict = contract.functions.submit(number,address,money,tx_hash).buildTransaction({
        'from': address,
        'gas': 800000,
        'gasPrice': web3.toWei('50', 'gwei'),
        'nonce': nonce,
        'chainId': 3
    })
	signed_tx =  web3.eth.account.signTransaction(tx_dict, private_key)
	tx_hash =  web3.eth.sendRawTransaction(signed_tx.rawTransaction)
	return (web3.toHex(tx_hash))
# tuan = submitSmartContract(12,privateKey1,0.1,"0xb0c4b8edc77acf635d2fce509f42d35026367853a6649723566c4ac696c22fdb")
# print(tuan)


def convertWeitoETH(money):
	money_convert = web3.fromWei(money, 'ether')
	print(money_convert)
	return money_convert
# tuan = convertWeitoETH(3822320847500000001)
# print(tuan)

def get_number_win():
	number_win = contract.functions.number_win().call()	
	return number_win




	
def getTransaction(txHash):
	data = web3.eth.getTransaction(txHash)
	input = data['input']
	tuan = bytearray.fromhex(input[2:]).decode()
	return tuan
# tuan = getTransaction("0x242c4992de691c7b56489fdcc8c8fc9ba50c091c044da39621f05c43f4e8dc63")
# print(tuan)

# print(tuan)