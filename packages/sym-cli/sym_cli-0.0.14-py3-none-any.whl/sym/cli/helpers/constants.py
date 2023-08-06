import re

SentryDSN = "https://34647c66cad04a51b814cfade7b8d110@o373009.ingest.sentry.io/5342537"
SegmentWriteKey = "4RrqDnVYxMTE8wYJDNWKaPjHCSn9egeY"

AwsOktaNoRoles = re.compile("There are no roles that can be assumed|ARN isn't valid")
Saml2AwsNoRoles = re.compile(
    "no (?:account|role)s available|Supplied RoleArn not found in saml assertion"
)
