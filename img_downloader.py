# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
from PIL import Image
from io import BytesIO


SOURCE_FILE = 'source.txt'
HISTORY_FILE = 'history.txt'
IMG_FILE_EXTENSION = ['jpg', 'png', 'jpeg']
TARGET_FOLDER = './test/'
HISTORY = []

def get_all_image_link(page, history_file):
    """
    input: a ptt page url
    return a list contain all image's link that not in history.
    """
    hrefs = []
    html_doc = requests.get(page).text
    soup = BeautifulSoup(html_doc, 'html.parser')
    
    for link in soup.find_all('a'):
        href = link.get('href')
        # skip if the image has been downloaded
        # detect href end with image file extention
        if href not in HISTORY:
            if href[-3:] in IMG_FILE_EXTENSION:
                hrefs.append(href)
                history_file.write(href + '\n')
        else:
            print('image already exist: ' + href)
    return hrefs

def generate_output_file_name(url, counter, history_length):
    """
    example: 0001 - fOo7BAr.jpg
    """
    serial = str(history_length + counter).zfill(4)
    name = url.split('/')[-1]
    return TARGET_FOLDER + serial + ' - ' + name
    
def download_image(url, counter, history_length):
    output_location = generate_output_file_name(url, counter, history_length)
    html_doc = requests.get(url)
    Image.open(BytesIO(html_doc.content)).convert('RGB').save(output_location)
    
def main():
    
    source_file = open(SOURCE_FILE)
    history_file = open(HISTORY_FILE)
    counter = 1 # 檔名編號，維持組圖/短漫順序
    
    # 取出所有下載過的圖片的連結
    for link in history_file:
        if link[0].strip() != '#':
            HISTORY.append(link.strip())
    history_file.close()
    
    # 用來算新圖的起始編號
    history_length = len(HISTORY)
    
    history_file = open(HISTORY_FILE, 'a')
    
    # 從每個ptt網頁好讀版中取出連結
    for ptt_page in source_file:
        # skip comment line
        if ptt_page.strip()[0] != '#':
            image_hrefs = get_all_image_link(ptt_page.strip(), history_file)
        else:
            continue
        # 下載連結圖片並儲存在電腦內
        for image_href in image_hrefs:
            download_image(image_href, counter, history_length)
            counter += 1
    
    source_file.close()
    history_file.close()
    
main()
