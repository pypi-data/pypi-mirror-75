# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup

import urllib.parse
import urllib.request

import re


class Recipes(object):

	@staticmethod
	def get(url):

		html_content = urllib.request.urlopen(url).read()
		soup = BeautifulSoup(html_content, 'html.parser')

		#image_url = str(soup.find("picture", {"class": "recipe-cover-blur"}).find("img").text)
		image_url=soup.find("picture", {"class": "recipe-cover-blur"}).find('img')["src"]

		list_ingredients=[]
		ingredients_data = soup.findAll("span", { "class": "recipe-ingredients-item-label"})
		for i in ingredients_data:
			list_ingredients.append(i.text)

		rate = (soup.find("span", {"class": "rating-grade"}).text).replace("\n        ", "")

		preparation_data = soup.findAll("div", {"class": "recipe-steps-text"})

		list_instructions = []
		for i in preparation_data:
			list_instructions.append(i.text)

		try:
			name=soup.find("span", {"class":"recipe-title"}).text
		except:
			name="Inconnu"
   
		data = {
			"url": "http://www.750g.com/"+uri,
			"image": image_url,
			"name": name,
			"ingredients": list_ingredients,
			"instructions": list_instructions,
			"rate": rate
		}

		return data








