#!/usr/bin/env python3

import urllib.request
from bs4 import BeautifulSoup
from selenium import webdriver
import time
import smtplib
from email import message
from pyvirtualdisplay import Display
from datetime import date
import sys


def sendMail(inSale):

    # Get mail credentials
    with open("creds.txt", "r+") as file:
        creds = file.read().splitlines()
        # creds[0] = from_addr
        # creds[1] = to_addr
        # creds[2] = smtp server
        # creds[3] = smtp pw

    if (inSale):
        if (inSale[0] == 'error'):
            # When the scraper finds no products at all, send me a warning.
            subject = 'Bonuswatcher AH - error'
            body = inSale[1]
        else:
            subject = 'Bonuswatcher AH'
            body = 'Deze week in de bonus: \n\n- ' + '\n- '.join(inSale)
    else:
        subject = 'Geen aanbiedingen deze week'
        body = 'Helaas pindakaas, geen door jouw geselecteerde producten zijn in de aanbieding deze week.'

    msg = message.Message()
    msg.add_header('from', creds[0])
    msg.add_header('to', creds[1])
    msg.add_header('subject', subject)
    msg.set_payload(body)

    server = smtplib.SMTP(creds[2], 587)
    server.login(creds[0], creds[3])
    server.send_message(msg, from_addr=creds[0], to_addrs=creds[1])


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
        products = ['error', 'It seems like Albert Heijn changed their CSS classes..again..']

    return products


def main():
    url = 'https://ah.nl/bonus'
    wantedProducts = ["Lavazza Espresso bonen", "Jordans", "Olijfolie", "AH Zacht toiletpapier 4-lagen voordeel", "Robijn", "Falafel", "toiletpapier", "dreft", "lavazza"]
    products = scrapeWebsite(url)

    if (products[0] != 'error'):
        products = [product for product in products if any(wantedProduct.lower() in product.lower() for wantedProduct in wantedProducts)]

    sendMail(products)


main()
