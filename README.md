# Introduction
The project contains several glue etl job definitions that read data from different sources (kinesis, kafka, s3 etc) to save them in the centralized S3 bucket in data account.

## Setup
* run application_account_resource.yaml in source aws account
* run data_account_resource.yaml in target data account
* run data_s3_resource.yaml in target data account

## Kinesis connection
Deploy glue etl job in the same account as kds is located

## Kafka connection

## Key Resources
All processed data should be saved under LITX aws account, 

# Deploy glue job using aws cli
Upload py file to S3 bucket

```
aws glue create-job --name python-redshift-test-cli --role role --command '{"Name" :  "pythonshell", "ScriptLocation" : "s3://MyBucket/python/library/redshift_test.py"}' 
     --connections Connections=connection-name --default-arguments '{"--extra-py-files" : ["s3://DOC-EXAMPLE-BUCKET/EGG-FILE", "s3://DOC-EXAMPLE-BUCKET/WHEEL-FILE"]}'
```

# Deploy and debug in local
Reference: https://towardsaws.com/how-to-run-aws-glue-jobs-locally-using-visual-studio-code-vs-code-127a9bb10bd1
## Prerequisites
awscli, docker vs code

## Setup
* AWS profile which is able to read S3
```
export AWS_PROFILE=<your-profile-name>
```
* Pull docker image
```
docker pull amazon/aws-glue-libs:glue_libs_4.0.0_image_01
```
* setup vs code, update workspace setting.json file
```
{
    "python.defaultInterpreterPath": "/usr/bin/python3",
    "python.analysis.extraPaths": [
        "/home/glue_user/aws-glue-libs/PyGlue.zip:/home/glue_user/spark/python/lib/py4j-0.10.9-src.zip:/home/glue_user/spark/python/",
    ]
}
```
* Run docker container
```
export PROFILE_NAME=<name-of-your-aws-profile>
export WORKSPACE_LOCATION=$(pwd)

docker run -it -v ~/.aws:/home/glue_user/.aws -v $WORKSPACE_LOCATION:/home/glue_user/workspace/ -e AWS_PROFILE=$PROFILE_NAME -e DISABLE_SSL=true --rm -p 4040:4040 -p 18080:18080 --name glue_pyspark amazon/aws-glue-libs:glue_libs_4.0.0_image_01 pyspark

```



Convert ipynb to python script
```
jupyter nbconvert --to script *.ipynb
```


# Put record to kinesis
```
aws kinesis put-record --stream-name launch-entry-eda-data-stream --partition-key 1 \
    --data "<base64 encoded string>" \
    --profile CommerceGCTest \
    --region cn-northwest-1
```

