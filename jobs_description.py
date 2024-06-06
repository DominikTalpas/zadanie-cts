import requests
from bs4 import BeautifulSoup
import os

url = "https://www.cts-tradeit.cz/kariera/"
script_dir = os.path.dirname(os.path.abspath(__file__))

response = requests.get(url)
if response.status_code == 200:
    main_page_content = response.text
    
    soup = BeautifulSoup(main_page_content, 'html.parser')
    
    job_links = []
    for a in soup.find_all('a', href=True):
        href = a['href']
        if '/kariera/' in href:
            full_link = "https://www.cts-tradeit.cz" + href
            job_links.append(full_link)

    for job_link in job_links:
        job_response = requests.get(job_link)
        if job_response.status_code == 200:
            job_page_content = job_response.text
            
            job_soup = BeautifulSoup(job_page_content, 'html.parser')
           
            job_title = job_link.rstrip('/').split('/')[-1]
           
            section = job_soup.find('h2', string="Co Tě u nás čeká?")
            
            if section:
                element_ul = section.find_next('ul')
                text_ul = element_ul.get_text(separator=' ', strip=True) 

                element_p = section.find_all_next()
                text_p = []
                for elem in element_p:
                    if elem.name == 'ul':
                        break
                    if elem.name == 'p':
                        text_p.append(elem.get_text(separator=' ', strip=True))
                text_p = ' '.join(text_p)        
                
                description = f"{text_p} {text_ul}".strip()

                file_name = os.path.join(script_dir, f"{job_title}.txt")
                with open(file_name, 'w', encoding="utf-8") as f:
                    f.write(f"Co Tě u nás čeká? {description}")
           
    print(f"Job details have been saved in the directory.")
else:
    print(f"Failed to fetch the main page. Status code: {response.status_code}")
