# Use env=test|prod as input parameter

JOB_NAME=taijitu-etl-launch-entries-${env}
AWS_Regions=cn-northwest-1

ifndef env
$(error env is not set)
endif

do_it=0
ifeq ($(env),test)
do_it=1
endif
ifeq ($(env),prod)
do_it=1
endif
ifeq ($(do_it),0)
$(error env can only be either test or prod)
endif

ifeq ($(env),test)
JOB_ROLE=arn:aws-cn:iam::734176943427:role/bots-taijitu-glue-etl-role
TempDir=s3://aws-glue-assets-734176943427-cn-northwest-1/temporary/
OutputDir=s3://bots-taijitu-test-439314357471-flatted-data
ScriptDir=s3://aws-glue-assets-734176943427-cn-northwest-1/scripts/
AthenaTableDir=s3://bots-taijitu-test-439314357471-athena-table-data
AWS_PROFILE=CommerceGCTest
endif
ifeq ($(env),prod)
JOB_ROLE=arn:aws-cn:iam::734147128161:role/bots-taijitu-glue-etl-role
TempDir=s3://aws-glue-assets-734147128161-cn-northwest-1/temporary/
OutputDir=s3://bots-taijitu-prod-439413396736-flatted-data
ScriptDir=s3://aws-glue-assets-734147128161-cn-northwest-1/scripts/
AthenaTableDir=s3://bots-taijitu-prod-439413396736-athena-table-data
AWS_PROFILE=CommerceGCProd
endif


# @echo "JOB_ROLE: "$(JOB_ROLE)
# @echo "TempDir: "${TempDir}
# @echo "OutputDir: "${OutputDir}
# @echo "ScriptDir: "${ScriptDir}

.FORCE:
print: .FORCE
	echo ${JOB_NAME}
convert-to-python: .FORCE
	jupyter nbconvert --to python kinesis_handler.ipynb
generate-aws-credentials: .FORCE
	echo "Generating aws credentials for profile ${AWS_PROFILE}..."
	gimme-aws-creds --profile ${AWS_PROFILE}

sync-athena-launch-entries-bucket: .FORCE
	echo "Syncing Athena launch entries bucket..."
	aws s3 sync "${OutputDir}/launch-entries/" \
		"${AthenaTableDir}/launch-entries/" \
		--exclude "*_spark_metadata/*" \
		--exclude "*_spark_metadata*" \
		--exclude "*year=__HIVE_DEFAULT_PARTITION__/*" \
		--profile default

create-job: .FORCE
	echo "Building notebook script..."
	jupyter nbconvert --to python kinesis_handler.ipynb
	echo "Uploading script..."
	aws s3 cp --profile ${AWS_PROFILE} --region ${AWS_Regions} kinesis_handler.py ${ScriptDir}
	echo "Creating glue job..."
	aws glue create-job --name ${JOB_NAME} --profile ${AWS_PROFILE} \
		--role ${JOB_ROLE} \
		--command '{"Name" :  "gluestreaming", "ScriptLocation" : "${ScriptDir}kinesis_handler.py", "PythonVersion": "3"}' \
		--tags '{"nike-tagguid": "648007d7-d23e-4bcc-8a5f-a40119600eda"}' \
		--glue-version 4.0 \
		--number-of-workers 2 \
		--worker-type G.1X \
		--default-arguments '{"--enable-glue-datacatalog" : "true", "--enable-metrics": "true", "--TempDir": "'${TempDir}'", "--OutputDir": "'${OutputDir}'"}' \
		--region ${AWS_Regions}

update-job: .FORCE
	echo "Building notebook script..."
	jupyter nbconvert --to python kinesis_handler.ipynb
	echo "Uploading script..."
	aws s3 cp --profile ${AWS_PROFILE} --region ${AWS_Regions} kinesis_handler.py ${ScriptDir}
	echo "Updating glue job..."
	aws glue update-job --job-name ${JOB_NAME} --profile ${AWS_PROFILE} \
		--job-update '{"Role": "'${JOB_ROLE}'", \
		"Command" : {"Name" :  "gluestreaming", "ScriptLocation" : "${ScriptDir}kinesis_handler.py", "PythonVersion": "3"}, \
		"DefaultArguments": {"--enable-glue-datacatalog" : "true", "--enable-metrics": "true", "--TempDir": "'${TempDir}'", "--OutputDir": "'${OutputDir}'"}, \
		"GlueVersion": "4.0", "WorkerType": "G.1X", "NumberOfWorkers": 2}' --region ${AWS_Regions}