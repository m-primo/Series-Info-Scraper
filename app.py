# Series-Info-Scraper
# app.py
# Get a tv series information from IMDb or Rotten Tomatoes.
# (C) 2021 Primo. BSD-2-Clause License. (https://github.com/m-primo/Series-Info-Scraper)
# ==============================> Include <==============================
import sys
import json
import requests
from bs4 import BeautifulSoup
from pprint import pprint
# ==============================> Core <==============================
WATCHLIST_FILE = "watchlist.json"
def ViewSeriesInformation(title, id_, rate, last_aired_season, episodes):
    print("")
    print("===> TV Series Information <===")
    print("[>] Title:", title)
    print("[>] ID:", id_)
    print("[>] Rate:", rate)
    print("[>] Last Aired Season:", last_aired_season)
    print("[>] Episodes Information:")
    pprint(episodes)
    print("")
def ViewSeriesCatchedInfo(title, id_):
    print("[+] Found. Series:",title,"- ID:",id_)
    print("[*] Please wait while getting the rest of the information...")
    print("")
# ==============================> Classes <==============================
class Object(object):
    pass
class JSONfile():
    def __init__(self, filename):
        self.filename = filename
    def List(self):
        with open(self.filename, 'r') as file:
            content = file.read()
        return json.loads(content)
    def Append(self, dataobj):
        l = self.List()
        l.append(dataobj)
        j = json.dumps(l, indent=4)
        with open(self.filename, 'w') as file:
            file.write(j)
        return l
    def Contains(self, filter):
        for item in self.List():
            if filter(item):
                return True
        return False
class WatchList():
    def __init__(self, filename=WATCHLIST_FILE):
        self.filename = filename
    def List(self):
        jf = JSONfile(self.filename)
        return jf.List()
    def Append(self, title):
        title = title.lower()
        jf = JSONfile(self.filename)
        if not self.Exist(title):
            return jf.Append({'title': title})
        else:
            return '[!] Title Already Exist'
    def Exist(self, title):
        title = title.lower()
        jf = JSONfile(self.filename)
        return jf.Contains(lambda series: series['title'] == title)
class IMDbScrapper():
    @staticmethod
    def get_rate(tv_id):
        url = "https://www.imdb.com/title/"+tv_id
        html = requests.get(url).text
        soup = BeautifulSoup(html, 'lxml')
        return soup.find('div', {"data-testid": "hero-title-block__aggregate-rating__score"}).text.strip()
    def ScrapeSeries(self, series):
        try:
            tv_id = None
            try:
                # [1] Search in IMDb
                url = "https://www.imdb.com/find?q="+series.replace(' ','%2B')+"&s=tt&ttype=tv"
                html = requests.get(url).text
                soup = BeautifulSoup(html, 'lxml')

                # [2] Get the first link
                tv_block = soup.find('div', {'class': 'findSection'}).find('table', {'class': 'findList'}).find('tr')
                tv_text = tv_block.find('td', {'class': 'result_text'}).a.text.strip()
                tv_link = tv_block.find('td').a['href']
                tv_id = tv_link.split('/')[2]
            except Exception as e:
                print("["+series+"] Not found on 'IMDb'.")
                print("[!] Exception Error:",e)

            if tv_id:
                ViewSeriesCatchedInfo(tv_text, tv_id)

                # Go to the episodes page and then extract the data
                def method_2():
                    # [3] Go to the episodes page
                    url = "https://www.imdb.com/title/"+tv_id+"/episodes"
                    html = requests.get(url).text
                    soup = BeautifulSoup(html, 'lxml')

                    season = soup.find('h3', {'id': 'episode_top'}).text

                    episodes = soup.find('div', {'id': 'episodes_content'}).find('div', {'class': 'list'}).find_all('div', {'class': 'list_item'})

                    episode_data = []

                    index = 0
                    for ep in episodes:
                        number = ep.find('div', {'class': 'image'}).find('div', {'class': 'hover-over-image'}).text.split('Ep')[1].strip()
                        date = ep.find('div', {'class': 'info'}).find('div', {'class': 'airdate'}).text.strip()
                        title = ep.find('strong').text.strip()
                        rate = ep.find('span', {'class': 'ipl-rating-star__rating'}).text.strip()+'/'+'10'

                        episode_data.append({
                            'index': index,
                            'number': number,
                            'title': title,
                            'date': date,
                            'rate': rate
                        })
                        index += 1

                    return [season, episode_data]

                # Prepare the information
                tv_rate = self.get_rate(tv_id)
                season, episodes = method_2()

                ViewSeriesInformation(tv_text, tv_id, tv_rate, season, episodes)
        except Exception as e:
            print("[!] Exception Error:",e)

