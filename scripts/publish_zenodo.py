import os
import requests
import json
import time

def publish_lang(lang, pdf_dir):
    token = os.environ.get('ZENODO_TOKEN')
    if not token:
        print("Error: ZENODO_TOKEN not set.")
        return

    if not os.path.exists(pdf_dir):
        print(f"Skipping {lang}, {pdf_dir} missing.")
        return

    headers = {"Content-Type": "application/json"}
    params = {'access_token': token}

    r = requests.post('https://zenodo.org/api/deposit/depositions', params=params, json={}, headers=headers)
    if r.status_code != 201:
        print(f"Error {lang}: {r.status_code}")
        return

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
            'description': f'10 meta-analyses on neuroscience and emotional intelligence ({lang}).',
            'creators': [{'name': 'de la Serna, Juan Moisés', 'affiliation': 'UNIR'}]
        }
    }
    requests.put(f"https://zenodo.org/api/deposit/depositions/{dep_id}", params=params, data=json.dumps(meta), headers=headers)
    requests.post(f"https://zenodo.org/api/deposit/depositions/{dep_id}/actions/publish", params=params)
    print(f"Published {lang}: {dep_id}")

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 3:
        print("Usage: python publish_zenodo.py <lang> <pdf_dir>")
    else:
        publish_lang(sys.argv[1], sys.argv[2])
