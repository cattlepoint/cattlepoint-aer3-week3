# cattlepoint-aer3-week3
Capstone Project for AWS ER - Week 3
#### Finalized June 12th 2025

## Overview
* These instructions are intended for participants of the AWS Engagement Ready Class started in April 2025
* The goal of this week3 project is to verify minimal Jenkins competency and to ensure that the environment is working properly
* This project assumes that you have access to the eruser315 credentials
* This project also assumes that you are running the latest MacOS and have terminal access sufficient to install local applications

## Prerequisite
### This section is to ensure you have access to the AWS account and the necessary credentials
* Review the public repo cattlepoint/cattlepoint-aer3-week3
* Login to [AWS Account eruser315account](https://eruser315account.signin.aws.amazon.com/console) using username eruser315 and password ***
* [Download AWS Access Keys](https://us-east-1.console.aws.amazon.com/iam/home?region=us-east-1#/security_credentials/access-key-wizard) file eruser315_accessKeys.csv by selecting Command Line Interface (CLI) and I understand the above recommendation and want to proceed to create an access key -> Next

### This section installs the AWS CLI and configures it with the credentials from the CSV file
* If you haven't already done so, setup Homebrew on your MacOS following [these instructions](https://brew.sh/).
```sh
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```
* Perform these steps in the MacOS terminal to install the AWS CLI
```sh
brew update && brew install awscli
```
* Next we need to configure the AWS CLI with the credentials from the CSV file. You can do this by running the following command in your terminal:
```sh
aws configure --profile eruser315
```
* When prompted, enter the access key and secret access key from the CSV file.  Set the default region to us-east-1 and the output format to json.  The command will look like this:
```sh
% aws configure --profile eruser315
AWS Access Key ID [****************GFJ2]:
AWS Secret Access Key [****************Ya3D]:
Default region name [us-east-1]:
Default output format [json]:
```
* Verify AWS credentials are working:
```sh
export AWS_PROFILE=eruser315
aws sts get-caller-identity
```
* Visually verify in output: arn:aws:iam::***:user/eruser315

### This section installs the latest version of the Kubernetes Command Line Tool, Amazon Elastic Kubernetes Service (Amazon EKS) Command Line Tool (eksctl), Podman (Docker, project dependencies and verifies they are working
* Perform these steps in the MacOS terminal to install podman, git, github client, kubectl, and eksctl:
```sh
brew update && brew install git gh kubectl eksctl podman
```
* Login to your github account following the instructions the below command provides:
```sh
gh login
```
* Verify the the github client is working:
```sh
gh auth status
```
* Expected output (contents will vary):
```sh
✓ Logged in to github.com account
```
* Verify the git tool is working:
```sh
git --version
```
* Verify the the Kubernetes CLI is working:
```sh
kubectl version --client
```
* Verify the the eksctl is working:
```sh
eksctl version
```
* Verify podman is working:
```sh
podman -v
```

### This section is to ensure you have git configured and working properly
* Perform these steps in the MacOS terminal to configure git:
```sh
git config --global user.name "cattlepoint"
git config --global user.email "nobody@nowhere.local"
```
* Verify git is configured:
```sh
gh repo clone cattlepoint/cattlepoint-aer3-week3
```
* Expected output (contents will vary):
```sh
% gh repo clone cattlepoint/cattlepoint-aer3-week3
Cloning into 'cattlepoint-aer3-week3'...
remote: Enumerating objects: 33, done.
remote: Counting objects: 100% (33/33), done.
remote: Compressing objects: 100% (23/23), done.
remote: Total 33 (delta 11), reused 27 (delta 8), pack-reused 0 (from 0)
Receiving objects: 100% (33/33), 9.41 KiB | 3.14 MiB/s, done.
Resolving deltas: 100% (11/11), done.
```
* Change into the project directory:
```sh
cd cattlepoint-aer3-week3
```
* Verify the git repository is working:
```sh
git status && git config --get-regexp '^(remote|branch)\.'
```
* Expected output (contents will vary):
```sh
% git status && git config --get-regexp '^(remote|branch)\.'
On branch main
Your branch is up to date with 'origin/main'.

nothing to commit, working tree clean
remote.origin.url https://github.com/cattlepoint/cattlepoint-aer3-week3.git
remote.origin.fetch +refs/heads/*:refs/remotes/origin/*
branch.main.remote origin
branch.main.merge refs/heads/main
```
#### Clone the remaining repositories (if desired)
* Clone the remaining repositories to your local project directory:
```sh
gh repo clone cattlepoint/cattlepoint-aer3-week3-extras-ecr-pipeline
gh repo clone cattlepoint/cattlepoint-aer3-week3-extras-eks-pipeline
gh repo clone cattlepoint/cattlepoint-aer3-week3-extras-iam-users-pipeline
gh repo clone cattlepoint/cattlepoint-aer3-week3-extras-jenkins-ci
gh repo clone cattlepoint/cattlepoint-aer3-week3-extras-jenkins-create-ecr
gh repo clone cattlepoint/cattlepoint-aer3-week3-extras-jenkins-sample-pipeline
```

## Use Jenkins to build the CI/CD Pipelines to serve the app

### Build Jenkins from template in AWS CloudFormation:
* Verify AWS credentials are working:
```sh
export AWS_PROFILE=eruser315
aws sts get-caller-identity
```
* Visually verify in output: arn:aws:iam::***:user/eruser315

* Clone the Jenkins repository and open the directory:
```sh
gh repo clone cattlepoint/cattlepoint-aer3-week3-extras-jenkins-ci
cd cattlepoint-aer3-week3-extras-jenkins-ci
```

* Deploy the template (this command creates a boto3 python environment, deploys Jenkins and outputs the URL):
```sh
mkvirtualenv boto3
pip install boto3
python3 activity7.py
```

* Expected output (contents will vary):
```sh
% python3 activity7.py
{
  "InstanceId": "i-0b....",
  "JenkinsURL": "http://jenkin-......us-east-1.elb.amazonaws.com"
}
```

### Access Jenkins and configure an admin user
* Open the Jenkins URL in your web browser (e.g., http://jenkin-......us-east-1.elb.amazonaws.com)
* The first time you access Jenkins, it will prompt you to unlock it using an initial admin password.
* To find the initial admin password, run the following command in your terminal to access the Jenkins instance via EC2 Instance Connect:
```sh
INSTANCE_ID=$(aws cloudformation describe-stack-resource \
                --stack-name jenkins-ci \
                --logical-resource-id JenkinsInstance \
                --query 'StackResourceDetail.PhysicalResourceId' \
                --output text)
aws ec2-instance-connect ssh \
  --os-user ubuntu \
  --instance-id $INSTANCE_ID
```
* Once connected, run the following command to retrieve the initial admin password:
```sh
sudo cat /var/lib/jenkins/secrets/initialAdminPassword
```
* Expected output (contents will vary):
```sh
$ sudo cat /var/lib/jenkins/secrets/initialAdminPassword
32b27cc19dc3477a977fa566d89d15fe
```
* Copy the password and paste it into the Jenkins unlock page in your web browser.
* After unlocking Jenkins, it will prompt you to install plugins. Select the "Install suggested plugins" option.
* Wait for the plugins to install. This may take a few minutes.
* Once the plugins are installed, Jenkins will prompt you to create an admin user. Fill in the required information and click "Save and Continue."
* Finally, Jenkins will ask you to configure the instance URL. You can leave it as the default. Click "Save and Finish" to complete the setup.

### Install necessary plugins in Jenkins
* You should now see the Jenkins dashboard.
* Navigate to "Manage Jenkins" -> "Plugins" and install the following plugins:
  - Docker
  - Docker Pipeline
  - AWS Credentials
  - Amazon Web Services SDK :: All
* Once the plugins are installed, check the box "Restart Jenkins when installation is complete and no jobs are running"
* Jenkins will restart automatically. Wait for it to come back online.

### Disable the github throttling
* Navigate to "Manage Jenkins" -> "System"
* Scroll down to the " GitHub API usage" section.
* In the "Github API usage rate limiting strategy?" dropdown, select the "Never check rate limit (NOT RECOMMENDED)" option.
* Click "Save" to apply the changes.

### We need to bootstrap the Jenkins instance with the AWS credentials
* Deploy the cattlepoint-aer3-week3-extras-iam-users-pipeline/cfn-admin-user.yaml template
```sh
export AWS_PROFILE=eruser315
workon boto3
cd cattlepoint-aer3-week3-extras-iam-users-pipeline
python3 cfn-admin-user.py
```
* Expected output (contents will vary):
```sh
% python3 cfn-admin-user.py
Creating stack cfn-admin-user…
Waiting for stack to reach CREATE_COMPLETE …
UserName: cfn-admin-user
AccessKeyId: AK...
SecretAccessKey: Wg...
```
* Copy the AccessKeyId and SecretAccessKey values from the output. You will need them to configure Jenkins credentials.
* From the Jenkins dashboard, navigate to "Manage Jenkins" -> " Credentials"
* Click the dropdown option next to (global) under Stores scoped to Jenkins -> "Add Credentials"
* In the "Kind" dropdown, select "AWS Credentials"
  - ID: aws-jenkins-creds
  - Access Key ID: (paste the AccessKeyId value you copied earlier)
  - Secret Access Key: (paste the SecretAccessKey value you copied earlier)
  - Click Create
* The aws-jenkins-creds credential should now be listed

### Configure the IAM user pipeline
* From the Jenkins dashboard, click on "New Item."
* pipeline name: create-iam-users-pipeline
* pipeline type: Pipeline
* Click "OK" to create the pipeline.
* From the configuration page of the pipeline:
  - Check the box for "Discard old builds"
  - Check the box for "This project is parameterized"
  - Choose Add Parameter dropdown -> set to "Credentials Parameter"
  - Credential type: AWS Credentials
  - Default Value: select the AccessKeyId
  - In the "Pipeline" section, select Definition "Pipeline script from SCM."
  - SCM: Git
  - Repository URL: https://github.com/cattlepoint/cattlepoint-aer3-week3-extras-iam-users-pipeline.git
  - In the "Branches to build" subsection, set "Branch Specifier" to "*/main"
  - Click "Save" to save the pipeline configuration.
* From the pipeline page, click "Build with Parameters" to run the pipeline.
* Accept the default parameters and click "Build."
* Wait for the pipeline to complete. You can monitor the progress in the "Status" section -> "Last Build (#)" -> "Console Output"

### Add the ecr-create credentials to Jenkins
* From the Jenkins dashboard, navigate to "Manage Jenkins" -> " Credentials"
* Click the dropdown option next to (global) under Stores scoped to Jenkins -> "Add Credentials"
* In the "Kind" dropdown, select "AWS Credentials"
  - ID: ecr-create
  - Access Key ID: locate the AccessKeyId value from the output of the create-iam-users-pipeline
  - Secret Access Key: locate the SecretAccessKey value from the output of the create-iam-users-pipeline
  - Click Create
* The ecr-create credential should now be listed

### Configure the ECR creation pipeline
* From the Jenkins dashboard, click on "New Item."
* pipeline name: create-ecr-pipeline
* pipeline type: Pipeline
* Click "OK" to create the pipeline.
* From the configuration page of the pipeline:
  - Check the box for "Discard old builds"
  - Check the box for "This project is parameterized"
  - Choose Add Parameter dropdown -> set to "Credentials Parameter"
  - Credential type: AWS Credentials
  - Default Value: select the AccessKeyId for the ecr-create credential
  - In the "Pipeline" section, select Definition "Pipeline script from SCM."
  - SCM: Git
  - Repository URL: https://github.com/cattlepoint/cattlepoint-aer3-week3-extras-ecr-pipeline.git
  - In the "Branches to build" subsection, set "Branch Specifier" to "*/main"
  - Click "Save" to save the pipeline configuration.
* From the pipeline page, click "Build with Parameters" to run the pipeline.
* Accept the default parameters and click "Build."
* Wait for the pipeline to complete. You can monitor the progress in the "Status" section -> "Last Build (#)" -> "Console Output"

### Add the eks-deploy credentials to Jenkins
* From the Jenkins dashboard, navigate to "Manage Jenkins" -> " Credentials"
* Click the dropdown option next to (global) under Stores scoped to Jenkins -> "Add Credentials"
* In the "Kind" dropdown, select "AWS Credentials"
  - ID: eks-deploy
  - Access Key ID: locate the AccessKeyId value from the output of the create-iam-users-pipeline
  - Secret Access Key: locate the SecretAccessKey value from the output of the create-iam-users-pipeline
  - Click Create
* The eks-deploy credential should now be listed

### Configure the EKS creation pipeline
* From the Jenkins dashboard, click on "New Item."
* pipeline name: create-eks-pipeline
* pipeline type: Pipeline
* Click "OK" to create the pipeline.
* From the configuration page of the pipeline:
  - Check the box for "Discard old builds"
  - Check the box for "This project is parameterized"
  - Choose Add Parameter dropdown -> set to "Credentials Parameter"
  - Credential type: AWS Credentials
  - Default Value: select the AccessKeyId for the eks-deploy credential
  - In the "Pipeline" section, select Definition "Pipeline script from SCM."
  - SCM: Git
  - Repository URL: https://github.com/cattlepoint/cattlepoint-aer3-week3-extras-eks-pipeline.git
  - In the "Branches to build" subsection, set "Branch Specifier" to "*/main"
  - Click "Save" to save the pipeline configuration.
* From the pipeline page, click "Build with Parameters" to run the pipeline.
* Accept the default parameters and click "Build."
* Wait for the pipeline to complete. You can monitor the progress in the "Status" section -> "Last Build (#)" -> "Console Output"
