# misc_scripts
Collection of some miscellaneous stand-alone scripts

## bonus_scraper.py
Scrapes the Albert Heijn discount page (www.ah.nl/bonus) looking for specific products. As Im not interested in seeing all products in discount, I wanted a weekly notice of just the products I'm interested in. Using a crontab entry this program runs on my Raspberry Pi every Monday morning, notifying me when the Lavazza coffee and Heineken is in the discount.

## git_deploy.py
This program runs as a daemon on my Raspberry Pi, making it possible to deploy my scripts through Github.
