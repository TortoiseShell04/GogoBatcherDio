import requests
from bs4 import BeautifulSoup as bs
import os

# Defines Number of Episodes
numOfEps= int(input("How many episodes?: "))
eps = list(range(1,numOfEps+1))

# This function logs in and fetches each download link indiviually
def LoginAndGoToLink(eps):
    # Array of links to be downloaded
    Links = []

    # Loops for all episodes
    for ep in eps:
        # Episode link can be changed
        link = f"https://www1.gogoanime.bid/tokyo-revengers-seiya-kessen-hen-episode-{ep}"
        # Login page link
        linkLogin = "https://www1.gogoanime.bid/login.html"

        # Requests session to start handshake
        s = requests.session()
        # Gets the html data
        text = s.get(linkLogin).text
        # Sorts the data to be usable
        so = bs(text, "lxml")
        # Looks for CSRF token
        for i in so.find_all("meta"):
            if i.get("name") == "csrf-token":
                csrftoken = i.get("content")

        # Dictionary for storing user data add your email and password 
        login_data = dict(email='emailsGoesHere', password='passwordGoesHere', _csrf=csrftoken, next='/')

        # Logs in using the data
        s.post(linkLogin,data=login_data, headers=dict(Referer=linkLogin))

        # Gets html data of the episode page
        html_page= s.get(link).text
        # Sorts html data
        soup = bs(html_page, "lxml")

        # Finds download links
        for link in soup.find_all("a"):
            # You can set the resloution from '360, 480, 720, 1080'
            if "480" in format(link.text):
                x = link.get("href")
                Links.append(x) 
    # Returns Links array to other functions
    return Links

# Downloading function, takes Links array as a parameter
def WGetTheFiles(Links):
    for Link in Links:
        # Downloads each file
        os.system(f"wget -O EP{Links.index(Link) + 1}.mp4 {Link}")

WGetTheFiles(LoginAndGoToLink(eps))

# ENJOY
