import pandas as pd
import urllib.request

def url_to_jpg(i, url, filename):
    
    filename ='image-{}.jpeg'.format(i)
    full_path = FILE_PATH + filename
    urllib.request.urlretrieve(url, full_path)

    print('Downloaded {}'.format(filename))

    return None

FILENAME = 'url.json'
FILE_PATH = 'images/'

urls = pd.read_json(FILENAME)
df = pd.DataFrame(urls)
print(df.loc[0][6])

for i, url in enumerate(urls['image']):
    url_to_jpg(i, url, FILE_PATH)
