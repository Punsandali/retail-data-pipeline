from google.cloud import bigquery

PROJECT_ID = "retail-data-pipeline-516009"

client = bigquery.Client(project=PROJECT_ID)

# 1. Simple query to prove authentication works
rows = client.query("SELECT 'connected' AS status, CURRENT_DATE() AS today").result()
for row in rows:
    print(dict(row))

# 2. List the datasets and their locations
for ds in client.list_datasets():
    full = client.get_dataset(ds.reference)
    print(f"{ds.dataset_id}: location = {full.location}")