# Latolog

Simple customizable logging.
> Only JSON mode is supported at the moment. XML is WIP

## Installation

    pip install LatoLog

## Usage example

    import LatoLog

    my_content = { "a": 1, "b", 2 }

    latolog = LatoLog()

    latolog.print_log(my_content)

    >>> {"timestamp": "04-12-2019 16:43:49", "a": 1, "b": 2 }
