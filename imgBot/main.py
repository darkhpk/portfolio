import os
import requests
import argparse
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from urllib.parse import urljoin, urlparse
from concurrent.futures import ThreadPoolExecutor

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

        print(f"Downloaded {file_path}")
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
    print("Start iterable download")
    time.sleep(1)
    for i in range(1,nr_img):
        url_all = f"{url}/chapter-{i}"
        output_folder = f"downloaded_images/{title}/chapter-{i}"
        download_all_images(url_all, output_folder)

def th_chapter(url, title, nr_img):
    print(f"Starting download on chapter-{nr_img}")
    time.sleep(1)
    url_img = f"{url}/chapter-{nr_img}"
    output_folder = f"downloaded_images/{title}/chapter-{nr_img}"
    download_all_images(url_img, output_folder)
    print(f"Done download on chapter-{nr_img}")

def multi_thread(url, title, nr_img):
    print("Start threaded function..")
    time.sleep(1)
    list_chapter = []
    for i in range(1, nr_img+1):
        list_chapter.append(i)
    with ThreadPoolExecutor() as executor:
        executor.map(th_chapter, [url]*nr_img, [title]*nr_img, list_chapter)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="Image Downloader",
        description="Help Download mangas from websites with simple URL examples: https://domain.com/title/chapter-[nr]"
    )
    parser.add_argument("url")
    parser.add_argument("-n", "--number", help="Add number of chapter the manga has!")
    parser.add_argument("-t", "--thread", action="store_true", help="Turn multithreading on or off")
    args = parser.parse_args()
    url = args.url
    ch_nr = args.number
    title = url.split("/")[-2]
    if args.thread == True:
        multi_thread(url, title, int(ch_nr))
    else:
        chapters(url, title, ch_nr)
    print(title, ch_nr)
    