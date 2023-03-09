import csv
import time
import tkinter as tk
from tqdm import tqdm
from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select


def clear_entry():
    url_entry.delete(0, tk.END)
    limit_entry.delete(0, tk.END)


def scrape_images():
    # Getting url and limit from user
    url = url_entry.get()
    limit = int(limit_entry.get())

    # Setting up the edge driver
    driver = webdriver.Edge()

    # Opening the website
    driver.get(url)

    try:
        day = Select(driver.find_element(By.ID, "ageDay"))
        month = Select(driver.find_element(By.ID, "ageMonth"))
        year = Select(driver.find_element(By.ID, "ageYear"))
        day.select_by_value("9")
        month.select_by_value("October")
        year.select_by_value("2000")
        driver.find_element(By.LINK_TEXT, "View Page").click()
    except NoSuchElementException:
        pass

    # Extracting the game title from the page
    game_title = driver.find_element(By.CSS_SELECTOR, "#ModalContentContainer > div.apphub_background > "
                                                      "div.apphub_HomeHeader > div.apphub_HomeHeaderContent > "
                                                      "div.apphub_HeaderTop > div.apphub_AppDetails > "
                                                      "div.apphub_AppName.ellipsis").text

    # Creating a list to store the image urls
    image_urls = []
    # Creating a progress bar to show time left for scraping
    progress_bar = tqdm(total=limit)

    # Scrolling down the page until the desired number of images is reached or no more images are loaded
    while len(image_urls) < limit:
        # Finding all the images on the page
        images = driver.find_elements(By.CLASS_NAME, "apphub_CardContentPreviewImage")
        # Getting the urls of each image and appending them to the list if not already present
        for image in images:
            url = image.get_attribute("src")
            if url not in image_urls:
                image_urls.append(url)
                progress_bar.update(1)
                if len(image_urls) == limit:
                    break
        # If the desired limit has been reached or no more images are available, break out of the loop
        if len(image_urls) == limit or len(images) == 0:
            break
        # Scrolling down by one-page height
        driver.execute_script("window.scrollBy(0, window.innerHeight);")
        # Waiting for up to 10 seconds until more images are loaded on the page
        time.sleep(10)

    progress_bar.close()
    # Closing the driver
    driver.close()

    # Creating the filename for the CSV file
    filename = f"{game_title}_images.csv"

    # Writing the image urls to a csv file with one url per line
    with open(filename, "w", newline="") as f:
        writer = csv.writer(f)
        for url in image_urls:
            writer.writerow([url])


# Creating the GUI
root = tk.Tk()
root.title("Steam Image Scraper")

# Creating a label and entry for the url input
url_example = tk.Label(root, text="Example URLs: \nhttps://steamcommunity.com/app/1240440/images/\nhttps"
                                  "://steamcommunity.com/app/49540/screenshots/\n"
                                  "You can find URLs under the 'Artwork' or 'ScreenShots' tabs of a game page")
url_example.pack(side=tk.TOP)
url_label = tk.Label(root, text="Enter url for steam images:")
url_label.pack(side=tk.LEFT)
url_entry = tk.Entry(root)
url_entry.pack(side=tk.LEFT)

# Creating a label and entry for the limit input
limit_label = tk.Label(root, text="Enter the maximum number of images to scrape:")
limit_label.pack(side=tk.LEFT)
limit_entry = tk.Entry(root)
limit_entry.pack(side=tk.LEFT)

# Creating a button to initiate the scraping process
scrape_button = tk.Button(root, text="Scrape Images", command=scrape_images)
scrape_button.pack(side=tk.LEFT)

# Creating a button to clear previous input
clear_button = tk.Button(root, text="Clear", command=clear_entry)
clear_button.pack()
# Starting the GUI event loop
root.mainloop()
