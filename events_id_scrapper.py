import concurrent.futures.thread
import json

import requests as req
from tqdm import tqdm

base = "https://d29dxerjsp82wz.cloudfront.net/api/v3/event/live/"

if __name__ == "__main__":
    events_id = []

    def iterate_through_ufc_events(event_id):
        data = req.get(base + str(event_id) + ".json").json()
        if not data["LiveEventDetail"] or data["LiveEventDetail"]["Organization"]["OrganizationId"] != 1:
            return
        events_id.append(event_id)


    with open('events_id.json', 'w', encoding='UTF8') as file:
        print('scrapping')
        possible_event_id_values = range(1300)
        with concurrent.futures.thread.ThreadPoolExecutor() as Executor:
            list(tqdm(Executor.map(iterate_through_ufc_events, possible_event_id_values),
                      total=1300))
        json.dump(events_id, file)

    print('done')
