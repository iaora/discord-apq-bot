from apq_discord_bot import db, client
from apq_discord_bot.image_ocr import *
import time


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
	print("before: ", prices)
	# Verify the length of the number is similar to the others
	avg_price_len = avg_price_len/len(prices)
	print("avg_price_len: ",avg_price_len)
	prices = list(filter(lambda x: (len(str(x)) >= avg_price_len), prices))
	print("after: ", prices)


def add_owl_screenshot(url):
	img_list = process_image_to_text(url)

	item_name, item_name_index  = find_item_name(img_list)
	if item_name_index == -1: return
	print(item_name)

	find_item_prices(img_list[item_name_index+1:])



