import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import time
import csv
import re
import unidecode


driver = webdriver.Firefox(executable_path = '..\geckodriver.exe')
link_players = 'https://www.worldpadeltour.com/jugadores/'
index = 'https://www.worldpadeltour.com'
headers = {
"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,\
*/*;q=0.8",
"Accept-Encoding": "gzip, deflate, sdch, br",
"Accept-Language": "en-US,en;q=0.8",
"Cache-Control": "no-cache",
"dnt": "1",
"Pragma": "no-cache",
"Upgrade-Insecure-Requests": "1",
"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/5\
37.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36"
}

def remove_accents(raw_text):
    raw_text = re.sub(u"[àáâãäå]", 'a', raw_text)
    raw_text = re.sub(u"[èéêë]", 'e', raw_text)
    raw_text = re.sub(u"[ìíîï]", 'i', raw_text)
    raw_text = re.sub(u"[òóôõö]", 'o', raw_text)
    raw_text = re.sub(u"[ùúûü]", 'u', raw_text)
    raw_text = re.sub(u"[ýÿ]", 'y', raw_text)
    raw_text = re.sub(u"[ª]", 'maria', raw_text)
    raw_text = re.sub(u"[ñ]", 'n', raw_text)
    return raw_text

def camel_case_split(name):
	splitted = re.sub('([A-Z][a-z]+)', r' \1',re.sub('([A-Z]+)', r' \1', name)).split()
	converted_list = [x.lower() for x in splitted]
	return converted_list

def compose_url(array_name):
	new_url = '-'.join(array_name)
	return remove_accents(new_url)

def build_url(name):
	compound_url = link_players + compose_url(camel_case_split(name))
	return compound_url


def scroll_down(driver, link):
	driver.get(link)
	driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
	print("Cargando datos.")
	time.sleep(3)

	web = driver.page_source
	content = BeautifulSoup(web, "lxml")
	count = 1 #Player counter

	for player in content.find_all('li', class_='c-player-card__item'):
		name = player.find('div', class_='c-player-card__name').text
		score = player.find('div', class_='c-player-card__score').text
		print("Jugador / puntuacion \n")
		print(name + '\n' + score)
		print(" ··········· \n")
		print(build_url(name))
		count += 1

	print("Contador de jugadores ", count)
	driver.close()

#main
scroll_down(driver, link_players)