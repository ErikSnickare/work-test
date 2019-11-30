#!/bin/bash
AWS_PROFILE?=aws-private
REGION?=eu-west-1
VERSION?=46


create-infrastructure:
	aws cloudformation create-stack \
		--stack-name work-test	\
		--template-body file://infrastructure/cfn-template.yaml \
		--profile=${AWS_PROFILE} \
		--region=${REGION}

update-infrastructure:
	aws cloudformation update-stack \
		--stack-name work-test	\
		--template-body file://infrastructure/cfn-template.yaml \
		--profile=${AWS_PROFILE} \
		--region=${REGION}

create-lambda:
	aws cloudformation create-stack \
		--stack-name work-test-functions	\
		--template-body file://infrastructure/cfn-lambdas.yaml \
		--profile=${AWS_PROFILE} \
		--capabilities CAPABILITY_IAM \
		--region=${REGION}

random:
	awk 'BEGIN{srand();printf("%d", 65536*rand())}'

update-lambda: upload-lambda-package
	aws cloudformation update-stack \
		--stack-name work-test-functions	\
		--template-body file://infrastructure/cfn-lambdas.yaml \
		--parameters ParameterKey=Version,ParameterValue=${VERSION} \
		--profile=${AWS_PROFILE} \
		--capabilities CAPABILITY_IAM \
		--region=${REGION}

package-lambda:
	cd handlers/packages && zip -r9 ../handler_package_${VERSION}.zip .
	cd handlers/common && zip -rg ../handler_package_${VERSION}.zip .
	cd handlers && zip -g handler_package_${VERSION}.zip db_insert.py

upload-lambda-package: package-lambda
	aws s3 cp handlers/handler_package_${VERSION}.zip s3://work-test-lambda-functions --profile=aws-private

upgrade-packages:
	cd handlers && sudo pip install -r requirements.txt --target ./packages/
	cd handlers/packages && rm packages.zip && zip -r9 packages.zip .
