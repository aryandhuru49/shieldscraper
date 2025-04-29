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
    "https://www.espn.com/soccer/standings/_/league/eng.1",
    "https://www.espn.com/soccer/standings/_/league/fra.1",
    "https://www.espn.com/soccer/standings/_/league/esp.1",
    "https://www.espn.com/soccer/standings/_/league/ita.1",
    "https://www.espn.com/soccer/standings/_/league/ger.1",
]

def upload_to_s3(local_file, s3_key):
    with open(local_file, "rb") as f:
        s3.put_object(
            Bucket=RAW_BUCKET,
            Key=f"scrapes/{s3_key}",
            Body=f.read(),
            ContentType='application/json'
        )
    print(f"Uploaded {s3_key} to S3!")

@defer.inlineCallbacks
def crawl():
    runner = CrawlerRunner()
    
    spiders = [
        (JobSpider, start_urls[0], output_files[0]),
        (JobSpider2, start_urls[1], output_files[1]),
        (JobSpider3, start_urls[2], output_files[2]),
        (JobSpider4, start_urls[3], output_files[3]),
        (JobSpider5, start_urls[4], output_files[4]),
    ]
    
    for spider_cls, start_url, output_file in spiders:
        settings = {
            'FEEDS': {
                output_file: {'format': 'json', 'overwrite': True}
            },
            'LOG_ENABLED': True
        }
        runner = CrawlerRunner(settings)
        yield runner.crawl(spider_cls, start_url=start_url, output_file=output_file)
    
    reactor.stop()


if __name__ == "__main__":
    try:
        crawl()
        reactor.run()

        for file_name in output_files:
            upload_to_s3(file_name, file_name)

        print("All leagues scraped and uploaded successfully!")

    except Exception as e:
        print(str(e))
        raise