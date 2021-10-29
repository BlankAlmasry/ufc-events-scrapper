import csv
from datetime import datetime
import requests
from bs4 import BeautifulSoup

base = "https://www.ufc.com"

if __name__ == "__main__":
    def recurse_through_ufc_events(next_event="/event/ufc-1"):
        page = requests.get(base + next_event)
        soup = BeautifulSoup(page.content, "html.parser")

        timestamp = int(soup.find('div', class_='tz-change-inner')['data-timestamp'])
        # don't scrape the future event
        if timestamp > current_time_stamp:
            return

        # Convert it to 0000-00-00 format
        dt = str(datetime.fromtimestamp(timestamp)).split(' ')[0]

        try:
            title = soup.find('div', class_='c-hero__header').h1.text.strip()
            print(title)
        except():
            # Some random pages aren't built well, might be not needed in the future
            print('unknown event name')

        fights = soup.find_all('li', class_='l-listing__item')
        for fight in fights:
            names = list(
                map(
                    lambda elem: elem.text.strip().replace('\n', '-'),
                    fight.find_all('div', class_='c-listing-fight__corner-name')
                )
            )
            results = list(
                map(lambda elem: elem.text.strip(), fight.find_all('div', class_='c-listing-fight__outcome-wrapper')))
            writer.writerow([*names, *results, dt])

        next_event = soup.find('a', 'next')["href"]
        recurse_through_ufc_events(next_event)


    with open('fights.csv', 'w', encoding='UTF8', newline='') as file:
        current_time_stamp = int(datetime.now().timestamp())
        writer = csv.writer(file)
        # Header
        writer.writerow(['first_fighter', 'second_fighter', 'result_1', 'result_2', 'date'])
        print('started scrapping')
        recurse_through_ufc_events()
