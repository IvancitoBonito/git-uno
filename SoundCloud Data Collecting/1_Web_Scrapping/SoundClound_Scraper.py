class Web_Scraper :
    from selenium import webdriver
    import os
    from selenium.webdriver.common.by import By
    from selenium.webdriver.common.keys import Keys
    from bs4 import BeautifulSoup
    import requests
    import time
    import pandas as pd

    ##### LISTS FOR THE DATA RECOLECTED #####
    # Composer DATA
    Author = []
    followers = []
    following = []
    number_songs = []
    Info = []

    # Songs DATA
    songtitle = []
    composer = []
    plays = []
    datetime_ = []
    comm = []
    likes = []
    sh = []

    def __init__(self,web_lista,Path):
        # Creating list for all the websites to scrap
        self.web_lista = web_lista

        #Driver LOCATION
        self.Path = Path

        # Instancing the driver
        driver = self.webdriver.Opera(executable_path=Path)
        self.driver = driver

        #Scrapping process
        self.scraper_Web(driver, web_lista)
        #Create Dataframes
        self.List_to_Dataframes()

    def scraper_Web(self,driver,web_list):
    # FOR LOOP FOR EVERY WEBSITE
        button_iterator = 1
        for web in web_list:
            # Create time instance for wait
            time = self.time
            #Enter to the page
            driver.get(web)
            time.sleep(1)
            # Look for the cache button
            if button_iterator == 1:
                button = driver.find_element(self.By.ID, 'onetrust-accept-btn-handler')
                # Click on cache button
                time.sleep(2)
                button.click()
                button_iterator -= 1
            # GET COMPOSER DATA and Calculate the scrolling time
            scrolls = self.composer_Data()
            time.sleep(2)
            # Select an element for scrolling
            page = driver.find_element_by_tag_name("html")
            # Scroll until n/10 times
            while scrolls > 0:
                page.send_keys(self.Keys.END)
                time.sleep(3)
                print(f"Scroll #{scrolls}")
                scrolls -= 1
            # Get new source page
            html = driver.page_source
            # Soup object
            soup = self.BeautifulSoup(html, 'html.parser')
            # RESULTS
            list = soup.find('div', attrs={'class': 'soundList lazyLoadingList'})
            results = list.find_all('li', 'soundList__item')
            print("Number of songs: ", len(results))
            self.Collecting_songs_Data(soup,results)

    def Collecting_songs_Data(self, soup,results):
        for song in results:
            # Song title
            try:
                title = song.find('a', 'sc-link-primary soundTitle__title sc-link-dark sc-text-h4').find('span').get_text()
                self.songtitle.append(title)
            except:
                try:
                    self.songtitle.append(
                        song.find('a',
                                  'sc-link-primary soundTitle__title g-opacity-transition-500 g-type-shrinkwrap-block g-type-shrinkwrap-primary theme-dark sc-text-h4').find(
                            'span').get_text())
                except:
                    self.songtitle.append('N/A')
            # COMPOSER AUTHOR
            try:
                self.composer.append(song.find('span', 'soundTitle__usernameText').get_text().strip())
            except:
                self.composer.append('N/A')
                # REPRODUCCIONES
            try:
                self.plays.append(song.find('li', class_='sc-ministats-item').find('span',class_='sc-visuallyhidden').get_text().strip().replace(' plays', ''))
            except:
                self.plays.append('0')
            # DATE
            try:
                self.datetime_.append(song.time['datetime'])
            except:
                self.datetime_.append('N/A')
            # Comments
            try:
                self.comm.append(
                    song.find('ul', class_='soundStats sc-ministats-group').find('a', attrs={"rel": 'nofollow'}).find(
                        'span', attrs={"aria-hidden": 'true'}).get_text())
            except:
                self.comm.append('0')
            # LIKES
            try:
                self.likes.append(song.find('button', attrs={'aria-label': 'Like'}).get_text())
            except:
                self.likes.append('0')
            # Shares
            try:
                self.sh.append(song.find('button', attrs={'aria-label': 'Repost'}).get_text())
            except:
                self.sh.append('0')


    def List_to_Dataframes(self):
        dicti_songs = {
            'title': self.songtitle,
            'composer': self.composer,
            'reproducciones': self.plays,
            'posted_Date': self.datetime_,
            'comments': self.comm,
            'likes': self.likes,
            'shares': self.sh
        }
        df1 = self.pd.DataFrame(dicti_songs)

        dicti_composers = {
            'Name':self.Author,
            'Followers': self.followers,
            'Following': self.following,
            'number_Of_Songs': self.number_songs,
            'Info': self.Info
        }
        df2 = self.pd.DataFrame(dicti_composers)

        print(df1.tail())
        print(df2.tail())
        print('DATAFRAME SONGS shape: ',df1.shape)
        print('Dataframe Artist shape: ',df2.shape)
        # SAVE THE DATAFRAMES TO CSV files
        path1 = r"C:\Users\HP\GIThub\Soundclound_SONGS.csv"
        path2 = r"C:\Users\HP\GIThub\Soundclound_Artists.csv"
        df1.to_csv(path1)
        df2.to_csv(path2)

    def composer_Data(self):
        number_of_scrolls = 0
        #Get the HTML page document
        html = self.driver.page_source
        # Soup object
        soup = self.BeautifulSoup(html, 'html.parser')
        # Collecting Data method
        self.Collecting_Composer_Data(soup)
        # Finding the table of statistics
        primary_data = soup.find('table',attrs={'class':'infoStats__table sc-type-small sc-text-body'}).find_all('td')
        # NUMBER OF SONGS
        number_of_songs = primary_data[2].find('div', attrs={'class':'infoStats__value sc-font-light'}).get_text()
        print(f'Numero de canciones: {number_of_songs}')

        # NUMBER OF SCROLLS FOR THE LAZY LIST
        number_of_scrolls = (int(number_of_songs) // 10)
        print(f'Number of scrolls: {number_of_scrolls}')

        #RETURN THE NUMBER OF SCROLLS CALCULATED
        return number_of_scrolls

    def Collecting_Composer_Data(self, soup):
        # COMPOSER INFO
        # GET Banner WITH THE POSIBLE DATA
        Banner_info = soup.find('div', attrs={'class': 'profileHeaderInfo__content sc-media-content'})
        # SET A PIVOT FROM THE FIRST GENERAL FATA
        h2_name = Banner_info.find('h2', attrs={
            'class': 'profileHeaderInfo__userName g-type-shrinkwrap-block g-type-shrinkwrap-large-primary sc-text-h1 theme-dark'})

        # Author Name
        try:
            self.Author.append(h2_name.get_text().strip().replace("Verified", "").replace("\n",""))
        except:
            self.Author.append("N/A")
        # Finding the table of statistics
        primary_data = soup.find('table',attrs={'class':'infoStats__table sc-type-small sc-text-body'}).find_all('td')
        # Followers
        try:
            self.followers.append(primary_data[0].find('div', attrs={'class':'infoStats__value sc-font-light'}).get_text())
        except:
            self.followers.append("0")
        # Following
        try:
            self.following.append(primary_data[1].find('div', attrs={'class':'infoStats__value sc-font-light'}).get_text())
        except:
            self.following.append("0")
        # Number of songs
        try:
            self.number_songs.append(primary_data[2].find('div', attrs={'class':'infoStats__value sc-font-light'}).get_text())
        except:
            self.number_songs.append('0')

        # GET THE NEXT BANNER ELEMENTS
        info_list = h2_name.find_next_siblings()
        composer_info = ''

        #GET THE LIST FROM THE ELEMENTS
        for item in info_list:
            # IGNORE <br/>
            if item.get_text() == "":
                continue
            else:
                #ADD THE DATA
                composer_info = composer_info + item.get_text().strip() + "-"
        # Info
        try:
            self.Info.append(composer_info)
        except:
            self.Info.append('N/A')



# Selenium Driver's location
PATH = r"C:\SeleniumDrivers\operadriver.exe"

# Websites (Soundcloud artists)
website1 = "https://soundcloud.com/frrb/tracks"
website2 = "https://soundcloud.com/nekoilove/tracks"
website3 = "https://soundcloud.com/kudasaibeats/tracks"
website4 = "https://soundcloud.com/idealismus/tracks"
website5 = "https://soundcloud.com/palmasur/tracks"
website6 = "https://soundcloud.com/kyoshin88/tracks"
website7 = "https://soundcloud.com/wrongnumberlofi/tracks"
website8 = "https://soundcloud.com/iam6teen/tracks"
website9 = "https://soundcloud.com/cxldblxxd/tracks"
website10= "https://soundcloud.com/musictenno/tracks"
lista = [website1,website2,website3,website4,website5, website6,website7, website8, website9, website10]
lista_test = ["https://soundcloud.com/frrb/tracks","https://soundcloud.com/cxldblxxd/tracks"]

# Instancing an object
obj = Web_Scraper(lista, PATH)
