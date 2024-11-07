import os
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from urllib.parse import urljoin, urlparse

def download_image(image_url, folder):
    try:
        response = requests.get(image_url, stream=True)
        response.raise_for_status()

        # Create local file path
        parsed_url = urlparse(image_url)
        filename = os.path.basename(parsed_url.path)
        file_path = os.path.join(folder, filename)

        # Save the image to the local file path
        with open(file_path, 'wb') as file:
            for chunk in response.iter_content(1024):
                file.write(chunk)

        print(f"Downloaded {image_url} to {file_path}")
    except requests.RequestException as e:
        print(f"Failed to download {image_url}: {e}")

def download_all_images(url, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Setup Selenium WebDriver
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Ensure GUI is off
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-web-security")
    chrome_options.add_argument("--allow-running-insecure-content")
    driver = webdriver.Chrome(options=chrome_options)

    # Open the webpage
    driver.get(url)

    ch = driver.find_elements(By.CLASS_NAME, "wp-manga-chapter")
    
        

    # Wait for images to load
    WebDriverWait(driver, 100).until(
        EC.presence_of_all_elements_located((By.CLASS_NAME, 'page-break'))
    )

    # Get the page source after JavaScript execution
    html_content = driver.page_source

    # Close the browser
    driver.quit()

    # Parse the HTML with BeautifulSoup
    soup = BeautifulSoup(html_content, 'html.parser')

    # Find all image tags
    img_tags = soup.find_all('img')

    # Download each image
    for img in img_tags:
        img_url = img.get('src') or img.get('data-src') or img.get('srcset')
        if img_url:
            # Ensure the URL is absolute
            img_url = urljoin(url, img_url.split()[0])
            download_image(img_url, output_folder)

    # Find background images in inline styles
    for div in soup.find_all(style=True):
        style = div['style']
        if 'background-image' in style:
            img_url = style.split('url(')[-1].split(')')[0].strip('\'"')
            if img_url:
                img_url = urljoin(url, img_url)
                download_image(img_url, output_folder)

def chapters(url, title, nr_img):
    for i in range(1,nr_img):
        url_all = f"{url}/chapter-{i}"
        output_folder = f"downloaded_images\{title}\chapter-{i}"
        download_all_images(url_all, output_folder)

url = input("Enter the URL of the webpage: ")
title = url.split("/")[-2]
print(title)
chapters(url, title, 378)