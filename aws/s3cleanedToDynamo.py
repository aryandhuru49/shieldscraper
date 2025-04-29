# import json
# import boto3

# def lambda_handler(event, context):
#     s3 = boto3.client('s3')
#     dynamodb = boto3.resource('dynamodb', region_name='us-east-1')

#     BUCKET_NAME = 'iu-sheild-scraper-bucket'
#     PREFIX = 'cleaned/'

#     response = s3.list_objects_v2(Bucket=BUCKET_NAME, Prefix=PREFIX)

#     if 'Contents' not in response:
#         return {
#             'statusCode': 404,
#             'body': json.dumps('No cleaned files found.')
#         }

#     for obj in response['Contents']:
#         object_key = obj['Key']

#         if not object_key.endswith('.json'):
#             continue

#         # Extract league name (e.g., league1, league2)
#         filename = object_key.split('/')[-1]
#         league_part = filename.replace('scraped_soccer_stats_cleaned_', '').replace('.json', '')
#         table_name = f'SoccerStats_{league_part.capitalize()}'

#         print(f"Uploading data from {object_key} to table {table_name}")

#         try:
#             # Get the S3 object content
#             s3_object = s3.get_object(Bucket=BUCKET_NAME, Key=object_key)
#             content = s3_object['Body'].read().decode('utf-8').strip()

#             # Load JSON or NDJSON
#             records = []
#             try:
#                 data = json.loads(content)
#                 if isinstance(data, list):
#                     records = data
#                 else:
#                     raise ValueError("Not a list")
#             except Exception:
#                 for line in content.splitlines():
#                     if line.strip():
#                         records.append(json.loads(line))

#             # Upload into the correct DynamoDB table
#             table = dynamodb.Table(table_name)
#             for record in records:
#                 try:
#                     table.delete_item(Key={'team': record['team']})
#                     table.put_item(Item=record)
#                 except Exception as e:
#                     print(f"Error replacing item {record}: {e}")

#             print(f"✅ Successfully uploaded {len(records)} items to {table_name}")

#         except Exception as e:
#             print(f"⚠️ Error processing {object_key}: {e}")

#     return {
#         'statusCode': 200,
#         'body': json.dumps('✅ All files uploaded into their respective DynamoDB tables!')
#     }






import json
import boto3

def lambda_handler(event, context):
    s3 = boto3.client('s3')
    dynamodb = boto3.resource('dynamodb', region_name='us-east-1')

    BUCKET_NAME = 'iu-sheild-scraper-bucket'
    PREFIX = 'cleaned/'

    response = s3.list_objects_v2(Bucket=BUCKET_NAME, Prefix=PREFIX)

    if 'Contents' not in response:
        return {
            'statusCode': 404,
            'body': json.dumps('No cleaned files found.')
        }

    for obj in response['Contents']:
        object_key = obj['Key']

        if not object_key.endswith('.json'):
            continue

        # Extract league name
        # filename = object_key.split('/')[-1]
        league_part = filename.replace('.json', '')
        table_name = f'SoccerStats_{league_part.capitalize()}'

        print(f"Uploading data from {object_key} to table {table_name}")

        try:
            # Get the S3 object content
            s3_object = s3.get_object(Bucket=BUCKET_NAME, Key=object_key)
            content = s3_object['Body'].read().decode('utf-8').strip()

            # Load JSON or NDJSON
            records = []
            try:
                data = json.loads(content)
                if isinstance(data, list):
                    records = data
                else:
                    raise ValueError("Not a list")
            except Exception:
                for line in content.splitlines():
                    if line.strip():
                        records.append(json.loads(line))

            # Upload into the correct DynamoDB table
            table = dynamodb.Table(table_name)

            # ⚡ Step 1: Scan and delete all existing records
            scan = table.scan(ProjectionExpression='#k', ExpressionAttributeNames={'#k': 'team'})
            with table.batch_writer() as batch:
                for item in scan['Items']:
                    batch.delete_item(Key={'team': item['team']})
            print(f"✅ Cleared all existing items from {table_name}")

            # ⚡ Step 2: Upload fresh records
            with table.batch_writer() as batch:
                for record in records:
                    batch.put_item(Item=record)

            print(f"✅ Successfully uploaded {len(records)} new items to {table_name}")

        except Exception as e:
            print(f"⚠️ Error processing {object_key}: {e}")

    return {
        'statusCode': 200,
        'body': json.dumps('✅ All files replaced into their respective DynamoDB tables!')
    }
