import os
import hashlib
from cStringIO import StringIO
import json

import boto3
from jinja2 import Template


client = boto3.client('s3')
bucket = os.environ['s3_bucket']

def handler(event, context):
    """
    generatePresignPOST
    """
    print('starting...')

    forms = event['forms']

    print(len(forms))

    for form in forms:

        _id = form['id']
        title = form['title']
        subtitle = form['subtitle']
        instructions = form['instructions']
        expires = form['expires']
        bucket = os.environ['s3_bucket']

        #hashed id for link path
        hash_object = hashlib.md5(_id)
        id_hash = hash_object.hexdigest()[:8]

        presign = client.generate_presigned_post(
                                            Bucket=bucket, Key='uploads/' + _id + '.zip',
                                            Fields=None,
                                            Conditions=None,
                                            ExpiresIn=expires)

        with open('template.index.html') as template_f:
            template = Template(template_f.read())

        tmp = template.render(
                            url=presign['url'],
                            policy=presign['fields']['policy'],
                            AWSAccessKeyId=presign['fields']['AWSAccessKeyId'],
                            x_amz_security_token=presign['fields']['x-amz-security-token'],
                            key=presign['fields']['key'],
                            signature=presign['fields']['signature'],
                            title=title,
                            subtitle=subtitle,
                            instructions=instructions)

        #write out to s3
        track_f = StringIO(tmp)
        track_f.seek(0)

        public_s3_key = 'public/' + id_hash + '/index.html'

        s3_response = client.put_object(
                                Body=track_f,
                                Bucket=bucket,
                                Key=public_s3_key,
                                ContentType='text/html'
                                    )

        #get the link
        link = '{}/{}/{}'.format(client.meta.endpoint_url, bucket, public_s3_key)

        details = {
            'presign': presign,
            'id': _id,
            'id_uuid': id_hash,
            'bucket': bucket,
            'form_link': link
        }

        print(json.dumps(details))

    print('done')

    return details
