#!/usr/bin/env bash

WORKSPACE_LOCATION=$(pwd)
SCRIPT_FILE_NAME=sample.py
mkdir -p ${WORKSPACE_LOCATION}/src
vim ${WORKSPACE_LOCATION}/src/${SCRIPT_FILE_NAME}


docker run -it -v ~/.aws:/home/glue_user/.aws -v $WORKSPACE_LOCATION:/home/glue_user/workspace/ -e AWS_PROFILE=$PROFILE_NAME -e DISABLE_SSL=true --rm -p 4040:4040 -p 18080:18080 --name glue_spark_submit amazon/aws-glue-libs:glue_libs_4.0.0_image_01 spark-submit /home/glue_user/workspace/src/$SCRIPT_FILE_NAME