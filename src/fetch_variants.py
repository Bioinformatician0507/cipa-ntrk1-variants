import requests
import json
import csv

BASE_URL = "https://myvariant.info/v1/query"

def fetch_ntrk1_variants():
    all_hits = []
    fields = "clinvar.rcv,clinvar.gene,cadd,dbnsfp.genename,dbnsfp.hgvsp,gnomad_exome.af"
    from_ = 0
    size = 100

    while True:
        params = {
            "q": "clinvar.gene.symbol:NTRK1",
            "fields": fields,
            "size": size,
            "from": from_
        }
        resp = requests.get(BASE_URL, params=params, timeout=30)
        resp.raise_for_status()
        data = resp.json()

        hits = data.get("hits", [])
        if not hits:
            break

        all_hits.extend(hits)
        print(f"Fetched {len(all_hits)} / {data.get('total', '?')}")

        from_ += size
        if from_ >= data.get("total", 0):
            break

    return all_hits

if __name__ == "__main__":
    hits = fetch_ntrk1_variants()

    with open("data/ntrk1_variants_raw.json", "w") as f:
        json.dump(hits, f, indent=2)

    print(f"\nSaved {len(hits)} variants to data/ntrk1_variants_raw.json")
