#!/usr/bin/env python3
"""Hands-off deployment of the Jenkins host CloudFormation stack."""
import json, os, pathlib, sys, boto3
from botocore.exceptions import ClientError

STACK_NAME   = os.getenv("STACK",    "jenkins-ci")
TEMPLATE_PATH= os.getenv("TEMPLATE", "activity7.yaml")
REGION       = os.getenv("AWS_REGION") or os.getenv("AWS_DEFAULT_REGION") or "us-east-1"

session = boto3.Session(region_name=REGION)
ec2 = session.client("ec2")
cf  = session.client("cloudformation")

def default_vpc() -> str:
    v = ec2.describe_vpcs(Filters=[{"Name":"is-default","Values":["true"]}])["Vpcs"]
    if not v: sys.exit(f"No default VPC in {REGION}")
    return v[0]["VpcId"]

def public_subnet(vpc_id: str) -> str:
    for f in (["default-for-az","true"], ["map-public-ip-on-launch","true"]):
        s = ec2.describe_subnets(Filters=[{"Name":"vpc-id","Values":[vpc_id]},
                                          {"Name":f[0],"Values":[f[1]]}])["Subnets"]
        if s: return sorted(s, key=lambda x: (x["AvailabilityZone"], x["SubnetId"]))[0]["SubnetId"]
    sys.exit(f"No public subnet in {vpc_id}")

def stack(template: str, params: list[dict]) -> None:
    try:
        cf.create_stack(StackName=STACK_NAME,
                        TemplateBody=template,
                        Parameters=params,
                        Capabilities=["CAPABILITY_NAMED_IAM"])
        waiter = cf.get_waiter("stack_create_complete")
    except ClientError as e:
        if "AlreadyExistsException" not in str(e): raise
        try:
            cf.update_stack(StackName=STACK_NAME,
                            TemplateBody=template,
                            Parameters=params,
                            Capabilities=["CAPABILITY_NAMED_IAM"])
            waiter = cf.get_waiter("stack_update_complete")
        except ClientError as u:
            if "No updates are to be performed" in str(u): return
            raise
    waiter.wait(StackName=STACK_NAME)

def outputs() -> None:
    out = cf.describe_stacks(StackName=STACK_NAME)["Stacks"][0]["Outputs"]
    print(json.dumps({o["OutputKey"]: o["OutputValue"] for o in out}, indent=2))

def main() -> None:
    vpc_id    = default_vpc()
    subnet_id = public_subnet(vpc_id)
    template  = pathlib.Path(TEMPLATE_PATH).read_text()
    params = [
        {"ParameterKey":"VpcId",         "ParameterValue":vpc_id},
        {"ParameterKey":"PublicSubnetId","ParameterValue":subnet_id},
    ]
    stack(template, params)
    outputs()

if __name__ == "__main__":
    main()
