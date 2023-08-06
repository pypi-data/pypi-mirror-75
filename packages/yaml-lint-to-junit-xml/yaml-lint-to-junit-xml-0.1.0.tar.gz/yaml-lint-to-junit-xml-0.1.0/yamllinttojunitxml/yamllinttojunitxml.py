import fileinput
import re
import xml.dom.minidom
import xml.etree.cElementTree as ET


LINE_REGEX = re.compile(r"^(.*?):(\d+?:\d+?): \[([a-z]+?)\]\s(.*)$")


def get_input():
    """Read input from stdin or filenames passed through args
    """
    return [line.strip() for line in fileinput.input() if line and len(line.strip())]


def parse_lint_line(lint_line):
    """Parse an yaml lint line and extract fields filename, line, lint error
    """
    match = LINE_REGEX.match(lint_line)

    return (match.group(1), match.group(2), match.group(3), match.group(4))


def prettify(elem):
    """Return a pretty-printed XML string for the Element.
    """
    rough_string = ET.tostring(elem, "utf-8")
    reparsed = xml.dom.minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="\t")


def lint_to_junit_xml(lint_output):
    """Convert lint output lines to junit xml
    """
    testsuite = ET.Element(
        "testsuite",
        name="yaml-lint",
        tests=str(len(lint_output)),
        errors=str(len(lint_output)),
    )

    if not lint_output:
        # Output an empty test case to avoid breaking some junit xml processors
        ET.SubElement(testsuite, "testcase", name="no linting errors found")
        return testsuite

    for line in lint_output:
        filename, linenr, lint_exception_type, lint_exception_text = parse_lint_line(line)

        error_description = """
yaml-lint exception type: {0}
yaml-lint exception description: {1}
filename: {2}
line nr: {3}
        """.format(
            lint_exception_type, lint_exception_text, filename, linenr
        )

        testcase = ET.SubElement(testsuite, "testcase", name=lint_exception_text)
        ET.SubElement(
            testcase, "failure", message=line, type="yaml-lint"
        ).text = error_description
    return testsuite


def main():
    yaml_lint_output = get_input()

    testsuites = lint_to_junit_xml(yaml_lint_output)

    parsed_lines_xml = prettify(testsuites)
    print(parsed_lines_xml)


if __name__ == "__main__":
    main()
