# Steam Image Scraper

A Python script that scrapes images from the Artwork/ScreenShots tabs of Steam games.

## Description

This script uses Selenium library to scrape images from Steam games given a URL from Artwork/ScreenShots. It does not use BeautifulSoup or any other parsing library. It scrapes the image URLs directly from the source code of the web pages. It saves the image URLS in a CSV file named after the game title.

## Usage

To run the script, you need to have Python 3 and Selenium library installed. You can install Selenium using pip:

`pip install selenium`

You also need to have a web driver for your browser of choice. You can download one from https://www.selenium.dev/documentation/en/webdriver/driver_requirements/
the application here uses Edge as the default driver, so you might not need to download one.

Then, you can run the script from the command line:

`python steamImageScraper.py`

The script will open a GUI with two inputs one where you copy the url of the steam page and one to specify how many images you wish to scrape
keep in mind that the script uses selenium and can be somewhat slow.

## Credits

This script was created by Cameron Guinn (Dsarken) as a personal project. You can find more of my Python programs at https://github.com/Dsarken
