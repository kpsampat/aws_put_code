import boto3
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db import transaction

class AWSFileUpload(APIView):

    @transaction.atomic()
    def post(self, request, folder , fileName):
        #example folder in aws account ('Eg : mediaphoenix')
        try:

            s3 = boto3.resource('s3',region_name='us-east-1',aws_access_key_id='AKIA6F7PCUPMTKT3TJW3',aws_secret_access_key='0ABh1Bb9w+D8szWIoYo7R/UQAxqr6tkouheaiojy')

            attachment = open(folder+'/'+fileName, "rb").read()

            response = s3.Object(folder, fileName).put(Body=attachment)

            if response['ResponseMetadata']['HTTPStatusCode'] == 200 or response['ResponseMetadata']['HTTPStatusCode'] == 201:
                print(response['ResponseMetadata']['HTTPStatusCode'])

            return Response('success', status=200)

        except Exception as e:

            return Response('fail',status=404)
            
            
