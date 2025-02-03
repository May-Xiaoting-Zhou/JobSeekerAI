import requests
from bs4 import BeautifulSoup

def scrape_jobs():
    url = "https://www.example-jobs.com"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    jobs = []
    for item in soup.select('.job-listing'):
        jobs.append({
            'title': item.select_one('.title').text,
            'company': item.select_one('.company').text,
            'description': item.select_one('.desc').text
        })
    return jobs