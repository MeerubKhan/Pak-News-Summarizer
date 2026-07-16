import requests
from google import genai
import os
from dotenv import load_dotenv
from bs4 import BeautifulSoup
from emailer import send_digest

load_dotenv()
client=genai.Client(api_key=os.getenv('pns-API-Key'))

url = "https://www.thenews.com.pk"
headers = {"User-Agent": "Mozilla/5.0"}  # pretend to be a browser

response=requests.get(url,headers=headers)
soup=BeautifulSoup(response.text,'html.parser')
headlines=soup.find_all(['h1','h2', 'h3'])
articles = []
for i,h in enumerate(headlines[:10],1):
    text= h.text.strip()
    #look for the a tag that has the link
    find_link=h.find('a')

     # if not found, try finding parent <a>
    if not find_link:
        find_link = h.find_parent('a')
    
    if find_link:
        link=find_link.get('href','No link')
        if link.startswith('/'):
            link = "https://www.thenews.com.pk" + link
    else:
        link='No Link Found'
    
    if text and link:  # only save if both exist
        articles.append({
            'title': text,
            'url': link
        })

    
    #print(f"{i}. {text}")
    #print(f" {link}")
    #print()

#print(f"\nTotal articles found: {len(articles)}")

def summarize(url,title):

    #fetch article
    try:
       response=requests.get(url,headers=headers, timeout=10)
       soup=BeautifulSoup(response.text,'html.parser')
    #extract article text
       paragraphs=soup.find_all('p')
       article_text = ' '.join([p.text for p in paragraphs[:10]])
    #send to Gemini
       result = client.models.generate_content(
       model = 'gemini-2.5-flash',
       contents=f"Summarize this in 2 lines:{article_text[:2000]}")

       return result.text
    except Exception as e:
       return f"Summary not available: {e}"

articles_with_summaries = []

for article in articles[:3]:
    print(f"Summarizing article: {article['title']} ... ^_^ ")
    summary=summarize(article['url'],article['title'])
    articles_with_summaries.append({
        'title': article['title'],
        'url'  : article['url'],
        'summary':summary
    })

# send email
send_digest(articles_with_summaries)
print("CI/CD Demo")



