import re
from textwrap import dedent
from typing import Optional

import boto3
import validators
from botocore.config import Config as BotoConfig

from ..errors import InstanceNotFound
from .params import get_ssh_user

InstanceIDPattern = re.compile("^i-[a-f0-9]+$")


def boto_client(saml_client, service):
    creds = saml_client.get_creds()
    return boto3.client(
        service,
        config=BotoConfig(region_name=creds["AWS_REGION"]),
        aws_access_key_id=creds["AWS_ACCESS_KEY_ID"],
        aws_secret_access_key=creds["AWS_SECRET_ACCESS_KEY"],
        aws_session_token=creds["AWS_SESSION_TOKEN"],
    )


def send_ssh_key(saml_client: "SAMLClient", instance: str, ssh_key: "SymConfigFile"):
    user = get_ssh_user()
    ssm_client = boto_client(saml_client, "ssm")
    # fmt: off
    command = dedent(
        f"""
        #!/bin/bash
        mkdir -p "$(echo ~{user})/.ssh"
        echo "{ssh_key.path.with_suffix('.pub').read_text()}" >> "$(echo ~{user})/.ssh/authorized_keys"
        chown -R {user}:{user} "$(echo ~{user})/.ssh"
        """
    ).strip()
    # fmt: on
    ssm_client.send_command(
        InstanceIds=[instance],
        DocumentName="AWS-RunShellScript",
        Comment="SSH Key for Sym",
        Parameters={"commands": command.splitlines()},
    )


def find_instance(saml_client, keys, value) -> Optional[str]:
    creds = saml_client.get_creds()
    ec2_client = boto_client(saml_client, "ec2")
    for key in keys:
        response = ec2_client.describe_instances(
            Filters=[{"Name": key, "Values": [value]}], MaxResults=5
        )
        if response["Reservations"]:
            return response["Reservations"][0]["Instances"][0]["InstanceId"]


def host_to_instance(saml_client, host: str) -> str:
    if InstanceIDPattern.match(host):
        target = host
    elif validators.ip_address.ipv4(host):
        target = find_instance(saml_client, ("ip-address", "private-ip-address"), host)
    else:
        target = find_instance(saml_client, ("dns-name", "private-dns-name"), host)

    if not target:
        raise InstanceNotFound(host)

    return target
