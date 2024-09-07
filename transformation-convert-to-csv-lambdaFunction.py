import json
import boto3
import pandas as pd

s3_client = boto3.client('s3')

def lambda_handler(event, context):
    # TODO implement
    source_bucket = event['Records'][0]['s3']['bucket']['name']
    object_key = event['Records'][0]['s3']['object']['key'] 
    
    target_bucket = 'zillow-cleaned-data-zone-csv-bucket-3'
    target_file_name = object_key[:-5]
    
    waiter = s3_client.get_waiter('object_exists')
    waiter.wait(Bucket=source_bucket, Key=object_key)
    
    response = s3_client.get_object(Bucket=source_bucket, Key=object_key)
    data = response['Body'].read().decode('utf-8')
    data = json.loads(data)
    
    f = []
    for i in data["results"]:
        f.append(i)
    df = pd.DataFrame(f)
    selected_columns = ['bathrooms', 'bedrooms', 'city', 'homeStatus', 'homeType',
                        'livingArea', 'price', 'rentZestimate', 'zipcode']
    df = df[selected_columns]
    
    csv_data = df.to_csv(index=False)
    
    object_key = f"{target_file_name}.csv"
    s3_client.put_object(Bucket=target_bucket, Key=object_key, Body=csv_data)
    
    return {
        'statusCode': 200,
        'body': json.dumps('CSV conversion and s3 upload completed successfully!')
    }
