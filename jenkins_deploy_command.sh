#!/bin/bash

ScriptLocalPath="$1"
ScriptS3Path="$2"
TemplateFile="$3"
StackName="$4"
Env="$5"

echo "script local path: $ScriptLocalPath"
echo "script s3 path: $ScriptS3Path"
echo "cloudformation file path: $TemplateFile"
echo "stack name: $StackName"
echo "selected Env: $Env"


aws s3 cp "$ScriptLocalPath" "$ScriptS3Path"


describe_stacks_output=$(aws cloudformation describe-stacks --stack-name "$StackName" 2>/dev/null)

if [ $? -eq 0 ]; then
  # update cloudformation stack
  echo "Updating stack: $StackName"
  aws cloudformation update-stack \
    --region cn-northwest-1 \
    --stack-name "$StackName" \
    --template-body "file://$TemplateFile" \
    --parameters ParameterKey=Env,ParameterValue="$Env"\
                 ParameterKey=ScriptS3Path,ParameterValue="$ScriptS3Path" \

else
  # create cloudformation stack
  echo "Creating new stack: $StackName"
  aws cloudformation create-stack \
    --region cn-northwest-1 \
    --stack-name "$StackName" \
    --template-body "file://$TemplateFile" \
    --parameters ParameterKey=Env,ParameterValue="$Env"\
                 ParameterKey=ScriptS3Path,ParameterValue="$ScriptS3Path" \

fi
