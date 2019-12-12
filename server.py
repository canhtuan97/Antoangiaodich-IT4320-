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
@aiohttp_jinja2.template('interface.jinja2')
async def hello(request):
	
	print("canhtuan")


@routes.get('/check_balance')
async def check_balance(request):
	raise web.HTTPFound('/')


@routes.post('/check_balance')
@aiohttp_jinja2.template('interface.jinja2')
async def check_balance(request):
	data = await request.post()
	address = data['address']
	print(address)
	balance =  getBalance(address)
	print(balance)
	balance_convert = convertWeitoETH(balance)
	return {'balance':balance_convert}



@routes.get('/postDataToEth')
async def postDataToEth(request):
	raise web.HTTPFound('/')

@routes.post('/postDataToEth')
@aiohttp_jinja2.template('interface.jinja2')
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
		tuan = postDataToBlockchain(privatekey,data_hex)
		print(tuan)
		return {'tx':tuan}

	else:
		return {'tx':"Đặt cược không thành công"}

@routes.get('/set_number_win')
async def set_number_win(request):
	raise web.HTTPFound('/')


@routes.post('/set_number_win')
@aiohttp_jinja2.template('interface.jinja2')
async def set_number_win(request):
	
	data = await request.post()
	privateKey = data['privateKey']
	number_win = random.randint(1 , 99)
	print(number_win,privateKey)
	tx = set_numberWin(number_win,privateKey)
	print(tx)
	return {'tx_set_number':number_win}


@routes.get('/submit')
async def submit(request):
	raise web.HTTPFound('/')


@routes.post('/submit')
@aiohttp_jinja2.template('interface.jinja2')
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
	time_end = datetime.timedelta(hours=1, minutes=10, seconds=0, microseconds=0)
	time_block_chain = datetime.timedelta(hours=hour_block_chain, minutes=hour_block_chain, seconds=second_block_chain, microseconds=0)


	if year == year_block_chain and month == month_block_chain and day == day_block_chain :
		
		if time_end > time_block_chain and time_end < time_now_format:
			print("oki")
			print(number,privateKey,money,type(tx))
			tuan = submitSmartContract(number,privateKey,money,str(tx))
			print(tuan)
			# if int(get_number_win_from_contract) == int(info['number']):
				
			# 	print(money)
			# 	# tx= submit(int(info['number']),address,privateKey,1)
			# 	# print(tx)
			# else:
			# 	print("ban khong trung thuong")
		else:
			print("sai")
	else:
		print("Da qua ngay thang nam")

if __name__ == "__main__":
	app.add_routes(routes)
	web.run_app(app)