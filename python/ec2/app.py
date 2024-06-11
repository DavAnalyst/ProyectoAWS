import os.path

from aws_cdk.aws_s3_assets import Asset

from aws_cdk import (
    aws_ec2 as ec2,
    aws_iam as iam,
    App, Stack
)

from constructs import Construct

dirname = os.path.dirname(__file__)


class EC2InstanceStack(Stack):

    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # VPC
        vpc = ec2.Vpc(self, "VPC",
            nat_gateways=0,
            subnet_configuration=[ec2.SubnetConfiguration(name="public",subnet_type=ec2.SubnetType.PUBLIC)]
            )

        # AMI
        amzn_linux = ec2.MachineImage.latest_amazon_linux(
            generation=ec2.AmazonLinuxGeneration.AMAZON_LINUX_2,
            edition=ec2.AmazonLinuxEdition.STANDARD,
            virtualization=ec2.AmazonLinuxVirt.HVM,
            storage=ec2.AmazonLinuxStorage.GENERAL_PURPOSE
            )
        
        ubuntu_linux = ec2.MachineImage.generic_linux(
            ami_map={
                "us.east-1":"ami-04b70fa74e45c3917"
            }
        )


        # Instance
        instance = ec2.Instance(self, "Instance",
            instance_type=ec2.InstanceType("t2.micro"),
            machine_image=ubuntu_linux,
            vpc = vpc
        
            )


app = App()
EC2InstanceStack(app, "ec2-instance")

app.synth()