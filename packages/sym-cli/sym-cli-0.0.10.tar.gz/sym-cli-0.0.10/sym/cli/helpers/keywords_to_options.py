from typing import List, Mapping, Sequence, Union

Options = Mapping[str, Union[str, bool]]
Argument = Union[str, Options]


def keywords_to_options(args: Sequence[Argument]) -> List[str]:
    """
    Converts any dicts in the given arguments into a sequence of
    options. The keys correspond to option names (with underscores
    replaced with hyphens). String values correspond to option
    arguments; boolean values correspond to the presence or
    absence of the option, with no argument.
    """

    result = []
    for arg in args:
        if isinstance(arg, str):
            result.append(arg)
        else:
            for (key, value) in arg.items():
                option = "--" + key.replace("_", "-")
                if value:
                    result.append(option)
                    if isinstance(value, str):
                        result.append(value)
    return result
