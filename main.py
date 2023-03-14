import eel
import requests
from bs4 import BeautifulSoup as BS
from array import *
import sqlite3 as sql
from flask import Flask, jsonify

stocks = []
koef = []
prices = []
	
@eel.expose
## utility before setting stocks
def clear_stocks():
	stocks.clear()
	koef.clear()

@eel.expose
## setting stocks names from input fields
def set_stocks(name, part):
	stocks.append(name)
	koef.append(float(part))

@eel.expose
## getting last prices from www.marketwatch.com
def let_calc():
	indexsum = 0
	for j in range(len(stocks)):
		zxc = requests.get("https://www.marketwatch.com/investing/stock/"+stocks[j])
		html = BS(zxc.content, 'lxml')
		xy = html.find("bg-quote", class_="value")
		prices.append(float(xy.text))
		indexsum += prices[j]*koef[j]
		j += 1
	index = indexsum/(sum(koef))
	print(stocks)
	print(koef)
	print(index)
	return index

@eel.expose
## creating/change index in indexes.db by sqlite3
def save_index(new_index_name):
	db = sql.connect('indexes.db')
	cursor = db.cursor()
	cursor.execute("""
		CREATE TABLE IF NOT EXISTS """+new_index_name+""" (
			stock_name string,
			koef float)
	""")
	i=0
	cursor.execute("DELETE FROM "+new_index_name+"")
	for i in range(len(stocks)):
		cursor.execute("INSERT INTO "+new_index_name+" VALUES (?, ?)", (stocks[i], koef[i]))
		i+=1
	db.commit()
	db.close()

@eel.expose
## initialize saved indexes to html
def saved_indexes_init():
	db = sql.connect('indexes.db')
	cursor = db.cursor()
	cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
	saved_index_name = cursor.fetchall()
	db.close()
	return saved_index_name
	
@eel.expose
def get_saved_index(selected_index):
	db = sql.connect('indexes.db')
	print(selected_index)
	cursor = db.cursor()
	cursor.execute("SELECT stock_name FROM "+selected_index)
	stock_count = len(cursor.fetchall())
	cursor.execute("SELECT stock_name FROM "+selected_index)
	for x in range(stock_count):
		stocks.append(cursor.fetchone()[0])
	cursor.execute("SELECT koef FROM "+selected_index)
	for x in range(stock_count):
		koef.append(cursor.fetchone()[0])
	print(stocks)
	print(koef)
	db.close()

eel.init("web")
eel.start("main.html", size=(800, 800))