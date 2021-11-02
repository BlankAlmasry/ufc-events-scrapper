import concurrent.futures.thread
import csv
import itertools
import requests as req
from tqdm import tqdm

"""
Will Search through Ufc cdn stats and return only ufc events
Will return the future events results as nothing in csv
At the time of making this script the last Scheduled Event had id of 1067, but it goes until 1350 anyway
I FOUND NO PATTERN WHAT SO EVER regarding EventID numbers and anything regarding their corresponding data
Looks to me stats comes from UFC/DWCS only since event id 819, and it's getting incremented since then
"""

# Might possibly change in few years
base = "https://d29dxerjsp82wz.cloudfront.net/api/v3/event/live/"

if __name__ == "__main__":
    def iterate_through_ufc_events(event_id):
        data = req.get(base + str(event_id) + ".json").json()

        """
        Api return empty LiveEventDetail object when event doesn't exist
        Ufc Organization id is 1, Dana white contender series is 67, I choose to not include other than ufc
        """
        if not data["LiveEventDetail"] or data["LiveEventDetail"]["Organization"]["OrganizationId"] != 1:
            return
        date = data["LiveEventDetail"]["StartTime"][:10]
        for fight in data["LiveEventDetail"]["FightCard"]:
            fighters = []
            results = []
            for index, fighter in enumerate(fight["Fighters"]):
                fighters.append(fighter["Name"]["FirstName"] + "-" + fighter["Name"]["LastName"])
                results.append(fighter["Outcome"]["Outcome"])
            writer.writerow([fighters[0], fighters[1], results[0], results[1], date])


    with open('fights.csv', 'w', encoding='UTF8', newline='') as file:
        writer = csv.writer(file)
        # Header
        writer.writerow(["fighter1", "fighter2", "result1", "result2", "date"])
        print('scrapping')
        """
        Non UFC Event IDS
         123~262
         317~410
         possibility for them to change in the future is very unlikely,
         since they use them for their stats site
        """
        possible_event_id_values = (itertools.chain(range(1, 122), range(263, 316), range(410, 1150)))
        with concurrent.futures.thread.ThreadPoolExecutor() as Executor:
            list(tqdm(Executor.map(iterate_through_ufc_events, possible_event_id_values),
                 total=914))
            # cant calculate itertools.chain obj length without heavy calculation so hardcoded it for now

        print('Searching for any possible random event IDS, You can pause if you wish')
        possible_event_id_values = (n for n in range(1151, 1351))
        with concurrent.futures.thread.ThreadPoolExecutor() as Executor:
            list(tqdm(Executor.map(iterate_through_ufc_events, possible_event_id_values),
                 total=200))
