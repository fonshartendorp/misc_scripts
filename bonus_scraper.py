#!/usr/bin/env python3

import urllib.request
from bs4 import BeautifulSoup
from selenium import webdriver
import time
import datetime
import smtplib
from pyvirtualdisplay import Display
import conf


def getWantedProducts():
    with open("wanted.txt", "r+", encoding="utf-8") as file:
        wantedProducts = file.read().splitlines()
        return wantedProducts

def sendMail(subject, content):

    headers = {
        'Content-Type': 'text/html; charset=utf-8',
        'Content-Disposition': 'inline',
        'Content-Transfer-Encoding': '8bit',
        'From': conf.sender,
        'To': conf.to,
        'Date': datetime.datetime.now().strftime('%a, %d %b %Y  %H:%M:%S %Z'),
        'Subject': subject
    }

    # Create the message.
    msg = ''
    for key, value in headers.items():
        msg += "%s: %s\n" % (key, value)

    if ('warning' in subject):
        msg += "\n%s\n"  % (content)
    elif not content:
        msg += 'Helaas pindakaas, geen door jouw geselecteerde producten zijn in de aanbieding deze week.'
    else:
        msg += 'Deze week in de bonus: \n\n- ' + '\n- '.join(content)

    # Send email.
    s = smtplib.SMTP(conf.host, conf.port)
    s.ehlo()
    s.starttls()
    s.ehlo()
    s.login(conf.username, conf.password)
    print ("sending %s to %s" % (subject, headers['To']))
    s.sendmail(headers['From'], headers['To'], msg.encode("utf8"))
    s.quit()


def scrapeWebsite(url):
    display = Display(visible=0, size=(800, 800))
    display.start()
    browser = webdriver.Chrome()
    browser.get(url)
    browser.execute_script("window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
    time.sleep(3)
    product_elements = browser.find_elements_by_xpath("//*[contains(@class, 'title_lineclamp__23pTR')]")
    products = [product.text for product in product_elements]
    browser.quit()
    display.stop()

    if not products:
        sendMail('Bonusscraper warning', 'It seems like Albert Heijn changed their CSS classes..again..')
        sys.exit()

    return products


def main():
    url = 'https://ah.nl/bonus'
    subject = 'AH - bonusscraper'
    wantedProducts = getWantedProducts()
    allProducts = scrapeWebsite(url)
    matchedProducts = [product for product in allProducts if any(wantedProduct.lower() in product.lower() for wantedProduct in wantedProducts)]

    sendMail(subject, matchedProducts)


main()
