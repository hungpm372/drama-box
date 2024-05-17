import os
import re
import csv
import time
import requests

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common import NoSuchElementException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from constant import drama_box_constant


def convert_to_valid_folder_name(movie_name):
    valid_folder_name = re.sub(r'[,\s]+', '_', movie_name)
    valid_folder_name = re.sub(r'[\\/:"*?<>|]', '_', valid_folder_name)
    valid_folder_name = re.sub(r'_+', '_', valid_folder_name)
    valid_folder_name = valid_folder_name.strip('_')
    return valid_folder_name


download_directory = os.path.join(os.getcwd(), "data")
options = Options()
options.add_experimental_option("detach", True)
options.add_experimental_option("prefs", {"download.default_directory": drama_box_constant.DEFAULT_DOWNLOAD_DIRECTORY})

# Create a new instance of the Chrome driver
driver = webdriver.Chrome(options=options)
current_page = 1
wait = WebDriverWait(driver, 2)

csv_file_path = os.path.join(download_directory, "movies.csv")

with open(csv_file_path, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(["Title", "Description", "Genres", "Image URL", "Movie folder"])

    while current_page <= drama_box_constant.TOTAL_PAGE:
        driver.get(f"{drama_box_constant.BASE_URL}/{current_page}")
        original_window = driver.current_window_handle
        time.sleep(2)

        # Get the list of movies
        list_movie_element = driver.find_elements(By.XPATH, drama_box_constant.MOVIE_XPATH)
        list_movie_urls = [movie.get_attribute("href") for movie in list_movie_element]

        for movie_url in list_movie_urls:
            driver.get(movie_url)
            time.sleep(2)

            # Get the title of the movie
            title_element = wait.until(EC.presence_of_element_located((By.XPATH, drama_box_constant.TITLE_XPATH)))
            title = title_element.text

            # Get the description of the movie
            description_element = wait.until(
                EC.presence_of_element_located((By.XPATH, drama_box_constant.DESCRIPTION_XPATH)))
            description = description_element.text

            # Get the genre of the movie
            genre_elements = wait.until(
                EC.presence_of_all_elements_located((By.XPATH, drama_box_constant.GENRE_XPATH)))
            genre_arr_texts = [genre_element.text for genre_element in genre_elements]
            genres = ", ".join(genre_arr_texts)

            # Get the image of the movie
            image_element = wait.until(EC.presence_of_element_located((By.XPATH, drama_box_constant.IMAGE_XPATH)))
            image_url = image_element.get_attribute("src")

            # Create a folder for the movie
            folder_name = convert_to_valid_folder_name(title)
            folder_path = os.path.join(download_directory, folder_name)
            if not os.path.exists(folder_path):
                os.makedirs(folder_path)

            # Download the image
            image_path = os.path.join(folder_path, "image.jpg")
            with open(image_path, 'wb') as img_file:
                img_file.write(image_element.screenshot_as_png)

            # Save the movie information to a CSV file
            writer.writerow([title, description, genres, image_url, folder_path])

            # Play the movie
            play_button_element = wait.until(
                EC.presence_of_element_located((By.XPATH, drama_box_constant.PLAY_BUTTON_XPATH)))
            play_button_element.click()
            time.sleep(2)

            # Episode list
            list_episodes = wait.until(
                EC.presence_of_all_elements_located((By.XPATH, drama_box_constant.EPISODES_XPATH)))

            for episode in list_episodes:
                episode.click()
                time.sleep(2)

                # Get the download button
                try:
                    download_button_element = driver.find_element(By.XPATH, drama_box_constant.DOWNLOAD_BUTTON_XPATH)
                    break
                except NoSuchElementException:
                    pass

                # Get the video element
                video_element = wait.until(EC.presence_of_element_located((By.XPATH, drama_box_constant.VIDEO_XPATH)))
                video_url = video_element.get_attribute("src")
                r = requests.get(video_url, stream=True)
                video_path = os.path.join(folder_path, f"{episode.text}.mp4")

                # download started
                print(f'Downloading: {video_path}')
                with open(video_path, 'wb') as f:
                    for chunk in r.iter_content(chunk_size=1024 * 1024):
                        if chunk:
                            f.write(chunk)

                print(f'Download completed: {video_path}')
                time.sleep(2)
        current_page += 1
        time.sleep(2)
