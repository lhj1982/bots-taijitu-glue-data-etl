#!/usr/bin/env bash

dt=$1
if [ -z "$dt" ]; then
    dt=`date '+%Y-%m-%d'`
fi
year=`date '+%Y'`
month=`date '+%m'`
day=`date '+%d'`

echo "Syncing Athena launch entries bucket..."
aws s3 sync "${OutputDir}/launch-entries/" \
    "${AthenaTableDir}/launch-entries/" \
    --exclude "*_spark_metadata/*" \
    --exclude "*_spark_metadata*" \
    --exclude "*year=__HIVE_DEFAULT_PARTITION__/*" \
    --region cn-northwest-1
