##############################################################
#
# alb_stack.py
#
#
##############################################################

from aws_cdk import (
  aws_ec2 as ec2,
  aws_iam as iam,
  aws_elasticloadbalancingv2 as elb,
  aws_autoscaling as autoscaling,
  core
)

with open("./user_data/user_data.sh") as f:
  user_data=f.read()

class ALBStack(core.Stack):

  def __init__(self, scope: core.Construct, construct_id: str, alb_sg: ec2.ISecurityGroup, alb_ec2_role: iam.IRole, **kwargs) -> None:
    super().__init__(scope, construct_id, **kwargs)

    itype=ec2.InstanceType("t3.nano")
    iami=ec2.MachineImage.from_ssm_parameter("/linux/production/ami_id",os=ec2.OperatingSystemType.LINUX)
    default_vpc=ec2.Vpc.from_lookup(self, "DefaultVpc", is_default=True)
    key_name="alb-key"

    # Create ALB
    self.alb=elb.ApplicationLoadBalancer(self,"myALB",
      vpc=default_vpc,
      security_group=alb_sg,
      internet_facing=True
    )

    # Create Target Group
    target_group=elb.ApplicationTargetGroup(self,"myTG",
      port=80,
      vpc=default_vpc,
      target_type=elb.TargetType.INSTANCE,
      stickiness_cookie_duration=core.Duration.days(1)
    )

    # Create listener
    listener=self.alb.add_listener("my80",
      port=80,
      open=True,
      default_target_groups=[target_group]
    )

    # Set Update Policy
    asg_update_policy = autoscaling.UpdatePolicy.rolling_update(
      min_instances_in_service=1,
      pause_time=core.Duration.minutes(2)
    )

    # Create ASG
    self.asg = autoscaling.AutoScalingGroup(self, "myASG",
      instance_type=itype,
      machine_image=iami,
      vpc=default_vpc,
      role=alb_ec2_role,
      security_group=alb_sg,
      cooldown=core.Duration.seconds(300),
      key_name=key_name,
      desired_capacity=2,
      min_capacity=1,
      max_capacity=3,
      update_policy=asg_update_policy,
      user_data=ec2.UserData.custom(user_data)
    )

    # Attach target group to autoscaling group
    self.asg.attach_to_application_target_group(target_group)

    # Auto-Scale based on CPU
    self.asg.scale_on_cpu_utilization(
      "CpuScaling",
      target_utilization_percent=50,
      #scale_in_cooldown=core.Duration.seconds(60),
      cooldown=core.Duration.seconds(60),
    )

    core.Tags.of(self.asg).add("ami_id_parameter", "/linux/production/ami_id")

    core.CfnOutput(self,"Output",value=self.alb.load_balancer_dns_name)

  #Exports
  @property
  def alb_arn(self) -> str:
    return self.alb.load_balancer_arn
    
