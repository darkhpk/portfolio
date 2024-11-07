import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

def save_file(url, folder):
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()
        
        # Create local file path
        parsed_url = urlparse(url)
        file_path = os.path.join(folder, os.path.basename(parsed_url.path))
        
        # Write file to local path
        with open(file_path, 'wb') as file:
            for chunk in response.iter_content(1024):
                file.write(chunk)
        
        return file_path
    except requests.RequestException as e:
        print(f"Failed to download {url}: {e}")
        return None

def clone_webpage(url, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    # Download the HTML content
    response = requests.get(url)
    response.raise_for_status()
    html_content = response.text
    
    # Parse the HTML
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Find and download all resources
    for tag in soup.find_all(['img', 'link', 'script']):
        src = None
        attr = None
        
        if tag.name == 'img':
            attr = 'src'
        elif tag.name == 'link' and tag.get('rel') == ['stylesheet']:
            attr = 'href'
        elif tag.name == 'script' and tag.get('src'):
            attr = 'src'
        
        if attr:
            src = tag.get(attr)
        
        if src:
            resource_url = urljoin(url, src)
            local_path = save_file(resource_url, output_folder)
            
            if local_path:
                tag[attr] = os.path.basename(local_path)
    
    # Save modified HTML to local file
    with open(os.path.join(output_folder, 'index.html'), 'w', encoding='utf-8') as file:
        file.write(str(soup))

    print(f"Webpage cloned successfully into '{output_folder}' folder.")

# Example usage
clone_webpage('https://www.facebook.com/?locale=en_GB', 'cloned_webpage')
