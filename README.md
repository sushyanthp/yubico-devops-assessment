# Yubico Assessment
This assessment uses AWS CloudFormation service to provision resources for deploying a web application to AWS which returns the current date in ISO 8601 format. The web application has been written in Python using Flask, a microweb framework to meet the requriements. It's deployment involves creation of a CloudFormation stack which creates below resources in AWS. For fault tolerance, the EC2 instances hosting the web application are being launched behind an Auto Scaling group with scale-in and scale-out policies.
- Creates an Ubuntu based Linux AWS EC2 instance which hosts the web application
- Creates an EC2 security group with rules for the web application to be accessed by the users on the Internet on port 80
- Creates CloudWatch alarms for monitoring the web application's CPU utilization and use it for scaling purposes

## Package Contents
- WebApp_AWSResources_CloudFormation.json - CloudFormation template to provision AWS resources for web application deployment
- README.md - A read me file with details of the package along with assumptions and instructions for web application deployment
- app directory contents include the source code, dependencies  and a Dockerfile
    - Dockerfile - Dockerfile to build an image of the web application
    - app.py - Source code for the web application using Flask to return the current date in ISO 8601 format
    - requirements.txt - Requirements for the web application to run

## Web Application Deployment Prerequisites
- AWS account to which this web application will be deployed to needs to have a VPC created with atleast one public subnet.
- EC2 instance will be launched without a key pair so SSH is disabled. Also, the security group created for the EC2 instance does not have port 22 open. This is to prevent bad users from connecting to the VM.

## Web Application Deployment Instructions
1. Clone the repo (or copy) the CloudFormation template to your local machine. FYI, this template is designed to work in the EU and US AWS regions. For additional regions, please update the AMIRegionMap mapping in the Mappings section of the template.
2. Login to an AWS account and navigate to the AWS CloudFormation console.
3. Create a CloudFormation stack by passing values for the parameters described below. For detailed instructions on stack creation, please refer this document - https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/cfn-console-create-stack.html
    - VpcId - VpcId where AWS Resources for the Web App are to be provisioned
    - PublicSubnets - Public Subnet(s) where EC2 Instance(s) need to be provisioned. It is recommended to choose two subnets from different AZs for fault tolerance
    - InstanceType - EC2 Instance Type to be used of the EC2. Defaults to t2.micro since we are using AWS Free Tier
    - PercentOfOnDemandInstances - Percentage of On-Demand EC2 instances to launch after the base capacity is reached. During any scaling activity, ensures percent of on-demand instances declared here is maintained.
4. Click Next and then select create for creating the CloudFormation stack.
5. Once stack creation completes, navigate to the EC2 console and search for "Yubico_DevOps_EC2_ASG" in the instances tab. Retrieve it's public IPv4 address from the details tab. We could've displayed the public IP of the instance in the CloudFormation outputs tab if the app (for easier access to it's IP) was launched on a single EC2 instance.
6. In your terminal, run command below to get the date in ISO 8601 format. App is accessible on port 80.
    ```console
    $ curl http://18.224.215.160
    {
        "today": "2020-10-31"
    }
    ```

## Why I chose to deploy the web application this way?
- For building the application, used Flask web framework since it does not have a lot of dependencies and is fairly easy to understand and use.
- The app was then packaged as a Docker image (via a Dockerfile) which makes it portable to any environment which has Docker installed. This container image is based off Alpine Linux. This was chosen to keep the resulting image as small as possible. An FYI, as part of this deployment to an EC2 instance, Docker is first installed on it before launching running the app as a container.
- Following cloud best practices of deploying applications across AZs for increased availability and fault tolerance, I opted for deploying the web application on free tier EC2 instances behind an auto scaling group instead of directly launching the web app on a stand along EC2 instance. In addition, using an auto scaling group provides a number of benefits like replacement of instances which fail instance/system checks and performing scaling operations when apps receive increased load.
- From a pricing perspective, all resources created as part of this stack fall within AWS' free tier. Starting with t2.micro EC2 instances to Cloudwatch alarms (basic monitoring) to the auto scaling group. In addition, support for spot instances has been built-in to the auto scaling group via the mixed instance type feature which allows this application to utilize both on-demand and spot instances. By default, the app is launched on an on-demand instance since the OnDemandBaseCapacity parameter is set to 1 to ensure there is atleast 1 on-demand instance running. Depending on the value passed of the PercentOfOnDemandInstances parameter, subsequent instances can either be spot or on-demand. For example, if PercentOfOnDemandInstances is set to 0, the auto scaling group will launch the web application on spot instances when a scale out occurs.

## Improvements
- Now that we have the application as a Docker image, we can consider deploying it to a container orchestraction service in AWS like ECS or EKS. This will make management of the service easier.
- For increased availability, we can also consider adding a load balancer to the deployment. This will improve app availability by routing requests only to healthy backend instances and also help us use a single endpoint for accessing the web application.

## Instructions for Local Deployment of Web App
# System Requirements
- Python3
- Pip3
- Docker

# Python Dependencies
- Flask - Python WSGI web application framework

## Local Development
A dedicated Python virtual environment is highly recommended for this project to isolate Python dependencies from your system's Python installation and from other Python projects. Instructions to install and setup a Python virutal environment can be found here - https://sourabhbajaj.com/mac-setup/Python/virtualenv.html

For local developement within a virtual environment, use commands listed below:

```console
(venv) $ git clone <repo-url>
(venv) $ cd app/
(venv) $ pip3 install -r requirements.txt
(venv) $ python3 app.py
```