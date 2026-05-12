import requests
import json
import os
import glob

# Using environment variable for security
ACCESS_TOKEN = os.getenv('ZENODO_TOKEN')

def publish_to_zenodo():
    if not ACCESS_TOKEN:
        print("Error: ZENODO_TOKEN environment variable not set.")
        return

    params = {'access_token': ACCESS_TOKEN}

    # 1. Create deposition
    r = requests.post('https://zenodo.org/api/deposit/depositions',
                      params=params,
                      json={},
                      headers={"Content-Type": "application/json"})

    if r.status_code != 201:
        print(f"Error creating deposition: {r.status_code}")
        print(r.json())
        return

    deposition_id = r.json()['id']
    bucket_url = r.json()['links']['bucket']
    print(f"Deposition created: {deposition_id}")

    # 2. Upload French Academic PDFs
    files = glob.glob('results/policy_briefs/fr/pdf/*.pdf')
    for file_path in files:
        file_name = os.path.basename(file_path)
        with open(file_path, "rb") as fp:
            r = requests.put(
                f"{bucket_url}/{file_name}",
                data=fp,
                params=params,
            )
        if r.status_code == 200 or r.status_code == 201:
            print(f"Uploaded: {file_name}")
        else:
            print(f"Error uploading {file_name}: {r.status_code}")

    # 3. Add metadata (Academic French)
    data = {
        'metadata': {
            'title': 'Briefs Politiques Académiques : Neurosciences et Gouvernance (Série I)',
            'upload_type': 'publication',
            'publication_type': 'report',
            'description': 'Une collection de 10 briefs politiques académiques approfondis explorant l\'intégration des neurosciences affectives et sociales dans les politiques publiques, la santé et l\'éducation. Auteur : Juan Moises de la Serna.',
            'creators': [{'name': 'de la Serna, Juan Moises',
                          'affiliation': 'Universidad Internacional de La Rioja (UNIR)',
                          'orcid': '0000-0002-8401-8018'}],
            'access_right': 'open',
            'license': 'cc-by-4.0',
            'keywords': ['Neurosciences', 'Politiques Publiques', 'Architecture Émotionnelle', 'Neuroplasticité', 'Gouvernance', 'Santé Mentale', 'France']
        }
    }
    r = requests.put(f'https://zenodo.org/api/deposit/depositions/{deposition_id}',
                     params=params,
                     data=json.dumps(data),
                     headers={"Content-Type": "application/json"})

    if r.status_code == 200:
        print("Metadata added.")
    else:
        print(f"Error adding metadata: {r.status_code}")
        print(r.json())
        return

    # 4. Publish
    r = requests.post(f'https://zenodo.org/api/deposit/depositions/{deposition_id}/actions/publish',
                      params=params)
    if r.status_code == 202:
        print("Published to Zenodo!")
        print(f"DOI: {r.json()['doi']}")
        print(f"URL: https://zenodo.org/record/{r.json()['id']}")
    else:
        print(f"Error publishing: {r.status_code}")
        print(r.json())

    print(f"URL: https://zenodo.org/deposit/{deposition_id}")

if __name__ == "__main__":
    publish_to_zenodo()
