from apq_discord_bot import db, client
from apq_discord_bot.image_ocr import *
import apq_discord_bot.db_helper as db_helper
from statistics import median

def find_item_name(img_list):
	common_items = ['[Mastery Book]', 'Apple', 'Scroll', 'Ore', 'Stone']
	
	for i in range(len(img_list)):
		if any(common_item in img_list[i] for common_item in common_items):
			return img_list[i], i
	
	return '',-1


def find_item_prices(img_list):
	prices = []
	avg_price_len = 0

	# Parse through list of items to extract numbers only
	for i in img_list:
		try:
			cleaned_i = ''.join(list(filter(str.isdigit, i)))
			avg_price_len += len(cleaned_i)
			prices.append(int(cleaned_i))
		except ValueError:
			continue
	# Verify the length of the number is similar to the others
	avg_price_len = avg_price_len/len(prices)
	prices = list(filter(lambda x: (len(str(x)) >= avg_price_len), prices))
	return prices

"""Add all prices parsed from owl screenshot into item_log collection. New document per price point"""
def log_item_prices(item_name, prices):
	for price in prices:
		data = {
			'date' : db_helper.get_current_time(),
			'item_name' : item_name,
			'price' : price,
		}
		db.collection('price_log').add(data)
		#print (f' {data} added into document {discord_author_id}')

"""Query all of the prices of one item. Update the items collection with the new min, max, avg, median, date"""
def update_items_collection(item_name):
	log_query = db.collection('price_log').where('item_name', '==', item_name).get()
	prices = [doc.to_dict()['price'] for doc in log_query]
	
	item_db_id = db_helper.find_single_doc_id(db.collection('items'),'item_name',item_name)

	db.collection('items').document(item_db_id).update(
		{
			'avg' : int(sum(prices)/len(prices)),
			'max' : max(prices),
			'median' : median(prices),
			'min' : min(prices),
			'update_date' : db_helper.get_current_time(),
		}
	)


def add_item_to_items_collection(item_name):
	if db.collection('items').where('item_name','==',item_name).get():
		return
	data = {
		'item_name' : item_name,
		'avg' : 0,
		'max' : 0,
		'median' : 0,
		'min' : 0,
		'update_date' : db_helper.get_current_time(),
	}
	db.collection('items').add(data)
		

def add_owl_screenshot(url):
	img_list = process_image_to_text(url)
	print(img_list)

	item_name, item_name_index  = find_item_name(img_list)
	if item_name_index == -1: return
	print(item_name)

	prices = find_item_prices(img_list[item_name_index+1:])
	print(prices)

	log_item_prices(item_name, prices)
	add_item_to_items_collection(item_name)
	update_items_collection(item_name)

	return item_name


def get_item_info(item_name):
	item_info = db.collection('items').where('item_name', '==', item_name).get()
	if len(item_info) == 0:
		return 
	return item_info[0].to_dict()
