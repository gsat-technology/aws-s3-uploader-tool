## aws-s3-uploader-tool

### About

This is an application of the S3 pre-signed url feature. Pre-signed urls can be created and shared with someone who then uses the pre-signed url as a target to POST a file.

The benefit of pre-signed urls is you do not need a set of personal AWS keys to use it e.g. you could give a pre-signed url to anyone and they can use it to upload a file to your s3 bucket.

A pre-signed url is really a combination of url plus a number of other parameters (documented in the table on [this page](https://aws.amazon.com/articles/1434)).

So this application shows how to automate the creation of pre-signed urls. It imagines a scenario where you (admin) want to quickly create custom forms to share with people so they can upload a file to your s3 bucket (e.g. maybe people frequently need to send you large files which can't be emailed because of the file size).

![alt tag](https://github.com/gsat-technology/aws-s3-uploader-tool/blob/master/resources/arch_diagram.png?raw=true)


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

_Note: expiry is in seconds_

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
To understand how this application works, goto one of the output urls. The page will look something like this:

![alt tag](https://github.com/gsat-technology/aws-s3-uploader-tool/blob/master/resources/form_screenshot.png?raw=true)

Notice that the url path contains **public/** - this is a section of the bucket that is publicly GETable by anyone (determined by the policy attached to the bucket)

Drop in a file and it will instantly upload. The file will be uploaded to the **uploads/** directory. This section is _not_ public.

Once the file is uploaded, a lambda function will be triggered and the html form will be removed.
