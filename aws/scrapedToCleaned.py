import sys
import boto3
import json

# Setup S3 client
s3 = boto3.client('s3')

INPUT_BUCKET = 'iu-sheild-scraper-bucket'
INPUT_PREFIX = 'scrapes/'          # raw folder
OUTPUT_BUCKET = 'iu-sheild-scraper-bucket'
OUTPUT_PREFIX = 'cleaned/'          # final cleaned output

def clean_record(record):
    """Clean a single soccer record."""
    return {
        "team": record["team"],
        "GP": int(record["GP"]),
        "W": int(record["W"]),
        "D": int(record["D"]),
        "L": int(record["L"]),
        "F": int(record["F"]),
        "A": int(record["A"]),
        "GD": int(record["GD"].replace("+", "").replace("−", "-").strip()),
        "P": int(record["P"])
    }

def main():
    # 1. List all files inside scrapes/
    response = s3.list_objects_v2(Bucket=INPUT_BUCKET, Prefix=INPUT_PREFIX)

    if 'Contents' not in response:
        print("No files found in scrapes/ folder.")
        return

    for obj in response['Contents']:
        input_key = obj['Key']
        
        if not input_key.endswith('.json') or 'scraped_soccer_stats.json' in input_key:
            continue  # Skip non-json files or base file

        print(f"Processing file: {input_key}")

        # 2. Download file
        raw_obj = s3.get_object(Bucket=INPUT_BUCKET, Key=input_key)
        raw_data = json.loads(raw_obj['Body'].read())

        # 3. Clean records
        cleaned_records = [clean_record(r) for r in raw_data]

        # 4. Convert to NDJSON
        ndjson_content = '\n'.join(json.dumps(record) for record in cleaned_records)

        # 5. Prepare output path dynamically
        filename = input_key.split('/')[-1]  # scraped_soccer_stats_league1.json

        # Extract league info from filename (e.g., league1, league2)
        if 'league' in filename:
            league_part = filename.split('league')[-1].replace('.json', '')
            league_folder = f'league{league_part}'
        else:
            league_folder = 'other'

        # New output key format
        cleaned_filename = filename.replace('scraped_soccer_stats', 'scraped_soccer_stats_cleaned')
        output_key = f"{OUTPUT_PREFIX}{league_folder}/{cleaned_filename}"

        # 6. Upload cleaned NDJSON
        s3.put_object(
            Bucket=OUTPUT_BUCKET,
            Key=output_key,
            Body=ndjson_content.encode('utf-8'),
            ContentType='application/json'
        )

        print(f"✅ Uploaded cleaned NDJSON to s3://{OUTPUT_BUCKET}/{output_key}")

if __name__ == "__main__":
    main()
