from click import ClickException


class CliErrorMeta(type):
    _exit_code_count = 1

    def __new__(cls, name, bases, attrs):
        cls._exit_code_count += 1
        klass = super().__new__(cls, name, bases, attrs)
        klass.exit_code = cls._exit_code_count
        return klass


class CliError(ClickException, metaclass=CliErrorMeta):
    pass


class SuppressedError(CliError):
    def show(self):
        pass


class UnavailableRoleError(CliError):
    def __init__(self) -> None:
        super().__init__(
            "The role you requested is not available. Please wait for approval and retry."
        )


class InstanceNotFound(CliError):
    def __init__(self, instance) -> None:
        super().__init__(f"Could not find instance {instance}")


class FailedSubprocessError(CliError):
    def __init__(self, command) -> None:
        super().__init__(f"Cannot run: {command}")
