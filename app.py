import pandas as pd
import requests
from urllib.parse import urljoin
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import requests
from bs4 import BeautifulSoup
import csv
import json
import os
import json
import requests
from urllib.parse import urlparse
from mimetypes import guess_extension

# Read Excel file
excel_file_path = 'data.xlsx'  # Replace with the actual path to your Excel file
df = pd.read_excel(excel_file_path)


def download_image(url, title):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for bad responses

        # Check if the response contains image content
        content_type = response.headers.get('content-type', '')
        if content_type.startswith('image'):
            _, extension = os.path.splitext(urlparse(url).path)
            if not extension:
                # If the extension is not present in the URL, try to guess it from content type
                extension = guess_extension(content_type.split(';')[0])
            filename = f"{title.replace(' ', '-').lower()}{extension}"
            with open(filename, "wb") as file:
                file.write(response.content)
            print(f"Downloaded: {filename}")
        else:
            print(f"Skipping non-image content from {url}")

    except requests.exceptions.RequestException as e:
        print(f"Failed to download image from {url}: {e}")
        
        

for index, row in df.iterrows():
    image_name = row['name ']
    url = row['website ']

    if not pd.isna(url):  # Check for NaN values
       

        try:
            if not str(url).startswith(('http://', 'https://')):
            # Assuming the domain is part of the URL in your Excel sheet
            # If not, you might need to provide the domain separately
                domain = 'https://' + str(url)
            else:
                domain = str(url)
                    
            print(domain)
            
            page = requests.get(domain,timeout=10)
            soup = BeautifulSoup(page.text, 'html.parser')
            images = soup.find_all('img')

            i=0
            for image in images:
                image_name_=image_name
                src = image.get('src', '')
                if 'logo' in src.lower():
                    # Check if the URL is complete or not
                    if not src.startswith(('http://', 'https://')):
                        # Join the base URL with the relative URL
                        src = urljoin(domain, src)
                    if i>=1:
                        image_name_=str(image_name_)+'_'+str(i)

                    print(f"Found logo for {domain}: {src}")
                    
                    download_image(src,str(image_name_))
                    i=i+1
                    
                    
            
            
            print('-----------------------------------------')
        except Exception as e:
            print(e)