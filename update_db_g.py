from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
import time
import requests
import shutil
import psycopg2
import datetime

def scrape():
    root_link = "https://store.epicgames.com/en-US/"
    base_link = "https://store.epicgames.com"

    binary = FirefoxBinary('C:\\Program Files\\Mozilla Firefox\\firefox.exe')
    driver = webdriver.Firefox(firefox_binary=binary)

    driver.get(root_link)
    time.sleep(5)
    html = driver.page_source
    soup = BeautifulSoup(html, 'lxml')

    db_args = []

    for game in soup.find_all('div', class_='css-5auk98'):
        name = game.find('div', class_='css-1h2ruwl').text
        ref = base_link + game.find('a').get('href')
        img_ref = game.find('img', class_='css-174g26k')['src']
        dates = game.find('span', class_='css-nf3v9d')
        date_range = game.find('span', class_='css-nf3v9d').text
        date_range_arr = dates.find_all('time')
        start = date_range_arr[0].get('datetime')
        end = date_range_arr[1].get('datetime')
        ret_tup = (name, ref, start, end, img_ref, date_range)
        db_args.append(ret_tup)

    driver.quit()
    return db_args

def update(db_args):
    #Establishing the connection
    conn = psycopg2.connect(
    database="", user='', password='', host='127.0.0.1', port= '5432'
    )
    #Setting auto commit false
    conn.autocommit = True

    #Creating a cursor object using the cursor() method
    cursor = conn.cursor()
    for args in db_args:
        tmp_start = datetime.datetime.strptime(args[2][0:10], '%Y-%m-%d').date()
        tmp_end = datetime.datetime.strptime(args[3][0:10], '%Y-%m-%d').date()
        print(type(tmp_start))
    # Preparing SQL queries to INSERT a record into the database.
        sql_statement = f"INSERT INTO epic(name, reference, start_date, end_date, img_ref, date_range) VALUES(\'{args[0]}\', \'{args[1]}\', \'{tmp_start}\', \'{tmp_end}\', \'{args[4]}\', \'{args[5]}\')" 
        cursor.execute(sql_statement)

# Commit your changes in the database
    conn.commit()
    print("Records inserted........")

# Closing the connection
    conn.close()

def main():
    db_args = scrape()
    update(db_args)

if __name__ == '__main__':
    main()
