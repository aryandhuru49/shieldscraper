import json
import boto3
import requests
from bs4 import BeautifulSoup

s3 = boto3.client('s3')

# Read bucket name from environment variable
import os
RAW_BUCKET = os.environ['RAW_BUCKET']

def fetch_espn_page(url):
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    return response.content

def parse_espn_data(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    page_title = soup.title.string if soup.title else 'No Title'
    
    # You can add more specific parsing logic here
    return {
        'page_title': page_title,
    }

def lambda_handler(event, context):
    try:
        url = event['url']
        html = fetch_espn_page(url)
        parsed_data = parse_espn_data(html)
        
        # Save to S3
        filename = url.split('/')[-1] or 'index'
        s3.put_object(
            Bucket=RAW_BUCKET,
            Key=f"scrapes/{filename}.json",
            Body=json.dumps(parsed_data),
            ContentType='application/json'
        )
        
        return {
            'statusCode': 200,
            'body': 'Scrape and upload successful!'
        }
        
    except Exception as e:
        print(str(e))
        raise
