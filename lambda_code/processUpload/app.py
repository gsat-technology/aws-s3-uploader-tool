
import os
import json
import hashlib
import urllib

import boto3
import botocore


s3_client = boto3.client('s3')
sns_client = boto3.client('sns')

bucket = os.environ['s3_bucket']
topic = os.environ['sns_arn']

def notify(_id):
    message = {"foo": "bar"}

    try:
        response = sns_client.publish(
            TargetArn=topic,
            Message='file has been uploaded for id: {}'.format(_id),
        )
        return True
    except:
        print('could not publish to SNS topic')
        return False

def handler(event, context):
    """
    processUpload
    """
    print('starting...')

    key = event['Records'][0]['s3']['object']['key']
    bucket = event['Records'][0]['s3']['bucket']['name']

    #notify admin
    notify(key)

    encoded_id = key.split('.zip')[0].split('uploads/')[1]
    _id = urllib.unquote(encoded_id).decode('utf8')

    hash_object = hashlib.md5(_id)
    id_hash = hash_object.hexdigest()[:8]

    delete_key = 'public/' + id_hash + '/index.html'

    response = s3_client.delete_object(
        Bucket=bucket,
        Key=delete_key)

    status_code = response['ResponseMetadata']['HTTPStatusCode']

    was_delete = False

    if str(status_code)[0] == '2':
        was_deleted = True

    details = {
        'key': key,
        'bucket': bucket,
        'delete_key': delete_key,
        'was_deleted': was_deleted,
        'notification_success': notify(_id)
    }

    print(json.dumps(details))

    print('done')

    return {}
