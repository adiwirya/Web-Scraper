import requests
from bs4 import BeautifulSoup
import json
import math
import pandas as pd
import os
import unicodedata

Url ='https://store.weddingku.com/ajax/category-package.asp?url=venue-deals&page=1&txtpricemin=&txtpricemax=&txtpaxmin=&txtpaxmax=&zonaid=&rc=10&type=&sortby=&promo='
Url2 ='https://store.weddingku.com//wedding-package//venue-deal//special-all-in-package-for-200-pax-at-harmony-grand-ballroom-by-holiday-inn-suites-jakarta-gajah-mada-by-jwp-wedding'
def totalresults(url):
    response = requests.get(url)
    data = dict(response.json())
    totalpages = data['page_info']['count']['page']
    return int(totalpages)

def get_data(url):
    response = requests.get(url)
    data = dict(response.json())
    return data['html']   


def get_url(data):
    print('Parsing data...')
    paketlist = []
    soup = BeautifulSoup(data, 'lxml')
    pakets = soup.find_all('div', class_='col-xl-25 col-md-25 col-6 px-2 my-2')

    for paket in pakets:
        url = paket.find('a')['href']
        image = paket.find('div',class_='ico-bundle')
        print(image)
        if(image != None):
            mypaket ={ 
                'url': url,
                }
        else:
            mypaket ={ 
                'url': '',
                }
        
        paketlist.append(mypaket)
        # print("Done")
    return paketlist

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
            detailPaket = soup.find('label', text='INCLUSIONS').find_next('div')
        except:
            detailPaket = ''
        soup2 = BeautifulSoup(str(detailPaket), 'lxml')
        b = soup2.find_all('b')
        ul = soup2.find('ul')




        text1 = 'Master of Ceremony'
        text2 = 'Wedding Car'
        text3 = 'Photographers'
        text4 = 'Videographers'
        text5 = 'Crew'
        text6 = 'Cake'
        text7 = 'Singer'
        text8 = 'Instruments'
        text9 = 'Make Up Artist'
        text10 = 'Pax'
        text11 = 'Stage'
        text12 = 'Gate'
        text13 = 'Table Decoration'
        text14 = 'Groom'
        text15 = 'Bride'
        try:
            MC = soup2.find(lambda tag: tag.name == "li" and text1 in tag.text).text
        except:
            MC = '0'
        try:
            WD = soup2.find(text=text2).text
        except:
            WD = '0'
        try:
            PH = soup2.find(lambda tag: tag.name == "li" and text3 in tag.text).text
        except:
            PH = '0'
        try:
            VD = soup2.find(lambda tag: tag.name == "li" and text4 in tag.text).text
        except:
            VD = '0'
        try:
            C = soup2.find(lambda tag: tag.name == "li" and text5 in tag.text).text
        except:
            C = '0'
        try:
            CK = soup2.find(lambda tag: tag.name == "li" and text6 in tag.text).text
        except:
            CK = '0'
        try:
            S = soup2.find(lambda tag: tag.name == "li" and text7 in tag.text).text
        except:
            S = '0'
        try:
            Ins = soup2.find(lambda tag: tag.name == "li" and text8 in tag.text).text
        except:
            Ins = '0'
        try:
            MUA = soup2.find(lambda tag: tag.name == "li" and text9 in tag.text).text
        except:
            MUA = '0'        
        try:
            Pax = soup2.find(lambda tag: tag.name == "li" and text10 in tag.text).text
        except:
            Pax = '0'
            if(Pax == '0'):
                text10 = 'persons'
                try:
                    Pax = soup2.find(lambda tag: tag.name == "li" and text10 in tag.text).text
                except:
                    Pax = '0'
            
        try:
            WS = soup2.find(lambda tag: tag.name == "li" and text11 in tag.text).text
        except:
            WS = '0'
        try:
            WG = soup2.find(lambda tag: tag.name == "li" and text12 in tag.text).text
        except:
            WG = '0'
        try:
            BT = soup2.find(lambda tag: tag.name == "li" and text13 in tag.text).text
        except:
            BT = '0'
        try:
            G = soup2.find(lambda tag: tag.name == "span" and text14 in tag.text).text
        except:
            G = '0'
        try:
            B = soup2.find(lambda tag: tag.name == "span" and text15 in tag.text).text
        except:
            B = '0'
        


        
        print("{namaPaket}\n---------------------------\nMC = {MC}\nCar = {WD}\nPhoto = {PH}\nVideo = {VD}\nCrew = {C}\nCake = {CK}\nSing = {S}\nIns = {Ins}\nMUA = {MUA}\nPax = {Pax}\n---------------------------\n".format(MC=MC,WD=WD,PH=PH,VD=VD,C=C,CK=CK,S=S,Ins=Ins,MUA=MUA,namaPaket=namaPaket,Pax=Pax))
        # bs =  detailPaket.find_all('b')

        # for i in range(len(bs)):
        #     b = detailPaket.find('b')
        #     ul = detailPaket.find('ul')
           
                        
            # nData = unicodedata.normalize('NFKD', str(bs[i].text)).encode('ASCII', 'ignore')
            # bs[i] = nData.decode('utf-8')
        
        # for i in range(len(uls)):
        #     nData = unicodedata.normalize('NFKD', str(uls[i].text)).encode('ASCII', 'ignore')
        #     uls[i] = nData.decode('utf-8')
        
        
        detailPaket = detailPaket.text.strip()
        mypaket = {
            'url': url,
            'namaPaket': namaPaket,
            'totalHarga': totalHarga,
            'venueType': venueType,
            'lokasi': lokasi,
            'jumlahTamu': jumlahTamu,
            'image': image,
            'MC':MC,
            'Wedding Car':WD,
            'Photographers':PH,
            'Videographers':VD,
            'Crew':C,
            'Cake':CK,
            'Singer':S,
            'Ins':Ins,
            'MUA':MUA,
            'Pax':Pax,
            'Wedding Stage' : WS,
            'Wedding Gate' : WG,
            'Bridal Table Decoration' : BT,
            'Groom' : G,
            'Bride' : B,
            'detailPaket':detailPaket,
        }

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
            'MC':'',
            'Wedding Car':'',
            'Photographers':'',
            'Videographers':'',
            'Crew':'',
            'Cake':'',
            'Singer':'',
            'Ins':'',
            'MUA':'',
            'Pax':'',
            'Wedding Stage' : '',
            'Wedding Gate' : '',
            'Bridal Table Decoration' : '',
            'Groom' : '',
            'Bride' : '',
            'detailPaket': ''
        }
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

