#!/usr/bin/env python3

from aws_cdk import core

import boto3
import sys

client = boto3.client('sts')

region=client.meta.region_name

#if region != 'us-east-1':
#  print("This app may only be run from us-east-1")
#  sys.exit()

account_id = client.get_caller_identity()["Account"]

my_env = {'region': region, 'account': account_id}

from stacks.iam_stack import IAMStack
from stacks.sg_stack import SGStack
from stacks.alb_stack import ALBStack
from stacks.wafv2_stack import WAFV2Stack

proj_name="website1-alb"
proj_group_name="ami-auto-replace"

app = core.App()

iam_stack=IAMStack(app, proj_name+"-iam",env=my_env)
sg_stack=SGStack(app, proj_name+"-sg",env=my_env)
alb_stack=ALBStack(app, proj_name+"-alb",
  alb_sg=sg_stack.alb_sg,
  alb_ec2_role=iam_stack.alb_ec2_role,
  env=my_env
)
wafv2_stack=WAFV2Stack(app,proj_name+"-wafv2",
  alb_arn=alb_stack.alb_arn,
  env=my_env
)

for stack in [iam_stack,sg_stack,alb_stack]:
  core.Tags.of(stack).add("Project", proj_name)
  core.Tags.of(stack).add("ProjectGroup", proj_group_name)

app.synth()
