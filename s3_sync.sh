#!/bin/bash
# test
OutputDir="s3://bots-taijitu-test-439314357471-flatted-data"
AthenaTableDir="s3://bots-taijitu-test-439314357471-athena-table-data"

# prod
OutputDir="s3://bots-taijitu-prod-439413396736-flatted-data"
AthenaTableDir="s3://bots-taijitu-prod-439413396736-athena-table-data"

AWS_REGION=cn-northwest-1

echo "Syncing Athena launch entries bucket..."
aws s3 sync "${OutputDir}/launch-entries/" \
    "${AthenaTableDir}/launch-entries/" \
    --exclude "*_spark_metadata/*" \
    --exclude "*_spark_metadata*" \
    --exclude "*year=__HIVE_DEFAULT_PARTITION__/*" \
    --region ${AWS_REGION}
