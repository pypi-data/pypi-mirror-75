from contextlib import contextmanager
from typing import Callable, ContextManager, Iterator, Type, TypeVar

import pytest

from sym.cli.saml_clients import SAMLClient
from sym.cli.tests.conftest import CustomOrgFixture
from sym.cli.tests.helpers.sandbox import Sandbox

P = TypeVar("P", bound=SAMLClient)
TestContextFixture = Callable[..., ContextManager[P]]


@pytest.fixture
def test_context(
    constructor: Type[P], sandbox: Sandbox, custom_org: CustomOrgFixture
) -> TestContextFixture[P]:
    @contextmanager
    def context(*, debug: bool) -> Iterator[P]:
        with sandbox.push_xdg_config_home(), custom_org("launch-darkly"):
            sandbox.create_file(f"bin/{constructor.binary}", 0o755)
            with sandbox.push_exec_path():
                yield constructor("catfood", debug=debug)

    return context
