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
        return self.soup.findAll('p')[0].get_text()

    def get_player_infobox(self):
        pass

    def get_links(self):
        div = self.soup.find("div", {"class": "infobox-center infobox-icons"})
        links = div.find_all('a')
        links_text = []

        for link in links:
            links_text.append(link['href'])
        return links_text
    
    def get_history(self):
        hist = self.soup.find_all("div", {"class": "infobox-center"})
        hist_div = hist[1].find_all("div")
        team_history = []
        for i in range(0, len(hist_div), 4):
            team_history.append(hist_div[i].get_text())

        return team_history
    
    def get_achieve(self):
        table = self.soup.find("table", {"class" : "wikitable wikitable-striped sortable"}).find("tbody").find_all("tr")
        achieve = []
        for i in range(1, len(table)-1):
            data = table[i].find_all("td")
            date = data[0].get_text()
            place = data[1].get_text()
            tourney_type = data[3].get_text()
            tourney_name = data[6].get_text()
            team_name = data[7].find("span")['data-highlightingclass']
            score = data[8].get_text()
            score = score.replace(u'\xa0', u' ')
            try:
                opposing = data[9].find("span")['data-highlightingclass']
            except:
                opposing = data[9].find("abbr")['title']

            prize = data[10].get_text()
    
            achieve.append([date, place, tourney_type, tourney_name, team_name, score, opposing, prize])

        return achieve





    def get_player_name(self):
        return self.player_name
    
    def get_url(self):
        return self.url