Launch entry example in ddb
```
{
 "id": "83f666b2-23ad-5c68-9ccc-1248e7005a6d",
 "appId": "com.nike.commerce.snkrs.ios",
 "channel": "SNKRS",
 "checkoutId": "d3e98748-94fe-476a-9097-24b9084a233d",
 "creationTimestamp": 1725238816172,
 "currency": "CNY",
 "forwardedFor": "114.227.98.25, 10.120.25.209, 58.222.47.172, 39.96.130.111",
 "geolocation": "null",
 "launchId": "24b75183-ced8-3ec8-978a-4dd3d735e892",
 "launchSkuStatus": "24b75183-ced8-3ec8-978a-4dd3d735e892:8b91811a-95ec-5099-ad5f-c25f1a4ca601:WINNER",
 "launchSkuStatusValidation": "24b75183-ced8-3ec8-978a-4dd3d735e892:8b91811a-95ec-5099-ad5f-c25f1a4ca601:WINNER:VALID",
 "locale": "zh_CN",
 "paymentStatus": "PENDING_PAYMENT",
 "paymentToken": "37086c07-d868-4a0f-a83e-769e9e6270ff",
 "postpayLink": "https://www.nike.com/omega",
 "postpayRetry": false,
 "rank": -1,
 "reentryPermitted": false,
 "reservationId": "P26cbda24e98d4bcdb75927a557df9b3d",
 "reservationJobId": "ed9a9e59-f6b9-4b9c-93ee-de211e628c66",
 "reservationTimestamp": 1725238922070,
 "retailPickupPerson": "null",
 "selectedTimestamp": 1725238925578,
 "shipping": "{\"recipient\":{\"firstName\":\"文杰\",\"lastName\":\"盛\",\"phoneNumber\":\"18112885616\"},\"address\":{\"address1\":\"荷花池街道荷花池公寓19-6号\",\"city\":\"常州市\",\"state\":\"CN-32\",\"postalCode\":\"213000\",\"country\":\"CN\",\"county\":\"钟楼区\"},\"method\":null,\"getBy\":{\"maxDate\":{\"dateTime\":\"2024-09-09T02:25:01.582Z\",\"timezone\":\"Asia/Shanghai\",\"precision\":\"DAY\"}}}",
 "skuId": "8b91811a-95ec-5099-ad5f-c25f1a4ca601",
 "sort": 151212521,
 "status": "WINNER",
 "totals": "{\"items\":{\"total\":1099.0,\"details\":{\"price\":1099.0,\"discount\":0.0}},\"taxes\":{\"details\":{\"items\":{\"type\":\"NOT_CALCULATED\"}}},\"fulfillment\":{\"total\":0.0,\"details\":{\"price\":0.0,\"discount\":0.0}}}",
 "traceContext": "v1:9655238fd3131624:702c742b47e20b6a:1",
 "trueClientIp": "114.227.98.25",
 "ttl": 1725843725,
 "upmId": "03c3403f-7d54-48f3-8ddb-f27d1ce611dd",
 "userAgent": "SNKRS/6.6.0 (prod; 2407181638; iOS 16.6.1; iPhone13,4)",
 "userType": "nike:plus",
 "validationSummary": "{\"result\":\"VALID\"}",
 "waitingReason": null
}
```

a ddb stream event looks like

