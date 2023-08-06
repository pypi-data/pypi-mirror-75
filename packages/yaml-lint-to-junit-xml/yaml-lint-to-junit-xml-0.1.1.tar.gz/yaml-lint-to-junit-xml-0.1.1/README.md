# Yaml Lint to jUnit XML

[![PyPI version](https://badge.fury.io/py/yaml-lint-to-junit-xml.svg)](https://badge.fury.io/py/yaml-lint-to-junit-xml)

Convert yaml-lint outputs to a jUnit valid xml tests result file.

Thanks to the author of the original project [ansible-lint-to-junit-xml](https://github.com/andreferreirav2/ansible-lint-to-junit-xml)

## Quickstart

Install `ansible-lint-to-junit-xml` with pip:

    pip install yaml-lint-to-junit-xml

Or you can simply get this repo and install with setup.py

## Usage

Run `yamllint` on the desired files and pipe to `yaml-lint-to-junit-xml`

    yamllint -f parsable <file or directly> | yaml-lint-to-junit-xml > results/yaml-lint-results.xml

Alternatively you can run `yamllint` separately from `yaml-lint-to-junit-xml` and use a file to pass the output


    yamllint -f parsable <file or directly> > yaml-lint-results.txt
    yaml-lint-to-junit-xml yaml-lint-results.txt > results/yaml-lint-results.xml

> **Note:** `yamllint` must run with `-f parsable` for the output to be machine parsable

## Features

-   Pipe output directly from `yamllint` call
-   Output XML file is compliant with [jenkins junit5 Schema](https://github.com/junit-team/junit5/blob/master/platform-tests/src/test/resources/jenkins-junit.xsd/).

## Example

Running `yamllint` on a file results in:

    roles/test_role/defaults/main.yml:25:121: [warning] line too long (157 > 120 characters) (line-length)
    roles/test_role/tasks/main.yml:33:35: [error] no new line character at the end of file (new-line-at-end-of-file)
    test_playbook.yml:4:8: [warning] truthy value should be one of [False, True, false, true] (truthy)

Running `yamllint` and piping the output to `yaml-lint-to-junit-xml` looks line this:

    yamllint -f parsable test_playbook.yml | yaml-lint-to-junit-xml

Would result in:

```
<?xml version="1.0" ?>
<testsuite errors="1" name="yaml-lint" tests="1">
        <testcase name="truthy value should be one of [False, True, false, true] (truthy)">
                <failure message="test_playbook.yml:4:8: [warning] truthy value should be one of [False, True, false, true] (truthy)" type="yaml-lint">
yaml-lint exception type: warning
yaml-lint exception description: truthy value should be one of [False, True, false, true] (truthy)
filename: test_playbook.yml
line nr: 4:8
        </failure>
        </testcase>
</testsuite>
```

