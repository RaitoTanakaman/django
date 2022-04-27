
from base.models import Campsite, CampsiteScore, City, Local, Post, Place,  User, PostImage
import pandas as pd
from tqdm import tqdm
import random
from gettext import find
from selenium import webdriver
from time import sleep
import googlemaps
import os
import sys
sys.path.append(os.path.abspath(os.path.dirname(__file__)))


def auto_create_user():
    for i in tqdm(range(4900)):
        User.objects.create(
            username=i,
            name=i,
            email='haniwa20010810@icloud.com',
            is_email_verified=True,
        )


def auto_create_post():
    images = PostImage.objects.all()
    local = Local.objects.get(local='北海道・東北')
    place = Place.objects.get(local=local)
    cities = City.objects.filter(place=place)
    list = []
    list_c = []
    list_i = []
    list_number = [1, 2, 3, 4, 5]
    for u in range(4900):
        list.append(u)

    for c in cities:
        list_c.append(c)

    for img in images:
        list_i.append(img)

    for i in tqdm(range(90000)):
        li = random.choice(list_i)
        image = images.get(image=li.image)
        uu = random.choice(list)
        user_choice = User.objects.get(username=uu)
        lc = random.choice(list_c)
        city_choice = cities.get(city=lc)
        campsites = Campsite.objects.filter(city=city_choice)
        list_cps = []
        for cps in campsites:
            list_cps.append(cps)
        lcps = random.choice(list_cps)
        campsite_choice = campsites.get(campsite=lcps)
        score_choice = random.choice(list_number)
        post = Post.objects.create(
            host=user_choice,
            title=str(i),
            local=local,
            place=place,
            city=city_choice,
            campsite=campsite_choice,
            score=score_choice
        )
        post.img.add(image)

        CampsiteScore.objects.create(
            campsite=campsite_choice,
            user=user_choice,
            score=score_choice
        )


def auto_like():
    users = User.objects.all()[:100]
    posts = Post.objects.all()[:500]
    list = []
    index_list = []
    for user in tqdm(users):
        list.append(user)

    for r in range(1, 100):
        index_list.append(r)

    for post in tqdm(posts):

        list_random = random.sample(list, random.choice(index_list))
        for lr in list_random:
            post.liked.add(lr)
            post.like_count += 1


def auto_score():
    posts = Post.objects.all()
    score_list = [1, 2, 3, 4, 5]
    for post in posts:
        post.score = random.choice(score_list)
        print(post.score)


def auto_delete_post():
    posts = Post.objects.order_by('?')[:50000]
    for post in tqdm(posts):
        post.delete()


def user_data():
    users = User.objects.all()
    campsite = Campsite.objects.all()
    list = []

    for u in users:
        list_second = []
        for c in campsite:
            campsite_score = CampsiteScore.objects.filter(user=u, campsite=c)
            list_cs = []
            for cs in campsite_score:
                list_cs.append(cs.score)

            if list_cs == []:
                list_second.append(0)
            else:
                list_second.append(max(list_cs))

        list.append(list_second)

    df = pd.DataFrame(list)

    df_pickle = df.to_pickle('results.pickle')
    print(df)


def campsites_ratings():
    campsites_ratings = CampsiteScore.objects.all()
    list = []
    for cr in tqdm(campsites_ratings):
        list_second = []
        list_second.append(cr.user.id)
        list_second.append(cr.campsite.campsite)
        list_second.append(cr.score)
        list.append(list_second)

    df = pd.DataFrame(list)
    df_pickle = df.to_pickle('campsites_ratings.pickle')


def scraping_campsite():
    googleapikey = 'AIzaSyClfcwgPYqCtYvepDoqf0IVq675UxB_-R4'
    gmaps = googlemaps.Client(key=googleapikey)

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
            title_txt = title[c].text
            place = driver.find_elements_by_class_name("m-mainlist-item__map")
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

            place = Place.objects.get(name='北海道')

            city = City.objects.get_or_create(
                place=place, city=place_text_after)

            driver.get(title[c].get_attribute('href'))
            mdtc = driver.find_element_by_class_name(
                "m-detailmain-table__contents")
            txtmdtc = mdtc.text
            txtreplace = txtmdtc.replace('[地図]', '')
            print(txtreplace)
            gmap_list = gmaps.geocode(txtreplace)

            gl = gmap_list[0]["geometry"]["location"]

            sleep(1)
            driver.back()
            sleep(2)
            Campsite.objects.create(
                city=city,
                campsite=title_txt,
                latitude=gl["lat"],
                longitude=gl["lng"])

        else:
            next_link = driver.find_element_by_class_name("m-pager__next")
            driver.get(next_link.get_attribute('href'))
            if i > 25:
                break
