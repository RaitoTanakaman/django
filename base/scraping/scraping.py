# -*- coding: utf-8 -*-
from base import models
from gettext import find
from selenium import webdriver
from time import sleep
import googlemaps
from tqdm import tqdm
from selenium.webdriver.chrome.options import Options


def WalkerPlus():
    googleapikey = 'AIzaSyClfcwgPYqCtYvepDoqf0IVq675UxB_-R4'
    gmaps = googlemaps.Client(key=googleapikey)

    options = Options()
    options.add_argument('--headless')

    driver = webdriver.Chrome('../scraping/chromedriver')
    driver.get('https://www.walkerplus.com/spot_list/ar0101/sg0112/')

    i = 0
    while True:
        i += 1
        c = -1
        sleep(1)
        while c < 9:
            c += 1
            sleep(1)
            title = driver.find_elements_by_class_name("m-mainlist-item__ttl")
            place = driver.find_elements_by_class_name("m-mainlist-item__map")
            title_text = title[c].text
            place_text = place[c].text
            # place_text_length = place_text.len()
            if '区' in place_text:
                if '道' in place_text:
                    find_dou = place_text.find('道')
                    place_text_dou = place_text[find_dou + 1:].strip()
                    find_city = place_text_dou.find('市')
                    place_text_after = place_text[find_city + 1:]
                    print(place_text_after)
            elif '郡' in place_text:
                if '道' in place_text:
                    find_dou = place_text.find('道')
                    place_text_dou = place_text[find_dou + 1:].strip()
                    find_text = place_text.find('郡')
                    place_text_after = place_text[find_text + 1:]
                    print(place_text_after)
            else:
                if '道' in place_text:
                    find_dou = place_text.find('道')
                    place_text_after = place_text[find_dou + 1:].strip()
                print(place_text_after)

            place = models.Place.objects.get(name='北海道')

            city = models.City.objects.get_or_create(
                place=place, city=place_text_after)

            city_city = models.City.objects.get(city=place_text_after)

            driver.get(title[c].get_attribute('href'))
            mdtc = driver.find_element_by_class_name(
                "m-detailmain-table__contents")
            txtmdtc = mdtc.text
            txtreplace = txtmdtc.replace('[地図]', '')
            print(txtreplace)
            gmap_list = gmaps.geocode(txtreplace)

            gl = gmap_list[0]["geometry"]["location"]
            print("Latitude : ", gl["lat"])
            print("Longitude : ", gl["lng"])
            sleep(1)

            campsite = models.Campsite.objects.get_or_create(
                city=city_city,
                campsite=title_text,
                latitude=gl["lat"],
                longitude=gl["lng"])

            driver.back()
            sleep(2)

        else:
            next_link = driver.find_element_by_class_name("m-pager__next")
            driver.get(next_link.get_attribute('href'))
            if i > 25:
                break
