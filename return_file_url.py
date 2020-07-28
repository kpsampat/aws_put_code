from rest_framework.response import Response
from phoenix.settings import *
import boto3
import boto
import sys
import random
from botocore.errorfactory import ClientError

class AWSFileUpload:

    def aws_put(self, folder, fileName, bucket_name):
        try:
            s3 = boto3.resource('s3', region_name='ap-southeast-1', aws_access_key_id=AWS_S3_ACCESS_KEY_ID, aws_secret_access_key=AWS_S3_SECRET_ACCESS_KEY)
            attachment = open(folder+'/'+fileName, "rb").read()
            response = s3.Object(bucket_name, fileName).put(Body=attachment, ACL='public-read', Key=fileName)
            if response['ResponseMetadata']['HTTPStatusCode'] == 200 or response['ResponseMetadata']['HTTPStatusCode'] == 201:
                print(response['ResponseMetadata']['HTTPStatusCode'])
            return Response('success', status=200)
        except Exception as e:
            return Response('fail',status=404)


    def get_url_of_file(self,fileName, attachment,bucket_name):
        try:
            s3 = boto3.resource('s3', region_name='ap-southeast-1', aws_access_key_id=AWS_S3_ACCESS_KEY_ID, aws_secret_access_key=AWS_S3_SECRET_ACCESS_KEY)
            response = s3.Object(bucket_name, fileName).put(Body=attachment, ACL='public-read', Key=fileName)
            if response:
                location = boto3.client('s3', region_name="ap-south-1", aws_access_key_id=AWS_S3_ACCESS_KEY_ID,
                                        aws_secret_access_key=AWS_S3_SECRET_ACCESS_KEY).get_bucket_location(
                    Bucket=bucket_name)['LocationConstraint']
                key = fileName
                url = "https://s3-%s.amazonaws.com/%s/%s" % (location, bucket_name, key)
                print(url)
                return url
            else:
                return "Error in file upload"
        except Exception as e:
            print(e)


    def create_bucket(self, bucket_name):
        try:
            if bucket_name is not None and bucket_name != "":
                s3 = boto3.resource('s3', region_name='ap-southeast-1', aws_access_key_id=AWS_S3_ACCESS_KEY_ID,
                                    aws_secret_access_key=AWS_S3_SECRET_ACCESS_KEY)
                res = s3.create_bucket(Bucket=bucket_name, ACL='public-read', CreateBucketConfiguration={'LocationConstraint': 'ap-southeast-1'})
                if bool(res) == True:
                    return True
                else:
                    return False
        except Exception as e:
            print("line number of error is ....{}".format(sys.exc_info()[-1].tb_lineno), e)
            return e


    def get_url_of_bucket(self,bucket_name):
        try:
            s3 = boto3.resource('s3', region_name='ap-southeast-1', aws_access_key_id=AWS_S3_ACCESS_KEY_ID,
                                aws_secret_access_key=AWS_S3_SECRET_ACCESS_KEY)
            location = boto3.client('s3', region_name="ap-south-1", aws_access_key_id=AWS_S3_ACCESS_KEY_ID,
                                aws_secret_access_key=AWS_S3_SECRET_ACCESS_KEY).get_bucket_location(
                Bucket=bucket_name)['LocationConstraint']
            url = "https://s3-%s.amazonaws.com/%s/" % (location, bucket_name)
            return url
        except Exception as e:
            print(e)


    def check_bucket_exists(self,bucket_name):
        try:
            s3 = boto3.resource('s3', region_name='ap-southeast-1', aws_access_key_id=AWS_S3_ACCESS_KEY_ID, aws_secret_access_key=AWS_S3_SECRET_ACCESS_KEY)
            find_bucket = s3.Bucket(bucket_name) in s3.buckets.all()
            if find_bucket == True:
                return True
            else:
                return False
        except Exception as e:
            print(e)

    def document_upload_handler(self, account_id, company_id, filename, attachment):

        try:

            if account_id is not None and account_id != "" and company_id is not None and company_id != "" and filename is not None and attachment is not None:

                # url_of_file = ""
                # company_id = str(company_id)
                # account_id = str(account_id)
                # company_id = company_id.strip()
                # account_id = account_id.strip()
                # bucket_name = 'phoenixbmro'+str(company_id) + str(account_id)

                # if check_if_bucket_exists is not True:
                #     self.create_bucket(bucket_name)

                # filename = self._make_filename_unique(filename)
                # url_of_file = self.get_url_of_file(filename, attachment, bucket_name)
                # print(url_of_file)

                url_of_file = ""
                bucket_name = self.get_bucket_for_current_environment()

                company_id = str(company_id)
                account_id = str(account_id)
                company_id = company_id.strip()
                account_id = account_id.strip()

                folder_name = 'phoenix' + str(company_id) + str(account_id)

                is_folder_exists = self.folder_exists(bucket_name, folder_name)

                if is_folder_exists is not True:
                    self.create_folder(bucket_name,folder_name)

                filename = self._make_filename_unique(filename)

                url_of_file = self.get_url_of_file(folder_name + '/' + filename, attachment, bucket_name)

                return url_of_file

        except Exception as e:
            print("Unhandled Exception occured at "+__file__+" on line number {} raised Exception is -> ".format(sys.exc_info()[2].tb_lineno), e)

    def image_upload_handler(self, filename, attachment):

        try:

            if  filename is not None and attachment is not None:

                # url_of_file = ""
                # bucket_name = 'bulkmro'
                # check_if_bucket_exists = self.check_bucket_exists(bucket_name)
                # print("bucket_name "+bucket_name)
                # print("check_if_bucket_exists ")
                # print(check_if_bucket_exists)
                # if check_if_bucket_exists is not True:
                #     self.create_bucket(bucket_name)

                # filename = self._make_filename_unique(filename)
                # url_of_file = self.get_url_of_file(filename, attachment, bucket_name)
                # print(url_of_file)

                url_of_file = ""
                bucket_name = self.get_bucket_for_current_environment()
                folder_name = 'images'

                is_folder_exists = self.folder_exists(bucket_name, folder_name)

                if is_folder_exists is not True:
                    self.create_folder(bucket_name,folder_name)

                filename = self._make_filename_unique(filename)
                url_of_file = self.get_url_of_file(folder_name + '/' + filename, attachment, bucket_name)
                print(url_of_file)

                return url_of_file

        except Exception as e:
            print("Unhandled Exception occured at "+__file__+" on line number {} raised Exception is -> ".format(sys.exc_info()[2].tb_lineno), e)



    def _make_filename_unique(self,filename):

        if filename != "" and filename is not None:

            splitted = filename.split('.')

            rand_int = random.randint(10000,99999)

            rand_int = str(rand_int)

            splitted[0]=splitted[0]+rand_int

            filename = '.'.join(splitted)

        return filename


    def create_folder(self, bucket_name, folder_name):

        if folder_name is not None and folder_name != "" and bucket_name is not None and bucket_name != "":
            
            try:
                
                s3 = boto3.resource('s3', region_name='ap-southeast-1', aws_access_key_id=AWS_S3_ACCESS_KEY_ID, aws_secret_access_key=AWS_S3_SECRET_ACCESS_KEY)

                response = s3.Object(bucket_name, folder_name+'/').put(ACL='public-read', Key=folder_name+'/')

                if response['ResponseMetadata']['HTTPStatusCode'] == 200 or response['ResponseMetadata']['HTTPStatusCode'] == 201:
                    print(response['ResponseMetadata']['HTTPStatusCode'])
                    return True

            except Exception as e:
                print("Unhandled Exception occured at "+__file__+" on line number {} raised Exception is -> ".format(sys.exc_info()[2].tb_lineno), e)
                return False

    def folder_exists(self, bucket_name, folder_name):        

        if folder_name is not None and folder_name != "" and bucket_name is not None and bucket_name != "":
            
            try:
                
                s3 = boto3.resource('s3', region_name='ap-southeast-1', aws_access_key_id=AWS_S3_ACCESS_KEY_ID, aws_secret_access_key=AWS_S3_SECRET_ACCESS_KEY)
                
                bucket = s3.Bucket(bucket_name)

                objs = list(bucket.objects.filter(Prefix=folder_name))

                if len(objs) != 0:
                    return True
                else:
                    return False

            except ClientError:

                return False

    def get_bucket_for_current_environment(self):

        environment_bucket_map = ENVIRONMENT_TO_AWS_S3_BUCKET_MAP

        bucket = environment_bucket_map['default']
        base_dir_var = BASE_DIR  
        base_dir_var = base_dir_var.lower()
        
        print("get_bucket_for_current_environment")
        print(base_dir_var)
        for environment in environment_bucket_map:            
            
            index = base_dir_var.find(environment)
            print(index)
            if index != -1:
                bucket = environment_bucket_map[environment]
                print(bucket)

        print("get_bucket_for_current_environment")

        return bucket

        #
