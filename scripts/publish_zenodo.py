import os
import requests
import json
import sys

def publish(lang, pdf_dir):
    token = os.environ.get('ZENODO_TOKEN')
    if not token:
        print("Error: ZENODO_TOKEN not set.")
        sys.exit(1)

    if not os.path.exists(pdf_dir):
        print(f"Error: {pdf_dir} not found.")
        sys.exit(1)

    headers = {"Content-Type": "application/json"}
    params = {'access_token': token}

    r = requests.post('https://zenodo.org/api/deposit/depositions', params=params, json={}, headers=headers)
    if r.status_code != 201:
        print(f"Error creating deposition: {r.status_code}")
        print(r.json())
        sys.exit(1)

    dep_id = r.json()['id']
    bucket_url = r.json()['links']['bucket']

    for f in os.listdir(pdf_dir):
        if f.endswith('.pdf'):
            with open(os.path.join(pdf_dir, f), 'rb') as fp:
                requests.put(f"{bucket_url}/{f}", data=fp, params=params)

    meta = {
        'metadata': {
            'title': f'Neuroscience Meta-Analysis Collection ({lang.upper()})',
            'upload_type': 'publication',
            'publication_type': 'article',
            'description': f'10 professional meta-analyses on neuroscience topics ({lang}).',
            'creators': [{'name': 'de la Serna, Juan Moisés', 'affiliation': 'UNIR'}]
        }
    }
    requests.put(f"https://zenodo.org/api/deposit/depositions/{dep_id}", params=params, data=json.dumps(meta), headers=headers)
    requests.post(f"https://zenodo.org/api/deposit/depositions/{dep_id}/actions/publish", params=params)
    print(f"Published {lang}: https://zenodo.org/deposit/{dep_id}")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python publish_zenodo.py <lang> <pdf_dir>")
    else:
        publish(sys.argv[1], sys.argv[2])