## Insert
```
{
  "awsRegion": "cn-northwest-1",
  "eventID": "172c5e7f-abc5-4e1e-8a21-9dd707c3b52b",
  "eventName": "INSERT",
  "userIdentity": null,
  "recordFormat": "application/json",
  "tableName": "launch.winnerselector.entry",
  "dynamodb": {
    "ApproximateCreationDateTime": 1725851715838,
    "Keys": {
      "id": {
        "S": "83f666b2-23ad-5c68-9ccc-1248e7005aee"
      }
    },
    "NewImage": {
      "userAgent": {
        "S": "SNKRS/6.6.0 (prod; 2407181638; iOS 16.6.1; iPhone13,4)"
      },
      "traceContext": {
        "S": "v1:9655238fd3131624:702c742b47e20b6a:1"
      },
      "currency": {
        "S": "CNY"
      },
      "launchSkuStatusValidation": {
        "S": "24b75183-ced8-3ec8-978a-4dd3d735e892:8b91811a-95ec-5099-ad5f-c25f1a4ca601:WINNER:VALID"
      },
      "reservationJobId": {
        "S": "ed9a9e59-f6b9-4b9c-93ee-de211e628c66"
      },
      "userType": {
        "S": "nike:plus"
      },
      "status": {
        "S": "WINNER"
      },
      "retailPickupPerson": {
        "S": "null"
      },
      "ttl": {
        "N": "1725843725"
      },
      "launchId": {
        "S": "24b75183-ced8-3ec8-978a-4dd3d735e892"
      },
      "skuId": {
        "S": "8b91811a-95ec-5099-ad5f-c25f1a4ca601"
      },
      "channel": {
        "S": "SNKRS"
      },
      "geolocation": {
        "S": "null"
      },
      "shipping": {
        "S": "{\"recipient\":{\"firstName\":\"文杰\",\"lastName\":\"盛\",\"phoneNumber\":\"18112885616\"},\"address\":{\"address1\":\"荷花池街道荷花池公寓19-6号\",\"city\":\"常州市\",\"state\":\"CN-32\",\"postalCode\":\"213000\",\"country\":\"CN\",\"county\":\"钟楼区\"},\"method\":null,\"getBy\":{\"maxDate\":{\"dateTime\":\"2024-09-09T02:25:01.582Z\",\"timezone\":\"Asia/Shanghai\",\"precision\":\"DAY\"}}}"
      },
      "paymentToken": {
        "S": "37086c07-d868-4a0f-a83e-769e9e6270ff"
      },
      "postpayRetry": {
        "BOOL": false
      },
      "paymentStatus": {
        "S": "PENDING_PAYMENT"
      },
      "selectedTimestamp": {
        "N": "1725238925578"
      },
      "upmId": {
        "S": "03c3403f-7d54-48f3-8ddb-f27d1ce611dd"
      },
      "reservationId": {
        "S": "P26cbda24e98d4bcdb75927a557df9b3d"
      },
      "creationTimestamp": {
        "N": "1725238816172"
      },
      "waitingReason": {
        "NULL": true
      },
      "totals": {
        "S": "{\"items\":{\"total\":1099.0,\"details\":{\"price\":1099.0,\"discount\":0.0}},\"taxes\":{\"details\":{\"items\":{\"type\":\"NOT_CALCULATED\"}}},\"fulfillment\":{\"total\":0.0,\"details\":{\"price\":0.0,\"discount\":0.0}}}"
      },
      "validationSummary": {
        "S": "{\"result\":\"VALID\"}"
      },
      "sort": {
        "N": "151212521"
      },
      "id": {
        "S": "83f666b2-23ad-5c68-9ccc-1248e7005aee"
      },
      "checkoutId": {
        "S": "d3e98748-94fe-476a-9097-24b9084a233d"
      },
      "locale": {
        "S": "zh_CN"
      },
      "trueClientIp": {
        "S": "114.227.98.25"
      },
      "postpayLink": {
        "S": "https://www.nike.com/omega"
      },
      "reservationTimestamp": {
        "N": "1725238922070"
      },
      "rank": {
        "N": "-1"
      },
      "reentryPermitted": {
        "BOOL": false
      },
      "forwardedFor": {
        "S": "114.227.98.25, 10.120.25.209, 58.222.47.172, 39.96.130.111"
      },
      "launchSkuStatus": {
        "S": "24b75183-ced8-3ec8-978a-4dd3d735e892:8b91811a-95ec-5099-ad5f-c25f1a4ca601:WINNER"
      },
      "appId": {
        "S": "com.nike.commerce.snkrs.ios"
      }
    },
    "SizeBytes": 1749
  },
  "eventSource": "aws:dynamodb"
}
```

