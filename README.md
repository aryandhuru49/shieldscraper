# ShieldScraper: Automated Soccer League Stats Pipeline

ShieldScraper is an automated, secure, and scalable cloud-based data engineering pipeline designed for advanced web scraping, data transformation, storage, and visualization. Implemented using a robust suite of Amazon Web Services (AWS), ShieldScraper integrates ECS Fargate for container orchestration, Glue for Extract-Transform-Load (ETL) processes, DynamoDB for scalable data storage, Athena for querying capabilities, and QuickSight for intuitive data visualization. The pipeline employs real-time monitoring and automated alerting, ensuring system robustness, fault tolerance, and operational efficiency.

---

## Contributors
- VarunKumar Sonaware
- Aryan Dhuru
- Suhana Ambol
- Shivali Mate

---

## Folder Structure

```bash
.
├── shieldscraper_docker       # AWS files
├── job_spider.py              # Scrapy spider for League 1
├── job_spider_2.py            # Spider for League 2
├── job_spider_3.py            # Spider for League 3
├── job_spider_4.py            # Spider for League 4
├── job_spider_5.py            # Spider for League 5
├── fargate_handler.py         # Runs all spiders and uploads output to S3
├── Dockerfile                 # Container for ECS/Fargate
├── requirements.txt           # Python dependencies
└── README.md
```

## Requirements

- Python 3.9+
- Docker
- AWS CLI configured (`aws configure`)
- AWS Account with:
  - S3 bucket (e.g., `iu-shield-scraper-bucket`)
  - IAM role with permissions for S3, ECS, Fargate
  - CloudWatch for logs

## Environment Variables

Set these before running the container:

```bash
export RAW_BUCKET=iu-shield-scraper-bucket
```

## Run Locally with Docker

```bash
docker build -t shieldscraper .
docker run --rm -e RAW_BUCKET=iu-shield-scraper-bucket shieldscraper
```

## Deploy to AWS Fargate

Push Docker image to ECR:

```bash
aws ecr get-login-password --region us-east-1 | \
docker login --username AWS --password-stdin <aws_account_id>.dkr.ecr.us-east-1.amazonaws.com

docker tag shieldscraper <aws_account_id>.dkr.ecr.us-east-1.amazonaws.com/shieldscraper:latest
docker push <aws_account_id>.dkr.ecr.us-east-1.amazonaws.com/shieldscraper:latest
```

Create ECS Task Definition:

- Use image from ECR
- Set `RAW_BUCKET` as environment variable
- Assign IAM role with S3 access
- Launch via ECS task or automate with EventBridge

## Output Format (S3)

Uploaded files follow this format:

```bash
scrapes/
  scraped_English_Premier_League.json
  scraped_La_Liga.json
  scraped_Bundesliga.json
  ...
```

Each file is NDJSON:

```json
{"Team": "Arsenal", "Games Played": "30", "Wins": "22", ...}
{"Team": "Manchester City", "Games Played": "30", "Wins": "21", ...}
```

## Use with AWS Athena

- Run AWS Glue Crawler on `scrapes/` path
- Create table with JSON classifier
- Query with Athena:

```sql
SELECT * FROM soccer_stats_premier_league LIMIT 10;
```
