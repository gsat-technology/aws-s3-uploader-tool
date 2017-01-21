## aws-s3-uploader-tool


### deploy

#### upload lambda deployment packages to s3

```
./lambda\_deploy.sh <bucket_name>
```

packages will be uploaded to `<bucket_name>/apps/aws-s3-uploader-tool` which is where the lambda resources in the cloudformation template is expecting the zip files to be.

#### Create Cloudformation Stack

Create stack using `cf.yml`

- `Stack Name`: 'aws-s3-uploader-tool'
- `NotificationEmailAddress`: _notification emails will be sent to this address whenever someone uploads a file_
- `S3PublicBucket`: _html forms and uploaded files will be put in this bucket_
- `S3ResourceBucket`: _the bucket where you uploaded the lambdas (in the instructions above)_

#### Create some forms

Take a look at `sample_payload.json` and modify as needed.

Install [jq](https://stedolan.github.io/jq/download/) or the last line from the command below. jq is very useful for parsing JSON

```
aws lambda invoke \
    --function-name aws-s3-uploader-tool_generatePresignPOST \
    --payload file://sample_payload.json \
    outfile.txt && cat outfile.txt \
    | jq '.[] |  .id  + ": " +   .form_link' --raw-output
```
Example output:
```
person1: https://s3-ap-southeast-2.amazonaws.com/<bucket>/public/25bf0679/index.html
person2: https://s3-ap-southeast-2.amazonaws.com/<bucket>/public/7bc5facc/index.html
```
