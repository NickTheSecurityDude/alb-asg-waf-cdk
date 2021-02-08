##############################################################
#
# wafv2_stack.py
#
#
##############################################################

from aws_cdk import (
  aws_wafv2 as waf,
  core
)

class WAFV2Stack(core.Stack):

  def __init__(self, scope: core.Construct, construct_id: str, alb_arn: str, **kwargs) -> None:
    super().__init__(scope, construct_id, **kwargs)


    web_acl=waf.CfnWebACL(self, "WAF ACL",
      default_action={ "allow": {} },
      scope="REGIONAL",
      visibility_config={
        "sampledRequestsEnabled": True,
        "cloudWatchMetricsEnabled": True,
        "metricName": "web-acl",
      },
      rules=[
        {
          "name": "rate_limit_500",
          "priority": 0,
          "action": {
            "block": {}
          },
          "visibilityConfig": {
            "sampledRequestsEnabled": True,
            "cloudWatchMetricsEnabled": True,
            "metricName": "rate_limit_500"
          },
          "statement": {
            "rateBasedStatement": {
              "limit": 500,
              "aggregateKeyType": "IP"
            }
          }
        },
        {
          "priority": 1,
          "overrideAction": { "none": {} },
          "visibilityConfig": {
            "sampledRequestsEnabled": True,
            "cloudWatchMetricsEnabled": True,
            "metricName": "AWS-AWSManagedRulesAmazonIpReputationList",
          },
          "name": "AWS-AWSManagedRulesAmazonIpReputationList",
          "statement": {
            "managedRuleGroupStatement": {
              "vendorName": "AWS",
              "name": "AWSManagedRulesAmazonIpReputationList",
            },
          },
        },
        {
          "priority": 2,
          "overrideAction": { "none": {} },
          "visibilityConfig": {
            "sampledRequestsEnabled": True,
            "cloudWatchMetricsEnabled": True,
            "metricName": "AWS-AWSManagedRulesCommonRuleSet",
          },
          "name": "AWS-AWSManagedRulesCommonRuleSet",
          "statement": {
            "managedRuleGroupStatement": {
              "vendorName": "AWS",
              "name": "AWSManagedRulesCommonRuleSet",
            },
          },
        },
        {
          "priority": 3,
          "overrideAction": { "none": {} },
          "visibilityConfig": {
            "sampledRequestsEnabled": True,
            "cloudWatchMetricsEnabled": True,
            "metricName": "AWS-AWSManagedRulesKnownBadInputsRuleSet",
          },
          "name": "AWS-AWSManagedRulesKnownBadInputsRuleSet",
          "statement": {
            "managedRuleGroupStatement": {
              "vendorName": "AWS",
              "name": "AWSManagedRulesKnownBadInputsRuleSet",
            },
          },
        },
        {
          "priority": 4,
          "overrideAction": { "none": {} },
          "visibilityConfig": {
            "sampledRequestsEnabled": True,
            "cloudWatchMetricsEnabled": True,
            "metricName": "AWS-AWSManagedRulesSQLiRuleSet",
          },
          "name": "AWS-AWSManagedRulesSQLiRuleSet",
          "statement": {
            "managedRuleGroupStatement": {
              "vendorName": "AWS",
              "name": "AWSManagedRulesSQLiRuleSet",
            },
          },
        }
      ]
    )
   
    waf.CfnWebACLAssociation(self, "WAF Assoc",
      resource_arn=alb_arn,
      web_acl_arn=web_acl.attr_arn
    )


