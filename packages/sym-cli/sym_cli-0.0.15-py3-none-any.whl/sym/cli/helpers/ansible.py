from typing import Tuple

from ..decorators import intercept_errors, run_subprocess
from ..helpers.params import get_ssh_user
from ..helpers.ssh import SSHKey


def run_ansible(
    client: "SAMLClient", command: Tuple[str, ...], binary: str = "ansible"
):
    ssh_args = " ".join(
        [
            "-o StrictHostKeyChecking=no",
            f'-o ProxyCommand="sh -c \\"sym ssh-session-with-key {client.resource} --host %h --port %p\\""',
        ]
    )
    client.exec(
        binary,
        *command,
        f"--ssh-common-args={ssh_args}",
        f"--user={get_ssh_user()}",
        f"--private-key={str(SSHKey)}",
        suppress_=True,
    )
