import requests
import json
import os

token = os.environ.get("ZENODO_TOKEN", "iXAm71bZRic2YdLTkiVthcL7HFANPnbdE3DXcQfQtwSL0BTkr3reaE5rEejj")
headers = {"Authorization": f"Bearer {token}"}
url = "https://zenodo.org/api/deposit/depositions"

def fetch_all_md():
    all_md = {}
    # Comprehensive search using common keywords to exceed 10k record limits
    keywords = ["Neuroscience", "Preprint", "Open Research", "Serna", "Taxonomy", "Scale"]
    for q in keywords:
        print(f"Searching keyword: {q}")
        for page in range(1, 101):
            r = requests.get(url, headers=headers, params={"q": q, "page": page, "size": 100})
            if r.status_code != 200: break
            depos = r.json()
            if not depos: break
            for d in depos:
                for f in d.get("files", []):
                    name = f.get("filename") or f.get("key", "")
                    if name.endswith(".md"):
                        all_md[f["id"]] = {"depo_id": d["id"], "filename": name}
            if len(depos) < 100: break
    return list(all_md.values())

def main():
    mds = fetch_all_md()
    print(f"Found {len(mds)} unique MD files.")
    with open("scripts/zenodo/md_inventory.json", "w") as f:
        json.dump(mds, f, indent=2)

if __name__ == "__main__":
    main()
