from aiohttp import web
from ETH_python import *
import aiohttp_jinja2
import jinja2
import datetime
from datetime import date
import time
import json 
import ast 
import pymongo
import random
myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["Antoangiaodich"]
mycol = mydb["tx_hash"]


routes = web.RouteTableDef()
app = web.Application()

aiohttp_jinja2.setup(app,loader=jinja2.FileSystemLoader('./templates'))


@routes.get('/')
@aiohttp_jinja2.template('home.jinja2')
async def hello(request):
	
	print("canhtuan")


@routes.get('/check_balance')
@aiohttp_jinja2.template('home.jinja2')
async def check_balance(request):
	print("home.jinja2")


@routes.post('/check_balance')
@aiohttp_jinja2.template('home.jinja2')
async def check_balance(request):
	data = await request.post()
	address = data['address']
	print(address)
	balance =  getBalance(address)
	print(balance)
	balance_convert = convertWeitoETH(balance)
	return {'balance':balance_convert}


#-------------------------------
@routes.get('/postDataToEth')
@aiohttp_jinja2.template('user1.jinja2')
async def postDataToEth(request):
	print("user1.jinja2")

@routes.post('/postDataToEth')
@aiohttp_jinja2.template('user1.jinja2')
async def postDataToEth(request):
	data = await request.post()
	privatekey = data['private_key']
	amount = data['amount']
	number = data['number']
	print(privatekey,amount,number)

	time_now = datetime.datetime.now()
	time_end = time_now.replace(hour=18, minute=30, second=0, microsecond=0)
	print(time_now)
	if time_now < time_end:
		
		today = date.today() 
		year = time_now.year
		month = time_now.month
		day = time_now.day
		hour = time_now.hour
		minute = time_now.minute
		second = time_now.second
		print(minute)
		data = {
			'number':number,
			'amount':amount,
			'year':year,
			'month':month,
			'day':day,
			'hour':hour,
			'minute':minute,
			'second':second
		}
		print(data)
		
		data_string = str(data).encode('utf-8')
		data_hex = data_string.hex()
		print(data_hex)
		tx_send_money = await send_eth_to_smart_contract(privatekey,amount)
		# time.sleep(6)
		tx_post_data = await postDataToBlockchain(privatekey,data_hex)
		print(tx_post_data,tx_send_money)
		return {'tx':tx_post_data}

	else:
		return {'tx':"Đặt cược không thành công"}

@routes.get('/set_number_win')
@aiohttp_jinja2.template('admin.jinja2')
async def set_number_win(request):
	print ("admin.jinja2")


@routes.post('/set_number_win')
@aiohttp_jinja2.template('admin.jinja2')
async def set_number_win(request):
	
	data = await request.post()
	privateKey = data['privateKey']
	number_win = random.randint(1 , 99)
	print(number_win,privateKey)
	tx = set_numberWin(number_win,privateKey)
	print(tx)
	return {'tx_set_number':number_win}

#---------------------------------
@routes.get('/submit')
@aiohttp_jinja2.template('user2.jinja2')
async def submit(request):
	print("user2.jinja2")


@routes.post('/submit')
@aiohttp_jinja2.template('user2.jinja2')
async def submit_tx(request):
	data = await request.post()
	tx = data['tx']
	privateKey = data['privateKey']
	print(tx,privateKey)
	info_block = getTransaction(tx)
	print(info_block)
	info = ast.literal_eval(info_block) 
	
	number = int(info['number'])
	money = float(info['amount'])

	print(number,money)

	time_now = datetime.datetime.now()
	year = time_now.year
	month = time_now.month
	day = time_now.day
	hour = time_now.hour
	minute = time_now.minute
	second = time_now.second

	year_block_chain = info['year']
	month_block_chain = info['month']
	day_block_chain = info['day']
	hour_block_chain = info['hour']
	minute_block_chain = info['minute']
	second_block_chain = info['second']


	time_now_format =  datetime.timedelta(hours=hour, minutes=minute, seconds=0, microseconds=0)
	time_end = datetime.timedelta(hours=8, minutes=21, seconds=0, microseconds=0)
	time_block_chain = datetime.timedelta(hours=hour_block_chain, minutes=hour_block_chain, seconds=second_block_chain, microseconds=0)
	print(time_block_chain)

	if year == year_block_chain and month == month_block_chain and day == day_block_chain :
		
		if time_end > time_block_chain and time_end < time_now_format:
			print("oki")
			number_win = get_number_win()
			if number_win == number:
				print("oki")
				number_win = get_number_win()
				if number_win == number:
					print(number,privateKey,money,type(tx))
					tuan = submitSmartContract(number,privateKey,money*2,str(tx))
					print(tuan)
					return {'msg':"Woa! you win"}
				else:
					return {'msg':"Hmm error number"}
				
		else:
			return {'msg':"Hmm error time"}
	else:
		return {'msg':"Hmm error "}

if __name__ == "__main__":
	app.add_routes(routes)
	web.run_app(app)