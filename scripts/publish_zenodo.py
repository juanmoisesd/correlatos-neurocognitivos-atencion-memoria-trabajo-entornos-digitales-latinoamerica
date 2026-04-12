import os
import requests
import json

# Fetch token from environment variable
ACCESS_TOKEN = os.environ.get('ZENODO_TOKEN')
BASE_URL = 'https://zenodo.org/api/deposit/depositions'

def publish(collection_type='English'):
    if not ACCESS_TOKEN:
        print("Error: ZENODO_TOKEN environment variable not set.")
        return

    # 1. Create a new deposition
    headers = {"Content-Type": "application/json"}
    params = {'access_token': ACCESS_TOKEN}
    r = requests.post(BASE_URL, params=params, json={}, headers=headers)

    if r.status_code != 201:
        print(f"Error creating deposition: {r.status_code}")
        print(r.json())
        return

    res_json = r.json()
    deposition_id = res_json['id']
    bucket_url = res_json['links']['bucket']
    print(f"Deposition created for {collection_type}: {deposition_id}")

    # 2. Upload files
    pdf_dir = 'manuscripts/pdfs_en' if collection_type == 'English' else 'manuscripts/pdfs'
    if not os.path.exists(pdf_dir):
        print(f"Error: Directory {pdf_dir} does not exist.")
        return

    for filename in os.listdir(pdf_dir):
        if filename.endswith('.pdf'):
            file_path = os.path.join(pdf_dir, filename)
            with open(file_path, "rb") as fp:
                r = requests.put(
                    f"{bucket_url}/{filename}",
                    data=fp,
                    params=params,
                )
            if r.status_code in [200, 201]:
                print(f"Uploaded: {filename}")
            else:
                print(f"Error uploading {filename}: {r.status_code}")

    # 3. Add metadata
    if collection_type == 'English':
        metadata = {
            'title': 'Advanced Meta-Analyses in Neuroscience and Emotional Psychology (English Collection)',
            'upload_type': 'publication',
            'publication_type': 'article',
            'description': 'A comprehensive collection of 10 advanced scientific meta-analyses exploring emotional architecture, neuroplasticity, mindfulness, and the social brain.',
            'creators': [{'name': 'de la Serna, Juan Moisés', 'affiliation': 'UNIR'}],
            'keywords': ['Neuroscience', 'Emotional Intelligence', 'Meta-analysis', 'PRISMA', 'Brain Plasticity', 'Mindfulness']
        }
    else:
        metadata = {
            'title': 'Meta-análisis en Neurociencia y Psicología Emocional (Colección en Español)',
            'upload_type': 'publication',
            'publication_type': 'article',
            'description': 'Colección de 10 metaanálisis sobre arquitectura emocional, neuroplasticidad, mindfulness y cerebro social.',
            'creators': [{'name': 'de la Serna, Juan Moisés', 'affiliation': 'UNIR'}]
        }

    data = {'metadata': metadata}
    r = requests.put(f"{BASE_URL}/{deposition_id}", params=params, data=json.dumps(data), headers=headers)
    if r.status_code == 200:
        print("Metadata updated.")
    else:
        print(f"Error updating metadata: {r.status_code}")
        print(r.json())

    # 4. Finalize/Publish
    r = requests.post(f"{BASE_URL}/{deposition_id}/actions/publish", params=params)
    if r.status_code == 202:
        print(f"Published {collection_type} collection successfully.")
        print(f"Published DOI: {r.json().get('doi')}")
    else:
        print(f"Error publishing: {r.status_code}")
        print(r.json())

    print(f"Deposition URL: https://zenodo.org/deposit/{deposition_id}")

if __name__ == "__main__":
    publish('English')
