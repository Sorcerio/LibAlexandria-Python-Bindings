# LibAlexandria: Python 3 Bindings

>
> A dynamic standard for storing written works.
>

- [LibAlexandria: Python 3 Bindings](#libalexandria-python-3-bindings)
  - [Usage](#usage)
  - [Running Tests](#running-tests)

---

These bindings allow for control of [LibAlexandria](https://github.com/maximombro/LibAlexandria-Specifications) Library from within the Python 3 environment.

## Usage

Use `LibAlexItem.fromMetaFile(...)` function to load your LibAlexandria compatible `meta.json` files.

## Running Tests

The LibAlexandria Python 3 binding use the built-in `unittest` library for testing.
No additional requirements are needed to run the tests.

1. Open a terminal in the directory that this [README](./) is in.
2. Run `python.exe -m unittest discover tests`.
3. Wait for completion and review the report.
