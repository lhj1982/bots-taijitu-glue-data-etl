#!/bin/bash

SCRIPT_LOCAL_PATH="$1"
SCRIPT_S3_PATH="$2"
TEMPLATE_FILE="$3"
STACK_NAME="$4"
ENV="$5"

echo "script local path: $SCRIPT_LOCAL_PATH"
echo "script s3 path: $SCRIPT_S3_PATH"
echo "cloudformation file path: $TEMPLATE_FILE"
echo "stack name: $STACK_NAME"
echo "selected env: $ENV"


aws s3 cp "$SCRIPT_LOCAL_PATH" "$SCRIPT_S3_PATH"


# 检查堆栈是否存在
#describe_stacks_output=$(aws cloudformation describe-stacks --stack-name "$STACK_NAME" 2>/dev/null)
#
#if [ $? -eq 0 ]; then
#  # 堆栈存在，执行更新操作
#  echo "Updating stack: $STACK_NAME"
#  aws cloudformation update-stack \
#    --region cn-northwest-1 \
#    --stack-name "$STACK_NAME" \
#    --template-body "file://$TEMPLATE_FILE" \
#    --parameters ParameterKey=ENV,ParameterValue="$ENV" ParameterKey=SCRIPT_S3_PATH,ParameterValue="$SCRIPT_S3_PATH" \
#
#else
#  # 堆栈不存在，执行创建操作
#  echo "Creating new stack: $STACK_NAME"
#  aws cloudformation create-stack \
#    --region cn-northwest-1 \
#    --stack-name "$STACK_NAME" \
#    --template-body "file://$TEMPLATE_FILE" \
#    --parameters ParameterKey=ENV,ParameterValue="$ENV" ParameterKey=SCRIPT_S3_PATH,ParameterValue="$SCRIPT_S3_PATH" \
#fi
