from dotenv import load_dotenv
import os
from bs4 import BeautifulSoup
import requests
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import nltk

nltk.download('stopwords')
nltk.download('punkt')

load_dotenv()

def clean_text(text: str) -> str:
    stop_words = set(stopwords.words('english'))
    word_tokens = word_tokenize(text)

    cleaned_words = [w.lower() for w in word_tokens if not w.lower() in stop_words and w.isalnum()]

    return " ".join(cleaned_words)

def get_lyrics(song_title: str="", artist: str="") -> str:

    base_url = os.environ.get("LYRICS_BASE_URL")
    song_title = song_title.replace(" ", "").lower()
    artist = artist.replace(" ", "").lower()
    url = f"{base_url}{artist}/{song_title}.html"
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'html.parser')

    try:
        lyrics = " ".join([line for line in soup.find_all(class_="row")[1].find_all("div")[2].find_all("div")[5].get_text().split("\n") if len(line) > 0 and (len(line) < 3 or (line[0] != "[" and line[-2:] != ":]"))])
    except:
        # just give up
        return ""
    
    cleaned_lyrics = clean_text(lyrics)
    
    return cleaned_lyrics

