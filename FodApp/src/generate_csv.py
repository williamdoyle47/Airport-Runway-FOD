import requests
import csv

def generate_fod_csv():
    url = 'http://127.0.0.1:8000/all_logs'

    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
    }
    response = requests.request("GET", url, headers=headers, data={})
    json_results = response.json()
    data = []
    csvheader = ['UUID', 'FOD_TYPE', 'COORD', 'IMAGE_PATH', 'RECOMMENDED_ACTION', 'ID', 'TIMESTAMP', 'CONFIDENCE_LEVEL', 'CLEANED']

    for x in json_results:
        listing = [x['uuid'],x['fod_type'], x['coord'], x['image_path'], x['recommended_action'], x['id'], x['timestamp'], x['confidence_level'], x['cleaned']]
        data.append(listing)

    with open('generatedfod.csv', 'w', encoding='UTF8',newline='') as f:
        writer = csv.writer(f)

        writer.writerow(csvheader)
        writer.writerows(data)


    # print('DONE')