put record to kds directly
```
aws kinesis put-record --stream-name launch-entry-eda-data-stream --partition-key 1 --data "eyJhd3NSZWdpb24iOiJjbi1ub3J0aHdlc3QtMSIsImV2ZW50SUQiOiIxNzJjNWU3Zi1hYmM1LTRlMWUtOGEyMS05ZGQ3MDdjM2I1MmIiLCJldmVudE5hbWUiOiJJTlNFUlQiLCJ1c2VySWRlbnRpdHkiOm51bGwsInJlY29yZEZvcm1hdCI6ImFwcGxpY2F0aW9uL2pzb24iLCJ0YWJsZU5hbWUiOiJsYXVuY2gud2lubmVyc2VsZWN0b3IuZW50cnkiLCJkeW5hbW9kYiI6eyJBcHByb3hpbWF0ZUNyZWF0aW9uRGF0ZVRpbWUiOjE3MjU4NTE3MTU4MzgsIktleXMiOnsiaWQiOnsiUyI6IjgzZjY2NmIyLTIzYWQtNWM2OC05Y2NjLTEyNDhlNzAwNWFlZSJ9fSwiTmV3SW1hZ2UiOnsidXNlckFnZW50Ijp7IlMiOiJTTktSUy82LjYuMCAocHJvZDsgMjQwNzE4MTYzODsgaU9TIDE2LjYuMTsgaVBob25lMTMsNCkifSwidHJhY2VDb250ZXh0Ijp7IlMiOiJ2MTo5NjU1MjM4ZmQzMTMxNjI0OjcwMmM3NDJiNDdlMjBiNmE6MSJ9LCJjdXJyZW5jeSI6eyJTIjoiQ05ZIn0sImxhdW5jaFNrdVN0YXR1c1ZhbGlkYXRpb24iOnsiUyI6IjI0Yjc1MTgzLWNlZDgtM2VjOC05NzhhLTRkZDNkNzM1ZTg5Mjo4YjkxODExYS05NWVjLTUwOTktYWQ1Zi1jMjVmMWE0Y2E2MDE6V0lOTkVSOlZBTElEIn0sInJlc2VydmF0aW9uSm9iSWQiOnsiUyI6ImVkOWE5ZTU5LWY2YjktNGI5Yy05M2VlLWRlMjExZTYyOGM2NiJ9LCJ1c2VyVHlwZSI6eyJTIjoibmlrZTpwbHVzIn0sInN0YXR1cyI6eyJTIjoiV0lOTkVSIn0sInJldGFpbFBpY2t1cFBlcnNvbiI6eyJTIjoibnVsbCJ9LCJ0dGwiOnsiTiI6IjE3MjU4NDM3MjUifSwibGF1bmNoSWQiOnsiUyI6IjI0Yjc1MTgzLWNlZDgtM2VjOC05NzhhLTRkZDNkNzM1ZTg5MiJ9LCJza3VJZCI6eyJTIjoiOGI5MTgxMWEtOTVlYy01MDk5LWFkNWYtYzI1ZjFhNGNhNjAxIn0sImNoYW5uZWwiOnsiUyI6IlNOS1JTIn0sImdlb2xvY2F0aW9uIjp7IlMiOiJudWxsIn0sInNoaXBwaW5nIjp7IlMiOiJ7XCJyZWNpcGllbnRcIjp7XCJmaXJzdE5hbWVcIjpcIuaWh+adsFwiLFwibGFzdE5hbWVcIjpcIuebm1wiLFwicGhvbmVOdW1iZXJcIjpcIjE4MTEyODg1NjE2XCJ9LFwiYWRkcmVzc1wiOntcImFkZHJlc3MxXCI6XCLojbfoirHmsaDooZfpgZPojbfoirHmsaDlhazlr5MxOS025Y+3XCIsXCJjaXR5XCI6XCLluLjlt57luIJcIixcInN0YXRlXCI6XCJDTi0zMlwiLFwicG9zdGFsQ29kZVwiOlwiMjEzMDAwXCIsXCJjb3VudHJ5XCI6XCJDTlwiLFwiY291bnR5XCI6XCLpkp/mpbzljLpcIn0sXCJtZXRob2RcIjpudWxsLFwiZ2V0QnlcIjp7XCJtYXhEYXRlXCI6e1wiZGF0ZVRpbWVcIjpcIjIwMjQtMDktMDlUMDI6MjU6MDEuNTgyWlwiLFwidGltZXpvbmVcIjpcIkFzaWEvU2hhbmdoYWlcIixcInByZWNpc2lvblwiOlwiREFZXCJ9fX0ifSwicGF5bWVudFRva2VuIjp7IlMiOiIzNzA4NmMwNy1kODY4LTRhMGYtYTgzZS03NjllOWU2MjcwZmYifSwicG9zdHBheVJldHJ5Ijp7IkJPT0wiOmZhbHNlfSwicGF5bWVudFN0YXR1cyI6eyJTIjoiUEVORElOR19QQVlNRU5UIn0sInNlbGVjdGVkVGltZXN0YW1wIjp7Ik4iOiIxNzI1MjM4OTI1NTc4In0sInVwbUlkIjp7IlMiOiIwM2MzNDAzZi03ZDU0LTQ4ZjMtOGRkYi1mMjdkMWNlNjExZGQifSwicmVzZXJ2YXRpb25JZCI6eyJTIjoiUDI2Y2JkYTI0ZTk4ZDRiY2RiNzU5MjdhNTU3ZGY5YjNkIn0sImNyZWF0aW9uVGltZXN0YW1wIjp7Ik4iOiIxNzI1MjM4ODE2MTcyIn0sIndhaXRpbmdSZWFzb24iOnsiTlVMTCI6dHJ1ZX0sInRvdGFscyI6eyJTIjoie1wiaXRlbXNcIjp7XCJ0b3RhbFwiOjEwOTkuMCxcImRldGFpbHNcIjp7XCJwcmljZVwiOjEwOTkuMCxcImRpc2NvdW50XCI6MC4wfX0sXCJ0YXhlc1wiOntcImRldGFpbHNcIjp7XCJpdGVtc1wiOntcInR5cGVcIjpcIk5PVF9DQUxDVUxBVEVEXCJ9fX0sXCJmdWxmaWxsbWVudFwiOntcInRvdGFsXCI6MC4wLFwiZGV0YWlsc1wiOntcInByaWNlXCI6MC4wLFwiZGlzY291bnRcIjowLjB9fX0ifSwidmFsaWRhdGlvblN1bW1hcnkiOnsiUyI6IntcInJlc3VsdFwiOlwiVkFMSURcIn0ifSwic29ydCI6eyJOIjoiMTUxMjEyNTIxIn0sImlkIjp7IlMiOiI4M2Y2NjZiMi0yM2FkLTVjNjgtOWNjYy0xMjQ4ZTcwMDVhZWUifSwiY2hlY2tvdXRJZCI6eyJTIjoiZDNlOTg3NDgtOTRmZS00NzZhLTkwOTctMjRiOTA4NGEyMzNkIn0sImxvY2FsZSI6eyJTIjoiemhfQ04ifSwidHJ1ZUNsaWVudElwIjp7IlMiOiIxMTQuMjI3Ljk4LjI1In0sInBvc3RwYXlMaW5rIjp7IlMiOiJodHRwczovL3d3dy5uaWtlLmNvbS9vbWVnYSJ9LCJyZXNlcnZhdGlvblRpbWVzdGFtcCI6eyJOIjoiMTcyNTIzODkyMjA3MCJ9LCJyYW5rIjp7Ik4iOiItMSJ9LCJyZWVudHJ5UGVybWl0dGVkIjp7IkJPT0wiOmZhbHNlfSwiZm9yd2FyZGVkRm9yIjp7IlMiOiIxMTQuMjI3Ljk4LjI1LCAxMC4xMjAuMjUuMjA5LCA1OC4yMjIuNDcuMTcyLCAzOS45Ni4xMzAuMTExIn0sImxhdW5jaFNrdVN0YXR1cyI6eyJTIjoiMjRiNzUxODMtY2VkOC0zZWM4LTk3OGEtNGRkM2Q3MzVlODkyOjhiOTE4MTFhLTk1ZWMtNTA5OS1hZDVmLWMyNWYxYTRjYTYwMTpXSU5ORVIifSwiYXBwSWQiOnsiUyI6ImNvbS5uaWtlLmNvbW1lcmNlLnNua3JzLmlvcyJ9fSwiU2l6ZUJ5dGVzIjoxNzQ5fSwiZXZlbnRTb3VyY2UiOiJhd3M6ZHluYW1vZGIifQo=" \
    --profile CommerceGCTest \
    --region cn-northwest-1
```


