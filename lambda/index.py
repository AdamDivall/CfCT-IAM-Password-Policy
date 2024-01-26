import boto3
import cfnresponse
import os
import sys
from botocore.exceptions import ClientError

EnvMaxPasswordAge = os.environ['MAXPASSWORDAGE']
EnvMinPasswordLength = os.environ['MINPASSWORDLENGTH']
EnvRequireUppercaseChars = os.environ['REQUIREUPPERCASECHARS']
EnvRequireLowercaseChars = os.environ['REQUIRELOWERCASECHARS']
EnvRequireNumbers = os.environ['REQUIRENUMBERS']
EnvRequireSymbols = os.environ['REQUIRESYMBOLS']
EnvPasswordReusePrevention = os.environ['PASSWORDREUSEPREVENTION']

iam_client = boto3.client('iam')

def lambda_handler(event,context):
    props = event['ResourceProperties']
    if (event['RequestType'] == 'Create' or event['RequestType'] == 'Update'):
        try:
            iam_client.update_account_password_policy(
                AllowUsersToChangePassword=True,
                HardExpiry=False,
                MaxPasswordAge=int(EnvMaxPasswordAge),
                MinimumPasswordLength=int(EnvMinPasswordLength),
                RequireLowercaseCharacters=bool(EnvRequireLowercaseChars),
                RequireNumbers=bool(EnvRequireNumbers),
                RequireSymbols=bool(EnvRequireSymbols),
                RequireUppercaseCharacters=bool(EnvRequireUppercaseChars),
                PasswordReusePrevention=int(EnvPasswordReusePrevention)
            )
        except ClientError as ex:
            print(ex.response['Error']['Message'])
            print("Response: FAILED")
            cfnresponse.send(event, context, cfnresponse.FAILED, ex.response)

    elif (event['RequestType'] == 'Delete'):
        try:
            iam_client.delete_account_password_policy()
        except ClientError as ex:
            print(ex.response['Error']['Message'])
            print("Respond: FAILED")

            cfnresponse.send(event, context, cfnresponse.FAILED, ex.response)

    print("Response: SUCCESS")
    cfnresponse.send(event, context, cfnresponse.SUCCESS, {})
    sys.exit(0)