# s3 = boto3.resource('s3',region_name='ap-southeast-1',aws_access_key_id=Access,aws_secret_access_key=Secret_access_key)
# s3 = boto3.resource('s3',region_name='ap-southeast-1',aws_access_key_id='TEW',aws_secret_access_key='q2cvO7')
# attachment = open("/home/user1/cp_arc_template.xlsx", "rb").read()
# fileName = "Try.xlsx"
# response = s3.Object('mediaphoenix', fileName).put(Body=attachment, ACL='public-read', Key=fileName)
# location = boto3.client('s3', region_name="ap-south-1", aws_access_key_id='NLYFFW', aws_secret_access_key='uy2cvO7').get_bucket_location(Bucket='mediaphoenix')['LocationConstraint']
# key = "Try.xlsx"
# url = "https://s3-%s.amazonaws.com/%s/%s" % (location, bucket_name, key)
#
# #click on url

# import boto
# from boto.s3.key import Key
# import boto.s3.connection
#
# AWS_ACCESS_KEY_ID = '<access key>'
# AWS_SECRET_ACCESS_KEY = '<my secret key>'
# Bucketname = 'Bucket-name'
#
# >>> conn = boto.s3.connect_to_region('ap-south-1',
# ...       aws_access_key_id="NLYFFW",
# ...       aws_secret_access_key="qcvO7",
# ...       is_secure=True,
# ...       calling_format = boto.s3.connection.OrdinaryCallingFormat(),
# ...       )
# >>> bucket = conn.get_bucket(Bucketname)
#
# 80aecc8caf725c58ec5f76e5ae9b7088
#
#
# s3 = boto3.client('s3', region_name="ap-south-1", aws_access_key_id='MTEYFFW', aws_secret_access_key='qM922cvO7')
#
#
# boto3.client('s3', region_name="ap-south-1", aws_access_key_id='FFW', aws_secret_access_key='qMvO7').get_bucket_location(Bucket='mediaphoenix')['LocationConstraint']
#
# import boto3
# location = boto3.client('s3', region_name="ap-south-1", aws_access_key_id='LYFFW', aws_secret_access_key='bMvO7').get_bucket_location(Bucket='mediaphoenix')['LocationConstraint']
