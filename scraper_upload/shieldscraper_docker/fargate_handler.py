import os
import json
import boto3
from scrapy.crawler import CrawlerRunner
from twisted.internet import reactor, defer

from job_spider import JobSpider
from job_spider_2 import JobSpider2
from job_spider_3 import JobSpider3
from job_spider_4 import JobSpider4
from job_spider_5 import JobSpider5

# Setup S3 client
s3 = boto3.client('s3')
RAW_BUCKET = os.environ['RAW_BUCKET']

output_files = [
    "scraped_soccer_stats_league1.json",
    "scraped_soccer_stats_league2.json",
    "scraped_soccer_stats_league3.json",
    "scraped_soccer_stats_league4.json",
    "scraped_soccer_stats_league5.json",
]

start_urls = [
    "https://www.espn.com/soccer/table/_/league/",
    "https://www.espn.com/soccer/standings/_/league/esp.1",
    "https://www.espn.com/soccer/standings/_/league/eng.1",
    "https://www.espn.com/soccer/standings/_/league/ita.1",
    "https://www.espn.com/soccer/standings/_/league/ger.1",
]

# Upload file to S3
def upload_to_s3(local_file, s3_key):
    with open(local_file, "rb") as f:
        s3.put_object(
            Bucket=RAW_BUCKET,
            Key=f"scrapes/{s3_key}",
            Body=f.read(),
            ContentType='application/json'
        )
    print(f"✅ Uploaded {s3_key} to S3!")

@defer.inlineCallbacks
def crawl():
    runner = CrawlerRunner(settings={
        'FEEDS': {file_name: {'format': 'json', 'overwrite': True} for file_name in output_files},
        'LOG_ENABLED': True
    })

    yield runner.crawl(JobSpider, start_url=start_urls[0], output_file=output_files[0])
    yield runner.crawl(JobSpider2, start_url=start_urls[1], output_file=output_files[1])
    yield runner.crawl(JobSpider3, start_url=start_urls[2], output_file=output_files[2])
    yield runner.crawl(JobSpider4, start_url=start_urls[3], output_file=output_files[3])
    yield runner.crawl(JobSpider5, start_url=start_urls[4], output_file=output_files[4])

    reactor.stop()

if __name__ == "__main__":
    try:
        crawl()
        reactor.run()

        for file_name in output_files:
            upload_to_s3(file_name, file_name)

        print("🎯 All leagues scraped and uploaded successfully!")

    except Exception as e:
        print(str(e))
        raise
