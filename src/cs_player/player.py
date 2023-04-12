from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
import re

class player():

    def __init__(self, player_name):
        self.player_name = player_name
        self.url = 'https://liquipedia.net/counterstrike/' + player_name

        req = Request(self.url)
        html_page = urlopen(req)
        self.soup = BeautifulSoup(html_page, "lxml")

    def get_player_info(self):  
        return self.soup.findAll('p')[0]

    def get_links(self):
        pass
    
    def get_history(self):
        pass
    
    def get_achieve(self):
        pass

    def get_player_name(self):
        return self.player_name
    
    def get_url(self):
        return self.url