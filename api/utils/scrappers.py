from dotenv import load_dotenv
import os
from bs4 import BeautifulSoup
import requests
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import re

load_dotenv()

def get_lyrics(song_title: str="", artist: str="") -> str:

    try:
        base_url = os.environ.get("LYRICS_BASE_URL")
        cleaned_title = re.sub(r'[^\w\s]','',song_title).lower().replace(" ","")
        artist = artist.replace(" ", "").lower()
        url = f"{base_url}{artist}/{cleaned_title}.html"
        page = requests.get(url)
        soup = BeautifulSoup(page.text, 'html.parser')
        lyrics = " ".join([line for line in soup.find_all(class_="row")[1].find_all("div")[2].find_all("div")[5].get_text().split("\n") if len(line) > 0 and (len(line) < 3 or (line[0] != "[" and line[-2:] != ":]"))])
        
        stop_words = set(stopwords.words('english'))
        word_tokens = word_tokenize(lyrics)
        
        cleaned_lyrics = [w.lower() for w in word_tokens if not w.lower() in stop_words and w.isalnum()]
    except:
        return None
    return " ".join(cleaned_lyrics)

print(get_lyrics("Father Stretch My Hands Pt. 1", "kanye west"))