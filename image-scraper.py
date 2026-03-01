import requests
import os
import time
from PIL import Image
from urllib.parse import unquote
from time import sleep
from dotenv import load_dotenv

load_dotenv()

header = {'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:147.0) Gecko/20100101 Firefox/147.0"}

session = requests.session()
session.headers.update(header)


#Cleans obfuscated url
def clean(url):
    split_url = url.split('url=')[1].split('&')[0]
    new_url = unquote(split_url)
    return new_url


def resize(img_path,H,W):
    
    
        
        for i in os.listdir(img_path):
            
            try:
                path = os.path.join(img_path,i)
                img = Image.open(path)
                if img.mode in ("RGBA",'P'):
                    img = img.convert('RGB')
                if (img.size == ((H,W))):
                    print("Resize already done")
                    continue
                res = img.resize((H,W))
                
                res.save(path)
                print(f'{i} has been resized to {H},{W}')
            except Image.DecompressionBombError:
                print("File too large")
                os.remove(path)
        
def resize(img_path,H,W,tag):
    for i in os.listdir(img_path):
            
        try:
            path = os.path.join(img_path,i)
            img = Image.open(path)
            if img.mode in ("RGBA",'P'):
                img = img.convert('RGB')
            if (img.size == ((H,W))):
                print("Resize already done")
                continue
            res = img.resize((H,W))
            path = os.path.join(img_path,i)
            filename = tag + i
            new_path = os.path.join(img_path, filename)
            res.save(new_path)
            os.remove(path)
            print(f'{i} has been resized to {H},{W}')
        except Image.DecompressionBombError:
            print("File too large")
            os.remove(new_path)

#Less used as quality of images is lower.
def promptHero(y,tag,save_path):
    for num in range(1,y):
        url = 'https://prompthero.com/api/trpc/prompt.search?batch=1&input={"0":{"json":{"query":null,"searchMode":null,"page":CHANGE,"pageSize":24,"sort":"favorites","model":null,"modelVersion":null,"type":"image","timeRange":null,"nsfw":false,"featured":null,"category":"photography"},"meta":{"values":{"query":["undefined"],"searchMode":["undefined"],"model":["undefined"],"modelVersion":["undefined"],"timeRange":["undefined"],"featured":["undefined"]},"v":1}}}'
        url = url.replace("CHANGE",str(num))

        r = session.get(url)
        data = r.json()
        search_results = data[0]['result']['data']['json']['items']
        
        for item in search_results:
            asset = item.get('asset')
            image_url = asset.get('url') + '.png'
            filename = tag + image_url.split('/')[-1]
            image = session.get(image_url, headers=header)
            folder_name = save_path

            if image.status_code != 200:
                print("Error getting {}".format(filename))
            else:
                path = os.path.join(folder_name, filename)
                if not os.path.exists(folder_name):
                    os.makedirs(folder_name)
                    
                if (os.path.isfile(path)):
                    print("Exists")
                else:
                    with open(path, 'wb') as f:
                        f.write(image.content)
                        print('Save {}'.format(filename))


#Pulls 50 per page                        
def civit(y,save_path):
    
    url = "https://civitai.com/api/v1/images?limit=50&sort=Most%20Reactions&nsfw=Soft&tags=4"

    
    for i in range(y):
        r = session.get(url)
        print(f"DEBUG: Status is {r.status_code}")
  
        if r.status_code != 200:
            print("Error Retrieving")
        else:
            data = r.json()
            json = data.get('items', [])
            
            for img in json:
                url = img.get('url')
                filename = url.split('/')[-1]
                folder_name = save_path
                path = os.path.join(folder_name, filename)
                image = session.get(url, headers=header)
                
            
                
                if not os.path.exists(folder_name):
                    os.makedirs(folder_name)
                    
                if (os.path.isfile(path)):
                    print("Exists")
                    
                elif(filename.split('.')[1] == 'mp4'):
                    print("MP4 found")
                    
                else:
                    with open(path, 'wb') as f:
                        f.write(image.content)
                        print('Save {}'.format(filename))
        url = data.get('metadata', {}).get('nextPage')
        time.sleep(1.5)
        
def civit(y,save_path,tag):
    
    url = "https://civitai.com/api/v1/images?limit=50&sort=Most%20Reactions&nsfw=Soft&tags=4"

    
    for i in range(y):
        r = session.get(url)
        print(f"DEBUG: Status is {r.status_code}")
  
        if r.status_code != 200:
            print("Error Retrieving")
        else:
            data = r.json()
            json = data.get('items', [])
            
            for img in json:
                url = img.get('url')
                filename = tag + url.split('/')[-1]
                folder_name = save_path
                path = os.path.join(tag, folder_name, filename)
                image = session.get(url, headers=header)
                
            
                
                if not os.path.exists(folder_name):
                    os.makedirs(folder_name)
                    
                if (os.path.isfile(path)):
                    print("Exists")
                    
                elif(filename.split('.')[1] == 'mp4'):
                    print("MP4 found")
                    
                else:
                    with open(path, 'wb') as f:
                        f.write(image.content)
                        print('Save {}'.format(filename))
        url = data.get('metadata', {}).get('nextPage')
        time.sleep(1.5)



#Pulls 100 items per page
def safebooru(page, save_path):
    page_num = 1
    url = f'https://safebooru.org/index.php?page=dapi&s=post&q=index&json=1&pid={page_num}'

    for i in range(page):
        r = session.get(url)
        print(r.status_code)

        if r.status_code != 200:
            print("Error Retrieving")
        else:
            data = r.json()

            for img in data:
                img_url = img.get('file_url')
                filename = img_url.split('/')[-1]
                folder_name = save_path
                path = os.path.join(folder_name, filename)
                image = session.get(img_url, headers=header)

                if not os.path.exists(folder_name):
                    os.makedirs(folder_name)
                    
                if (os.path.isfile(path)):
                    print("Exists")
                    
                elif(filename.split('.')[1] == 'mp4' or filename.split('.')[1] == 'gif'):
                    print("Incorrect Filetype")
                    
                else:
                    with open(path, 'wb') as f:
                        f.write(image.content)
                        print('Save {}'.format(filename))
        page_num = page_num+1                
        url = f'https://safebooru.org/index.php?page=dapi&s=post&q=index&json=1&pid={page_num}'
        print(f"Page {page_num} downloaded")
        time.sleep(1.5)
        
def safebooru(page, save_path, tag):
    page_num = 1
    url = f'https://safebooru.org/index.php?page=dapi&s=post&q=index&json=1&pid={page_num}'

    for i in range(page):
        r = session.get(url)
        print(r.status_code)

        if r.status_code != 200:
            print("Error Retrieving")
        else:
            data = r.json()

            for img in data:
                img_url = img.get('file_url')
                filename = tag + img_url.split('/')[-1]
                folder_name = save_path
                path = os.path.join(folder_name, filename)
                image = session.get(img_url, headers=header)

                if not os.path.exists(folder_name):
                    os.makedirs(folder_name)
                    
                if (os.path.isfile(path)):
                    print("Exists")
                    
                elif(filename.split('.')[1] == 'mp4' or filename.split('.')[1] == 'gif'):
                    print("Incorrect Filetype")
                    
                else:
                    with open(path, 'wb') as f:
                        f.write(image.content)
                        print('Save {}'.format(filename))
        page_num = page_num+1                
        url = f'https://safebooru.org/index.php?page=dapi&s=post&q=index&json=1&pid={page_num}'
        print(f"Page {page_num} downloaded")
        time.sleep(1.5)
        
        
def pexels(page, save_path, tag, query):
    page_num = 1
    
    api_key = os.getenv("PEXELS_API_KEY")
    
    if not api_key:
        print("Error: PEXELS_API_KEY not found in environment variables.")
        return
    
    url = f'https://api.pexels.com/v1/search?query={query}&per_page=80'
    
    header = {
        
        "Authorization": api_key
    }
    
    session = requests.session()
    session.headers.update(header)


    for i in range(page):
        r = session.get(url)
        print(r.status_code)

        if r.status_code != 200:
            print("Error Retrieving")
        else:
            data = r.json()
            json = data.get('photos', [])

            for img in json:
                img_url = img.get('src', {}).get('original')
                filename = tag + img_url.split('/')[-1]
                folder_name = save_path
                path = os.path.join(folder_name, filename)
                image = session.get(img_url, headers=header)

                if not os.path.exists(folder_name):
                    os.makedirs(folder_name)
                    
                if (os.path.isfile(path)):
                    print("Exists")
                    
                elif(filename.split('.')[1] == 'mp4' or filename.split('.')[1] == 'gif'):
                    print("Incorrect Filetype")
                    
                else:
                    with open(path, 'wb') as f:
                        f.write(image.content)
                        print('Save {}'.format(filename))
        page_num = page_num+1                
        url = f'https://api.pexels.com/v1/search?query={query}&per_page=80&page={page_num}'
        print(f"Page {page_num} downloaded")
        time.sleep(1.5)
    

        
    