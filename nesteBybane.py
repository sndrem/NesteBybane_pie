#!/usr/bin/python
# coding=utf-8

import requests as req
from bs4 import BeautifulSoup
import datetime, time
import Adafruit_CharLCD as LCD

# Raspberry Pi pin configuration:
lcd_rs        = 25  # Note this might need to be changed to 21 for older revision Pi's.
lcd_en        = 24
lcd_d4        = 23
lcd_d5        = 17
lcd_d6        = 21
lcd_d7        = 22
lcd_backlight = 4

# Define LCD column and row size for 16x2 LCD.
lcd_columns = 16
lcd_rows    = 2


# Initialize the LCD using the pins above.
lcd = LCD.Adafruit_CharLCD(lcd_rs, lcd_en, lcd_d4, lcd_d5, lcd_d6, lcd_d7,
                           lcd_columns, lcd_rows, lcd_backlight)

now = datetime.datetime.now()
year = now.year
month = now.month
day = now.day
hour = now.hour
minute = now.minute
SKYSS_URL = "https://reiseplanlegger.skyss.no/scripts/TravelMagic/TravelMagicWE.dll/svar?from=Brann%20stadion,%20bybanestopp%20%28Bergen%29&to=Byparken,%20bybanestopp%20%28Bergen%29&direction=1&lang=nn&instant=1&date=" + str(day) + "." + str(month) + "." + str(year) + "&time=" + str(hour) + ":" + str(minute)

# Bruk requests til å hente bybanetider
page = req.get(SKYSS_URL)

# Gjør kildekoden om til et bs4-objekt
soup = BeautifulSoup(page.text, 'html.parser')

class BybaneTime():

	def __init__(self, start, end, timeOfTravel):
		self.start = start
		self.end = end
		self.timeOfTravel = timeOfTravel

	def getStart(self):
		return self.start

	def getEnd(self):
		return self.end

	def getTimeOfTravel(self):
		return self.timeOfTravel


def parsePage(soup):
	nextTwo = soup.select(".maincontent .tm-block-b")[:2]
	times = []
	for span in nextTwo:
		timeblock = span.select(".tm-result-time .tm-result-time-wrapper")
		travelTime = span.select(".tm-result-info-val")[0].text
		start = timeblock[0].select(".tm-result-fratil")[0].text
		end = timeblock[1].select(".tm-result-fratil")[0].text
		bybaneTime = BybaneTime(start, end, travelTime)
		times.append(bybaneTime)

	text = ""
	for bbt in times:
		text += "Bybane: {} - {} ({})\n".format(bbt.getStart(), bbt.getEnd(), bbt.getTimeOfTravel())
	text = text.rstrip()
	print(text)
	lcd.message(text)



def main():
	lcd.clear()
	parsePage(soup)
	
if __name__ == '__main__':
	main()