## Update
```
{"awsRegion":"cn-northwest-1","eventID":"fd5772af-6b44-408a-a66b-e05b64c816a4","eventName":"MODIFY","userIdentity":null,"recordFormat":"application/json","tableName":"launch.winnerselector.entry","dynamodb":{"ApproximateCreationDateTime":1725932134565,"Keys":{"id":{"S":"83f666b2-23ad-5c68-9ccc-1248e7005aff"}},"NewImage":{"userAgent":{"S":"SNKRS/6.6.0 (prod; 2407181638; iOS 16.6.1; iPhone13,4)"},"traceContext":{"S":"v1:9655238fd3131624:702c742b47e20b6a:1"},"currency":{"S":"CNY"},"launchSkuStatusValidation":{"S":"24b75183-ced8-3ec8-978a-4dd3d735e892:8b91811a-95ec-5099-ad5f-c25f1a4ca601:WINNER:VALID"},"reservationJobId":{"S":"ed9a9e59-f6b9-4b9c-93ee-de211e628c66"},"userType":{"S":"nike:plus"},"status":{"S":"WINNER"},"retailPickupPerson":{"S":"null"},"skuId":{"S":"8b91811a-95ec-5099-ad5f-c25f1a4ca601"},"launchId":{"S":"24b75183-ced8-3ec8-978a-4dd3d735e892"},"channel":{"S":"SNKRS"},"geolocation":{"S":"null"},"shipping":{"S":"{\"recipient\":{\"firstName\":\"文杰\",\"lastName\":\"盛\",\"phoneNumber\":\"18112885616\"},\"address\":{\"address1\":\"荷花池街道荷花池公寓19-6号\",\"city\":\"常州市\",\"state\":\"CN-32\",\"postalCode\":\"213000\",\"country\":\"CN\",\"county\":\"钟楼区\"},\"method\":null,\"getBy\":{\"maxDate\":{\"dateTime\":\"2024-09-09T02:25:01.582Z\",\"timezone\":\"Asia/Shanghai\",\"precision\":\"DAY\"}}}"},"paymentToken":{"S":"37086c07-d868-4a0f-a83e-769e9e6270ff"},"postpayRetry":{"BOOL":false},"paymentStatus":{"S":"PENDING_PAYMENT"},"selectedTimestamp":{"N":"1725238925578"},"upmId":{"S":"03c3403f-7d54-48f3-8ddb-f27d1ce611dd"},"reservationId":{"S":"P26cbda24e98d4bcdb75927a557df9b3d"},"creationTimestamp":{"N":"1725238816172"},"waitingReason":{"NULL":true},"totals":{"S":"{\"items\":{\"total\":1099.0,\"details\":{\"price\":1099.0,\"discount\":0.0}},\"taxes\":{\"details\":{\"items\":{\"type\":\"NOT_CALCULATED\"}}},\"fulfillment\":{\"total\":0.0,\"details\":{\"price\":0.0,\"discount\":0.0}}}"},"validationSummary":{"S":"{\"result\":\"VALID\"}"},"sort":{"N":"151212521"},"id":{"S":"83f666b2-23ad-5c68-9ccc-1248e7005aff"},"checkoutId":{"S":"d3e98748-94fe-476a-9097-24b9084a233d"},"locale":{"S":"zh_CN"},"trueClientIp":{"S":"114.227.98.25"},"postpayLink":{"S":"https://www.nike.com/omega"},"reservationTimestamp":{"N":"1725238922070"},"rank":{"N":"-1"},"reentryPermitted":{"BOOL":false},"forwardedFor":{"S":"114.227.98.25, 10.120.25.209, 58.222.47.172, 39.96.130.111"},"launchSkuStatus":{"S":"24b75183-ced8-3ec8-978a-4dd3d735e892:8b91811a-95ec-5099-ad5f-c25f1a4ca601:WINNER"},"appId":{"S":"com.nike.commerce.snkrs.ios"}},"OldImage":{"userAgent":{"S":"SNKRS/6.6.0 (prod; 2407181638; iOS 16.6.1; iPhone13,4)"},"traceContext":{"S":"v1:9655238fd3131624:702c742b47e20b6a:1"},"currency":{"S":"CNY"},"launchSkuStatusValidation":{"S":"24b75183-ced8-3ec8-978a-4dd3d735e892:8b91811a-95ec-5099-ad5f-c25f1a4ca601:WINNER:VALID"},"reservationJobId":{"S":"ed9a9e59-f6b9-4b9c-93ee-de211e628c66"},"userType":{"S":"nike:plus"},"status":{"S":"WINNER"},"retailPickupPerson":{"S":"null"},"skuId":{"S":"8b91811a-95ec-5099-ad5f-c25f1a4ca601"},"launchId":{"S":"24b75183-ced8-3ec8-978a-4dd3d735e892"},"channel":{"S":"SNKRS"},"geolocation":{"S":"null"},"shipping":{"S":"{\"recipient\":{\"firstName\":\"文杰22\",\"lastName\":\"盛\",\"phoneNumber\":\"18112885616\"},\"address\":{\"address1\":\"荷花池街道荷花池公寓19-6号\",\"city\":\"常州市\",\"state\":\"CN-32\",\"postalCode\":\"213000\",\"country\":\"CN\",\"county\":\"钟楼区\"},\"method\":null,\"getBy\":{\"maxDate\":{\"dateTime\":\"2024-09-09T02:25:01.582Z\",\"timezone\":\"Asia/Shanghai\",\"precision\":\"DAY\"}}}"},"paymentToken":{"S":"37086c07-d868-4a0f-a83e-769e9e6270ff"},"postpayRetry":{"BOOL":false},"paymentStatus":{"S":"PENDING_PAYMENT"},"selectedTimestamp":{"N":"1725238925578"},"upmId":{"S":"03c3403f-7d54-48f3-8ddb-f27d1ce611dd"},"reservationId":{"S":"P26cbda24e98d4bcdb75927a557df9b3d"},"creationTimestamp":{"N":"1725238816172"},"waitingReason":{"NULL":true},"totals":{"S":"{\"items\":{\"total\":1099.0,\"details\":{\"price\":1099.0,\"discount\":0.0}},\"taxes\":{\"details\":{\"items\":{\"type\":\"NOT_CALCULATED\"}}},\"fulfillment\":{\"total\":0.0,\"details\":{\"price\":0.0,\"discount\":0.0}}}"},"validationSummary":{"S":"{\"result\":\"VALID\"}"},"sort":{"N":"151212521"},"id":{"S":"83f666b2-23ad-5c68-9ccc-1248e7005aff"},"checkoutId":{"S":"d3e98748-94fe-476a-9097-24b9084a233d"},"locale":{"S":"zh_CN"},"trueClientIp":{"S":"114.227.98.25"},"postpayLink":{"S":"https://www.nike.com/omega"},"reservationTimestamp":{"N":"1725238922070"},"rank":{"N":"-1"},"reentryPermitted":{"BOOL":false},"forwardedFor":{"S":"114.227.98.25, 10.120.25.209, 58.222.47.172, 39.96.130.111"},"launchSkuStatus":{"S":"24b75183-ced8-3ec8-978a-4dd3d735e892:8b91811a-95ec-5099-ad5f-c25f1a4ca601:WINNER"},"appId":{"S":"com.nike.commerce.snkrs.ios"}},"SizeBytes":3444},"eventSource":"aws:dynamodb"}
```

