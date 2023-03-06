import argparse
import csv
import requests
from bs4 import BeautifulSoup


def scrape_steam_profile(url):
    # Send an HTTP GET request to the webpage
    res = requests.get(url)

    # Check if the request was successful
    if res.status_code == 200:
        # Parse the HTML of the page
        soup = BeautifulSoup(res.text, 'html.parser')

        # User info
        username = soup.find('span', class_='actual_persona_name').text.strip()
        city_country = soup.find('div', class_='header_real_name ellipsis').text.strip()
        player_level = soup.find('span', class_='friendPlayerLevelNum').text.strip()
        num_badges = soup.find('span', class_='profile_count_link_total').text.strip()
        status = soup.find('div', class_='profile_in_game_header').text.strip()

        # Game info
        games_info = soup.find('div', class_='showcase_content_bg showcase_stats_row')
        games_values = games_info.find_all('div', class_='value')
        games_labels = games_info.find_all('div', class_='label')
        favorite_game = soup.find('div', class_='showcase_item_detail_title').text.strip()

        # Write the data to a CSV file
        with open('steam_data.csv', 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(
                ['Username', 'City/Country', 'Player Level', 'Number of Badges', 'Status', 'Profile Picture URL'])
            writer.writerow([username, city_country, player_level, num_badges, status,
                             'https://cdn.akamai.steamstatic.com/steamcommunity/public/images/items/1379870/6efb6ca539385054ccf1384b6f586e539563f62e.gif'])
            writer.writerow(['Game', 'Value', 'Hours Played'])
            for label, value in zip(games_labels, games_values):
                game_name = label.text.strip()
                game_value = value.text.strip()
                game_hours = value.find_next_sibling('div').text.strip()
                writer.writerow([game_name, game_value, game_hours])
            writer.writerow(['Favorite game', favorite_game])

        print(f'Successfully scraped data from {url}!')
    else:
        # Print an error message if the request was not successful
        print(f'Error: {res.status_code}')


if __name__ == '__main__':
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description='Scrape data from a Steam profile and save it to a CSV file.')
    parser.add_argument('url', type=str, help='the URL of the Steam profile to scrape')
    args = parser.parse_args()

    # Scrape the Steam profile
    scrape_steam_profile(args.url)
