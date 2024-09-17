JOB_NAME=taijitu-etl-launch-entries-test
JOB_ROLE_TEST=arn:aws-cn:iam::734176943427:role/bots-taijitu-glue-etl-role
TempDirTest=s3://aws-glue-assets-734176943427-cn-northwest-1/temporary/
OutputDir=s3://bots-taijitu-test-439314357471-flatted-data
ScriptDir=s3://aws-glue-assets-734176943427-cn-northwest-1/scripts/
AWS_Regions=cn-northwest-1

.FORCE:

convert-to-python: .FORCE
	jupyter nbconvert --to python kinesis_handler.ipynb
generate-aws-credentials-test: .FORCE
	echo "Generating aws credentials..."
	gimme-aws-creds --profile CommerceGCTest
generate-aws-credentials-prod: .FORCE
	echo "Generating aws credentials..."
	gimme-aws-creds --profile CommerceGCProd

create-job-test: .FORCE
	echo "Building notebook script..."
	jupyter nbconvert --to python kinesis_handler.ipynb
	echo "Uploading script..."
	aws s3 cp --profile CommerceGCTest --region ${AWS_Regions} kinesis_handler.py ${ScriptDir}
	echo "Creating glue job..."
	aws glue create-job --name ${JOB_NAME} --profile CommerceGCTest \
		--role ${JOB_ROLE_TEST} \
		--command '{"Name" :  "gluestreaming", "ScriptLocation" : "${ScriptDir}kinesis_handler.py", "PythonVersion": "3"}' \
		--tags '{"nike-tagguid": "648007d7-d23e-4bcc-8a5f-a40119600eda"}' \
		--glue-version 4.0 \
		--number-of-workers 2 \
		--worker-type G.1X \
		--default-arguments '{"--enable-glue-datacatalog" : "true", "--TempDir": "'${TempDirTest}'", "--OutputDir": "'${OutputDir}'"}' \
		--region ${AWS_Regions}

update-job-test: .FORCE
	echo "Building notebook script..."
	jupyter nbconvert --to python kinesis_handler.ipynb
	echo "Uploading script..."
	aws s3 cp --profile CommerceGCTest --region ${AWS_Regions} kinesis_handler.py ${ScriptDir}
	echo "Updating glue job..."
	aws glue update-job --job-name ${JOB_NAME} --profile CommerceGCTest \
		--job-update '{"Role": "'${JOB_ROLE_TEST}'", \
		"Command" : {"Name" :  "gluestreaming", "ScriptLocation" : "${ScriptDir}kinesis_handler.py", "PythonVersion": "3"}, \
		"DefaultArguments": {"--enable-glue-datacatalog" : "true", "--TempDir": "'${TempDirTest}'", "--OutputDir": "'${OutputDir}'"}, \
		"GlueVersion": "4.0", "WorkerType": "G.1X", "NumberOfWorkers": 2}' --region ${AWS_Regions}
