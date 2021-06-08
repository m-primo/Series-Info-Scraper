# Series-Info-Scraper
Get a tv series information from [IMDb](https://imdb.com/) or [Rotten Tomatoes](https://rottentomatoes.com).


# Screenshots
![lastscreenshot#v2.1](https://lh3.googleusercontent.com/-uqXygpnw_pc/YL762MayZII/AAAAAAAAGsg/seW_UFeAnQgBsVVG9EPQKxrQGyXwLMlkwCNcBGAsYHQ/s0/Screenshot%2B2021-06-08%2B070520.png)
![screenshot#1](https://lh3.googleusercontent.com/-xqC9CFHUxiY/YLjNWlh6zeI/AAAAAAAAGrk/iR7IzTrCglkW_oq9xspFIqBqkoNeexOTwCNcBGAsYHQ/s0/Screenshot%2B2021-06-03%2B143614.png)
![screenshot#2](https://lh3.googleusercontent.com/-Jlc3J-fAyXU/YLkavGEd-QI/AAAAAAAAGrs/2-y8NFmBzcMG-JdEimJFNBN_hBtLaZydQCNcBGAsYHQ/s0/Screenshot%2B2021-06-03%2B200826.png)


# Installation
Before the installation you'll need to have:
1. [Python 3](https://www.python.org/downloads/).
2. pip.

Then:

3. Clone this repository. (Or just download it)
```bash
git clone https://github.com/m-primo/Series-Info-Scraper.git
```
4. Navigate to the directory.
```bash
cd Series-Info-Scraper
```
5. install the requirements.
```bash
pip install -r requirements.txt
```
6. Run.
```bash
python app.py
```

# Run
Run the script.
```bash
python app.py
```
You can also enter an argument of the series title:
```bash
python app.py -s [title]
```
If you want to check your watch list or add a title to a watch list:
```bash
python app.py -w [watchlist_filename]
```
If you want to create multiple watch lists, you have to copy `watchlist.json` and name it whatever your want.
**Important Notice: Do not leave the watch list file empty. The file has to be json encoded.**

# TO-DO
- [x] More than a website.
- [x] Watch list and save it in a json file.
- [x] More than a watchlist.
- [ ] Create a watchlist with the app.
- [x] Default watchlist and change it from the app.
- [x] Remove a title from the app.
- [ ] Notification System/Background Process.
- [ ] User interface (web or gui).


# Contributing
1. [Fork this repository](https://github.com/m-primo/Series-Info-Scraper/fork).
2. Clone your repository.
```bash
git clone [your_repo]
```
3. Make & commit your changes.
```bash
git commit -m "[message]"
```
3. Push it.
```bash
git push
```
4. Create a [new pull request](https://github.com/m-primo/Series-Info-Scraper/pulls) in this repository.


# Legal
THIS REPOSITORY AND EVERY SCRIPT INCLUDED IN IT IS FOR EDUCATIONAL, TESTING, AND RESEARCH PURPOSES ONLY. THE OWNER NOR ANY CONTRIBUTORS IS NOT RESPONSIBLE FOR YOUR ACTIONS.


# License
[BSD-2-Clause License](LICENSE)