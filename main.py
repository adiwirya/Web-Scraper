import requests
from bs4 import BeautifulSoup
import json
import math
import pandas as pd
import os

Url ='https://store.weddingku.com/ajax/category-package.asp?url=venue-deals&page=1&txtpricemin=&txtpricemax=&txtpaxmin=&txtpaxmax=&zonaid=&rc=10&type=&sortby=&promo='
Url2 ='https://store.weddingku.com/wedding-package/venue-deal/wedding-2022-for-150-pax-at-grand-ballroom-jw-marriott-by-pinkbow'
def totalresults(url):
    response = requests.get(url)
    data = dict(response.json())
    totalpages = data['page_info']['count']['page']
    return int(totalpages)

def get_data(url):
    response = requests.get(url)
    data = dict(response.json())
    return data['html']   


def parse(data):
    print('Parsing data...')
    paketlist = []
    soup = BeautifulSoup(data, 'lxml')
    pakets = soup.find_all('div', class_='col-xl-25 col-md-25 col-6 px-2 my-2')

    for paket in pakets:
        url = paket.find('a')['href']
        mypaket = get_data_detail(url)
        paketlist.append(mypaket)
    
    print("Done")
    return paketlist

def output(results):
    print('Generating output...')
    df = pd.concat([pd.DataFrame(g) for g in results]) 
    df.to_csv('wedding.csv', index=False)
    df.to_json('wedding.json', orient='records')
    print("Done")
    # print(df.head())
    return

def get_data_detail(url):
    response = requests.get(url).text
    soup = BeautifulSoup(response, 'lxml')
    try:
        image = soup.find('div',class_='ico-bundle').find_next_sibling('img')['src']
    except:
        image = ''
    if (image != ''):
        image = os.path.basename(image)
        image = "https://images.weddingku.com/images/upload/store/product/big/" + image
        try:   
            namaPaket = soup.find('h1', class_='mb-3').text.strip()
        except:
            namaPaket = ''
        try:
            totalHarga = soup.find('h3', class_='price').text.split('IDR')[1]
        except:
            totalHarga = ''
        totalHarga = int(totalHarga.replace('.', ''))
        try:
            venueType = soup.find("dt", text="Venue Type").find_next_sibling("dd").text.strip()
        except:
            venueType = ''
        try:
            lokasi = soup.find('label', text='SERVICE AREA').find_next('div').text.strip()
        except:
            lokasi = ''
        try:
            jumlahTamu = soup.find('label', text='PACKAGE PAX').find_next('strong').text.strip()
        except:
            jumlahTamu = ''
        try:
            detailPaket = soup.find('label', text='INCLUSIONS').find_next('div').text.strip()
        except:
            detailPaket = ''
        mypaket = {
            'url': url,
            'namaPaket': namaPaket,
            'totalHarga': totalHarga,
            'venueType': venueType,
            'lokasi': lokasi,
            'jumlahTamu': jumlahTamu,
            'image': image,
            'detailPaket': detailPaket
        }
        print(mypaket)
        return mypaket
    else:
        mypaket = {
            'url': '',
            'namaPaket': '',
            'totalHarga': '',
            'venueType': '',
            'lokasi': '',
            'jumlahTamu': '',
            'image': '',
            'detailPaket': ''
        }
        print(mypaket)
        return mypaket

# get_data_detail(Url2)

    
results = []
last = totalresults(Url)
print("Scraping data...")

for i in range(1,last+1):
    print('{i} / {last}'.format(i=i, last=last)) 
    data = get_data(f'https://store.weddingku.com/ajax/category-package.asp?url=venue-deals&page={i}&txtpricemin=&txtpricemax=&txtpaxmin=&txtpaxmax=&zonaid=&rc=10&type=&sortby=&promo=')
    results.append(parse(data))

output(results)

