##############################################################
#
# iam_stack.py
#
#
##############################################################

from aws_cdk import (
  aws_iam as iam,
  core
)

class IAMStack(core.Stack):

  def __init__(self, scope: core.Construct, construct_id: str, **kwargs) -> None:
    super().__init__(scope, construct_id, **kwargs)

    self._alb_ec2_role=iam.Role(self,"ALB EC2 Role",
      role_name="ALBEC2Role",
      assumed_by=iam.ServicePrincipal("ec2.amazonaws.com"),
      managed_policies=[
        iam.ManagedPolicy.from_aws_managed_policy_name('AmazonSSMManagedInstanceCore')
      ]
    )

  @property
  def alb_ec2_role(self) -> iam.IRole:
    return self._alb_ec2_role