## Delete
```
{"awsRegion":"cn-northwest-1","eventID":"005d9251-8fa3-4ba0-a9d1-d6a074d7f990","eventName":"REMOVE","userIdentity":null,"recordFormat":"application/json","tableName":"launch.winnerselector.entry","dynamodb":{"ApproximateCreationDateTime":1725932144754,"Keys":{"id":{"S":"83f666b2-23ad-5c68-9ccc-1248e7005aff"}},"OldImage":{"userAgent":{"S":"SNKRS/6.6.0 (prod; 2407181638; iOS 16.6.1; iPhone13,4)"},"traceContext":{"S":"v1:9655238fd3131624:702c742b47e20b6a:1"},"currency":{"S":"CNY"},"launchSkuStatusValidation":{"S":"24b75183-ced8-3ec8-978a-4dd3d735e892:8b91811a-95ec-5099-ad5f-c25f1a4ca601:WINNER:VALID"},"reservationJobId":{"S":"ed9a9e59-f6b9-4b9c-93ee-de211e628c66"},"userType":{"S":"nike:plus"},"status":{"S":"WINNER"},"retailPickupPerson":{"S":"null"},"launchId":{"S":"24b75183-ced8-3ec8-978a-4dd3d735e892"},"skuId":{"S":"8b91811a-95ec-5099-ad5f-c25f1a4ca601"},"channel":{"S":"SNKRS"},"geolocation":{"S":"null"},"shipping":{"S":"{\"recipient\":{\"firstName\":\"文杰\",\"lastName\":\"盛\",\"phoneNumber\":\"18112885616\"},\"address\":{\"address1\":\"荷花池街道荷花池公寓19-6号\",\"city\":\"常州市\",\"state\":\"CN-32\",\"postalCode\":\"213000\",\"country\":\"CN\",\"county\":\"钟楼区\"},\"method\":null,\"getBy\":{\"maxDate\":{\"dateTime\":\"2024-09-09T02:25:01.582Z\",\"timezone\":\"Asia/Shanghai\",\"precision\":\"DAY\"}}}"},"paymentToken":{"S":"37086c07-d868-4a0f-a83e-769e9e6270ff"},"postpayRetry":{"BOOL":false},"paymentStatus":{"S":"PENDING_PAYMENT"},"selectedTimestamp":{"N":"1725238925578"},"upmId":{"S":"03c3403f-7d54-48f3-8ddb-f27d1ce611dd"},"reservationId":{"S":"P26cbda24e98d4bcdb75927a557df9b3d"},"creationTimestamp":{"N":"1725238816172"},"waitingReason":{"NULL":true},"totals":{"S":"{\"items\":{\"total\":1099.0,\"details\":{\"price\":1099.0,\"discount\":0.0}},\"taxes\":{\"details\":{\"items\":{\"type\":\"NOT_CALCULATED\"}}},\"fulfillment\":{\"total\":0.0,\"details\":{\"price\":0.0,\"discount\":0.0}}}"},"validationSummary":{"S":"{\"result\":\"VALID\"}"},"sort":{"N":"151212521"},"id":{"S":"83f666b2-23ad-5c68-9ccc-1248e7005aff"},"checkoutId":{"S":"d3e98748-94fe-476a-9097-24b9084a233d"},"locale":{"S":"zh_CN"},"trueClientIp":{"S":"114.227.98.25"},"postpayLink":{"S":"https://www.nike.com/omega"},"reservationTimestamp":{"N":"1725238922070"},"rank":{"N":"-1"},"reentryPermitted":{"BOOL":false},"forwardedFor":{"S":"114.227.98.25, 10.120.25.209, 58.222.47.172, 39.96.130.111"},"launchSkuStatus":{"S":"24b75183-ced8-3ec8-978a-4dd3d735e892:8b91811a-95ec-5099-ad5f-c25f1a4ca601:WINNER"},"appId":{"S":"com.nike.commerce.snkrs.ios"}},"SizeBytes":1740},"eventSource":"aws:dynamodb"}
```