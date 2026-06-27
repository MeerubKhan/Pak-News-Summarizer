# Pak-News-Summarizer
An automated Python tool that scrapes top headlines from  Pakistani news sources (The News, Dawn) and uses AI to  generate concise 2-line summaries — delivered daily via email or whatsApp.
## What it does
- Scrapes real-time headlines from major Pakistani news websites
- Extracts article content using BeautifulSoup
- Summarizes each article using Google Gemini AI API
- Sends a clean formatted digest to subscribers every morning
- Runs automatically on a schedule — no human intervention needed

## Tech Stack
Python | BeautifulSoup | Requests | Gemini API | 
Flask | SQLite | APScheduler | SMTP | Docker

**Description of Important libraries used here**
**1.Dotenv**
dotenv is a popular developer library that loads environment variables from a configuration file into an application. 
It acts as a bridge, reading key-value pairs from a .env file (stored in your project's root) and making them available
in your code as actual environment variables.

**2.BeautifulSoup**
Beautiful Soup (often called BS4) is a popular Python library used for web scraping and parsing HTML and XML files.
It takes raw, messy webpage data and translates it into a structured, easily navigable object, allowing developers 
to quickly extract specific information like text, links, and tables.

**3.smtplib**
is a built-in Python module that allows you to send emails programmatically from your applications. It implements the Simple Mail Transfer Protocol (SMTP), letting your code connect to a mail server, authenticate, and route messages across the internet.

**4.SSL/TSL**
SSL (Secure Sockets Layer) is the standard security technology for establishing an encrypted link between a web server and a browser. It ensures that all data passed between the two remains private and safe from interception.While the term "SSL" is still widely used, the actual technology protecting modern websites is TLS (Transport Layer Security), which is simply a more secure and updated version of SSL.


## What I learned building this

**DAY-01 TASKS AND LEARNINGS**

**Web Scraping with BeautifulSoup**
You learned how to send an HTTP request to a real website and parse its HTML. This is how data is extracted from the internet without an official API — a skill used daily in data engineering, automation, and research roles.

---

**HTML Structure Reading**

You learned to use browser DevTools (right click → Inspect) to find exactly which HTML tags and classes contain the data you want. This is a fundamental skill — every web scraper starts here.

---

**CSS Class Selectors**

You used `soup.find_all('a', class_='story__link')` and `soup.find_all(['h1', 'h2', 'h3'])` — selecting elements by tag name and class, the same way CSS and JavaScript work.

---

**Navigating HTML Tree — two directions**

This was the most important concept today:

```
find('a')         → looks INSIDE the element (downward)
find_parent('a')  → looks ABOVE the element (upward)
```

Real websites have inconsistent structures — some put links inside headings, some wrap headings in links. You learned to handle both cases.

---

**Safe attribute access**

```python
h.get('href', 'No link')  # safe — never crashes
h['href']                  # unsafe — crashes if href missing
```

Using `.get()` with a default value is proper Python — you'll use this pattern everywhere.

---

**Storing structured data**

You moved from just printing results to storing them properly:

```python
articles.append({
    'title': text,
    'url': link
})
```

This dictionary-in-a-list pattern is how data flows through real applications — scraper → storage → AI → email.

---

**Variable naming bug**

You caught and understood a classic mistake — using the same variable name for both a list and a loop variable:

```python
headlines = soup.find_all(...)
for i, headlines in enumerate(...):  # ❌ overwrote the list
```
**Naming things properly matters. You won't make this mistake again.
**---

**DAY-02 TASKS AND LEARNINGS**

**VENV built**
I built a new venv

1.open python interpretar

2.create new environment

3.and than install all the libraries
pip install requests beautifulsoup4 google-genai python-dotenv

4.venv is cretaed for that project SEPERATELY


Take your `articles` list → fetch each article page → extract the article body text → send to Gemini API → get a 2-line summary back.

**Today's plan — the AI summarization step:**

**Step 1 — Get Gemini API key**

Go to **aistudio.google.com** → Sign in with Google → create a new project just put it's name  → Get API key → Copy it → Add to your `.env` file:
```
GEMINI_API_KEY=your_key_here
```

**Step 2 — Install the library:**
```
pip install google-genai
```

**Step 3 — Test Gemini first (separate file `test_gemini.py`):**

```python
from google import genai
import os
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("gemini-2.5-flash")  
response = model.generate_content("Summarize this in 2 lines: Pakistan's economy grew by 3% this year according to the State Bank.")
print(response.text)
```

Run this first — confirm Gemini works before touching your scraper.

**ERROR**
while doing this step I faced this error: 
I used this library **pip install google-generativeai**
However this is an old version it needs to be replaced with **python -m pip install google-genai**
In modern SDK(An SDK, or Software Development Kit, is a comprehensive toolkit that provides developers with the necessary resources, libraries, and documentation to build applications for a specific platform or system. It acts as a pre-built foundation so programmers do not have to write every piece of code from scratch) this is used.

**Step 4 — Add summarization to scraper.py:**

Once Gemini test works, add this function:
This part works like this go to the article of url -> send to gemini -> summarized
```python
def summarize(title, url):
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
```

**Step 5 — Connect to your articles list:**

```python
for article in articles[:3]:
    print(f"title:{article['title']}")
    Summary=summarize(article['url'],article['title'])
    print(f"Summary:{Summary}")
    print(f"Link:{article['url']}")
    print("-" * 50)
```
**DAY-03 TASKS AND LEARNINGS**

**Step 1** — Get Gmail App Password (10 mins)
You can't use your regular Gmail password in code — Google blocks it for security. You need an "App Password":

Go to myaccount.google.com →
Click Security →
Enable 2-Step Verification if not already on →
Search "App passwords" in the search bar →
Create one → name it news-summarizer →
Copy the 16-character password it gives you

Add to your .env file:
GMAIL_PASSWORD
GMAIL_USER=meerub.sk@gmail.com

1.The email body is made by making an email body function and after that use the loop to access articles_with_summaries list and in that list use **'email_body+='**

**DAY_04**
The projects gets built .... everything's done. 
**Automation will be done after docker image is built**
Docker steps:
Step 1: Create a requirements.txt file
pip freeze > requirements.txt
Step 2: Create your Dockerfile
