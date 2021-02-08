##############################################################
#
# sg_stack.py
#
#
##############################################################

from aws_cdk import (
  aws_ec2 as ec2,
  core
)

class SGStack(core.Stack):

  def __init__(self, scope: core.Construct, construct_id: str, **kwargs) -> None:
    super().__init__(scope, construct_id, **kwargs)

    alb_sg=ec2.SecurityGroup(self,"ALB SG",
      vpc=ec2.Vpc.from_lookup(self,"DefaultVPC",is_default=True)
    )

    alb_sg.add_ingress_rule(ec2.Peer.any_ipv4(),ec2.Port.tcp(80),"web traffic")
    alb_sg.add_ingress_rule(ec2.Peer.any_ipv4(),ec2.Port.tcp(443),"web traffic")

    self._alb_sg=alb_sg

  @property
  def alb_sg(self) -> ec2.ISecurityGroup:
    return self._alb_sg
