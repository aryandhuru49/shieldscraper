FROM python:3.9-slim

# Install necessary Python packages
RUN pip install scrapy boto3 twisted

# Copy project files
COPY fargate_handler.py .
COPY job_spider.py .
COPY job_spider_2.py .
COPY job_spider_3.py .
COPY job_spider_4.py .
COPY job_spider_5.py .


# Set the command to run the handler
CMD ["python", "fargate_handler.py"]
