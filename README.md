# misc_scripts
Collection of some miscellaneous stand-alone scripts

## bonus_scraper.py
Scrapes the Albert Heijn discount page (www.ah.nl/bonus) looking for specific products. As Im not interested in seeing all products in discount, I wanted a weekly notice of just the products I'm interested in. Using a cronjob this program runs on my Raspberry Pi every Monday morning, notifying me when the Lavazza coffee and Heineken is in the discount.

Cronjob
`0 10 * * 1 /usr/bin/python3 /home/pi/misc_scripts/bonus_scraper.py >> /home/pi/misc_scripts/logs/bonus_scraper.log 2>&1`


## git_deploy.py
This program runs as a daemon on my Raspberry Pi, allowing for deployment through Github.

Cronjob
`@reboot sleep 200; /usr/bin/python3 /home/pi/misc_scripts/git_deploy.py & >> /home/pi/misc_scripts/logs/git_deploy.log 2>&1`