class RottenTomatoesScrapper():
    @staticmethod
    def get_rate(url):
        html = requests.get(url).text
        soup = BeautifulSoup(html, 'lxml')
        return soup.find('a', {'id': 'tomato_meter_link'}).text.strip()
    def ScrapeSeries(self, series):
        try:
            url = "https://www.rottentomatoes.com/search?search="+series.replace(' ','%20')
            html = requests.get(url).text
            soup = BeautifulSoup(html, 'html.parser')

            tv_id = None

            try:
                tvs_json = soup.find('script', {'id': 'tvs-json'})
                relevant = str(tvs_json).split('>')[1].replace("</script", "").strip()
                data = json.loads(relevant)
                item = data['items'][0]
                tv_text = item['name']
                tv_link = item['url']
                tv_id = tv_link.split("/")[-1]
            except Exception as e:
                print("["+series+"] Not found on 'Rotten Tomatoes'.")
                print("[!] Exception Error:",e)

            if tv_id and tv_link:
                ViewSeriesCatchedInfo(tv_text, tv_id)

                url = tv_link
                html = requests.get(url).text
                soup = BeautifulSoup(html, 'lxml')

                last_episode_section = soup.find('section', {'id': 'most-recent-episode'})
                last_aired_episode = " ".join(last_episode_section.find('p', {'class': 'airDate'}).text.strip().split(" ")[1:])
                last_episode_info = str(last_episode_section.find('div', {'class': 'media-body'}).find('div', {'class': 'info'})).split("<br/>")[1].replace("</div>", "")

                print("===> Last Episode Information <===")
                print("")
                print("[>] Last Aired Episode Date:", last_aired_episode)
                print("[>] Last Aired Episode Info:", last_episode_info)
                print("")

                print("[*] PLease wait while getting the episodes...")
                print("")

                last_season = soup.find('section', {'id': 'seasonList'}).find_all('div')[0].find_all('a')[0]

                url = "https://www.rottentomatoes.com/"+last_season['href']
                html = requests.get(url).text
                soup = BeautifulSoup(html, 'lxml')

                episodes = soup.find('section', {'id': 'desktopEpisodeList'}).find('div', {'id': 'episode-list-root'}).find_all('div', {'class': 'episodeItem'})

                episode_data = []

                index = 0
                for ep in episodes:
                    ep_title = ep.find('a', {'class': 'episodelink-title'}).text.strip().split(".")
                    number = ep_title[0]
                    title = ep_title[1]
                    date = ep.find('div', {'class': 'airDate'}).text.strip().split(":")[1]

                    episode_data.append({
                        'index': index,
                        'number': number,
                        'title': title,
                        'date': date
                    })
                    index += 1

                rate = self.get_rate(tv_link)

                ViewSeriesInformation(tv_text, tv_id, rate, last_episode_info, episode_data)
        except Exception as e:
            print("[!] Exception Error:",e)
# ==============================> Main <==============================
def get_first_char(text):
    return text[0].lower()

def get_args():
    import argparse
    parser = argparse.ArgumentParser(description='Get a tv series information from IMDb or Rotten Tomatoes.')
    parser.add_argument('-s', '--series', help='Series Title')
    parser.add_argument('-w', '--watch-list', help='Watch List Filename')
    args = parser.parse_args()
    return args

def mainMenu():
    print("")
    print("===> Main Menu <===")
    print("1. Check a series title")
    print("2. Check a watch list or add a title to a watch list")
    print("3. Check the titles in a watchlist")
    print("0. Exit")
    print("")
    print("[>] Please enter a number.")
    menu = input("[?] ")
    print("")

    menu_args = Object()
    menu_args.series = None
    menu_args.watch_list = None

    if menu == '0':
        sys.exit(0)
    elif menu == '1':
        series_title = input("[?] Series Title: ")
        menu_args.series = series_title
    elif menu == '2':
        watch_list_filename = input("[?] Watch List Filename (default: "+WATCHLIST_FILE+"): ")
        if not watch_list_filename:
            watch_list_filename = WATCHLIST_FILE
        menu_args.watch_list = watch_list_filename
    elif menu == '3':
        watch_list_filename = input("[?] Watch List Filename (default: "+WATCHLIST_FILE+"): ")
        if not watch_list_filename:
            watch_list_filename = WATCHLIST_FILE
        wl = WatchList(watch_list_filename)

        what_site = input("[?] Choose a website to get the data from ([I]mdb / [R]ottenTomatoes) (default: imdb): ")
        if not what_site:
            Scrapper = IMDbScrapper()
        elif get_first_char(what_site) == "i":
            Scrapper = IMDbScrapper()
        elif get_first_char(what_site) == "r":
            Scrapper = RottenTomatoesScrapper()

        print("[*] Please wait...")
        print("")
        for series in wl.List():
            print("---",series['title'],"---")
            print("[*] Please wait...")
            print("")
            Scrapper.ScrapeSeries(series['title'])
            print("")
        print("[+] Done. Please scroll up to see the results.")
    else:
        menu_args = None
        print("[!] Invalid Number! Please enter a valid number from the list.")
        print("")
        return mainMenu()

    main(menu_args)

def main(args=None):
    if args.watch_list:
        wl = WatchList(args.watch_list)
        print("===> Your WatchList <===")
        print(wl.List())
        print("")
        print("Add a series to the watch list or just click enter to cancel.")
        title_input = input("[?] Please enter the title: ")
        if title_input: print(wl.Append(title_input))
    elif args.series:
        if args.series:
            what_site = input("[?] Choose a website to get the data from ([I]mdb / [R]ottenTomatoes): ")

            if get_first_char(what_site) == "i":
                Scrapper = IMDbScrapper()
            elif get_first_char(what_site) == "r":
                Scrapper = RottenTomatoesScrapper()
            else:
                sys.exit('[x] Input Error!')

            print("[*] Please wait...")
            print("")
            Scrapper.ScrapeSeries(args.series)
        else:
            print("[x] No Input!")
    else:
        mainMenu()

def Run():
    sys.exit(main(get_args()))

if __name__ == '__main__':
    Run()