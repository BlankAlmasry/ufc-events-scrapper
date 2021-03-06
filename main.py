import concurrent.futures.thread
import csv
import json
import requests as req
from tqdm import tqdm

"""
Will Search through Ufc cdn stats and return only ufc events
Will return the future events results as nothing in csv
At the time of making this script the last Scheduled Event had id of 1067, but it goes until 1350 anyway
I FOUND NO PATTERN WHAT SO EVER regarding EventID numbers and anything regarding their corresponding events_id
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
        # First load the well known events id
        with open('events_id.json', 'r') as f:
            events_id = json.load(f)
        # compute the rest of the possible events id

        """
         the numbers is hard coded passed on the pattern i saw the api have
         event ids incrementing over time so i check 50 before last event id
         normally they jump like 5 or 6 but just put 50 as future insurance
         i would estimate that it would about 6 years for all the future possible events to happen
        """
        possible_event_id_values = [n for n in range(max(events_id[-1] - 50, 1000), max(events_id[-1] - 50, 1000) + 250)
                                    if
                                    n not in events_id]
        # iterate through the events
        with concurrent.futures.thread.ThreadPoolExecutor(max_workers=10) as executor:
            list(tqdm(executor.map(iterate_through_ufc_events, events_id),
                      total=len(events_id)))
            print('Searching for events that are n\'t in pre-computed at events_id.json')
            list(tqdm(executor.map(iterate_through_ufc_events, possible_event_id_values),
                      total=len(possible_event_id_values)))
        print('Done')
