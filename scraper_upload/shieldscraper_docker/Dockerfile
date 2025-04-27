FROM python:3.9-slim

# Install packages
RUN pip install scrapy boto3

# Copy function code
COPY fargate_handler.py .
COPY job_spider.py .

# Set the CMD properly for Fargate 
CMD ["python", "fargate_handler.py"]



