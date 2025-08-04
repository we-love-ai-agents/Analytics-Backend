from fastapi import FastAPI, Query
from typing import Optional, Dict, Any
import boto3

app = FastAPI()

dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
table = dynamodb.Table('AbandonedBag')

@app.get("/getItems")
def get_items(limit: int = Query(10), last_key: Optional[str] = None):
    # Construct DynamoDB query arguments
    query_args: Dict[str, Any] = {
        "Limit": limit,
    }

    if last_key:
        # Decode the last_key if it's encoded (e.g., from base64 or JSON)
        import json
        query_args["ExclusiveStartKey"] = json.loads(last_key)
    
    response = table.scan(**query_args)  # Use .query(...) for queries by key

    items = response.get('Items', [])
    last_evaluated_key = response.get('LastEvaluatedKey')

    # Encode the LastEvaluatedKey for safe passing in URLs
    encoded_last_key = None
    if last_evaluated_key:
        import json
        encoded_last_key = json.dumps(last_evaluated_key)

    return {
        "items": items,
        "last_key": encoded_last_key,
        "limit": limit,
    }