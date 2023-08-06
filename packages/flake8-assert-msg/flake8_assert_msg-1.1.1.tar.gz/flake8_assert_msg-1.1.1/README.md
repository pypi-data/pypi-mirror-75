# flake8-assert-msg

flake8 plugin which forbids assert statements without messages.

## Installation

`pip install flake8-assert-msg`

## flake8 codes

| Code   | Description             |
|--------|-------------------------|
| ASS001 | do not use bare asserts |

## Rationale

This ensures that assertions have clear messages for failures. Adding a message to an assertion also acts as documentation for why the assertion is present.

## As a pre-commit hook

See [pre-commit](https://github.com/pre-commit/pre-commit) for instructions

Sample `.pre-commit-config.yaml`:

```yaml
-   repo: https://gitlab.com/pycqa/flake8
    rev: 3.8.1
    hooks:
    -   id: flake8
        additional_dependencies: [flake8-assert-msg==1.1.1]
```

## Acknowledgements

-   https://github.com/asottile/flake8-walrus used as a template
