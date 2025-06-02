import requests
import json
import domojupyter as domo
import time
import pandas as pd
from concurrent.futures import ThreadPoolExecutor, as_completed

def authenticate(domo_instance, email, password):
    auth_url = f"https://{domo_instance}.domo.com/api/content/v2/authentication"
    payload = {
        "method": "password",
        "emailAddress": email,
        "password": password
    }
    headers = {"Content-Type": "application/json"}

    response = requests.post(auth_url, json=payload, headers=headers)
    if response.status_code == 200:
        print("Authentication successful")
        return response.json().get('sessionToken')
    else:
        raise Exception(f"Authentication failed: {response.status_code} - {response.text}")

def get_dataset_mappings():
    df = domo.read_dataframe('DATASET', query='SELECT * FROM table')
    df = df.fillna('')
    return df.groupby('Dataset_ID').apply(
        lambda x: x[['rename', 'Column Description']].to_dict('records')
    ).to_dict()

def remap_dataset(domo_instance, session_token, dataset_id, columns):
    start_time = time.time()
    remap_payload = {
        "columns": [{"name": col['rename'], "description": col['Column Description']} for col in columns]
    }
    url = f"https://{domo_instance}.domo.com/api/query/v1/datasources/{dataset_id}/wrangle"
    headers = {
        'x-domo-authentication': session_token,
        'Content-Type': 'application/json'
    }

    try:
        response = requests.post(url, headers=headers, json=remap_payload)
        if response.status_code == 200:
            print(f"Remapping successful: {dataset_id}")
        else:
            print(f"Remapping failed for {dataset_id}: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"rror processing {dataset_id}: {str(e)}")

    duration = time.time() - start_time
    print(f"⏱ Time taken for {dataset_id}: {duration:.2f}s")
    time.sleep(2)

def authenticate_and_remap(domo_instance, email, password, max_workers=5):
    session_token = authenticate(domo_instance, email, password)
    dataset_mappings = get_dataset_mappings()
    total_datasets = len(dataset_mappings)
    print(f"\n🔍 Total datasets to process: {total_datasets}\n")
    processed_count = 0

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {
            executor.submit(remap_dataset, domo_instance, session_token, ds_id, cols): ds_id
            for ds_id, cols in dataset_mappings.items()
        }

        for future in as_completed(futures):
            ds_id = futures[future]
            try:
                future.result()
                processed_count += 1
            except Exception as e:
                print(f"❗ Exception for dataset {ds_id}: {e}")

    print(f" Finished processing. Datasets attempted: {total_datasets}, successfully processed: {processed_count}")

domo_instance = ''
email = ''
password = ''

authenticate_and_remap(domo_instance, email, password)
