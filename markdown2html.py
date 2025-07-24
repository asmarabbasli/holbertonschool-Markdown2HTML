#!/usr/bin/python3
"""
markdown2html.py

A simple Markdown to HTML converter.

Usage: ./markdown2html.py README.md README.html
"""

import sys


def convert_heading(line):
    if line.startswith("#"):
        level = len(line) - len(line.lstrip('#'))
        text = line.strip('#').strip()
        return f"<h{level}>{text}</h{level}>"
    return None


def is_unordered(line):
    return line.lstrip().startswith(("*", "-"))


def extract_list_item(line):
    return line.lstrip()[1:].strip()


def markdown_file(input_file, output_file):
    try:
        with open(input_file, 'r') as f:
            lines = f.readlines()

        output_lines = []
        in_list = False

        for i, line in enumerate(lines):
            stripped = line.strip()

            if not stripped:
                continue  # skip blank lines

            heading = convert_heading(stripped)
            if heading:
                if in_list:
                    output_lines.append("</ul>\n")
                    in_list = False
                output_lines.append(heading + "\n")

            elif is_unordered(stripped):
                if not in_list:
                    output_lines.append("<ul>\n")
                    in_list = True
                output_lines.append(f"<li>{extract_list_item(stripped)}</li>\n")

            else:
                if in_list:
                    output_lines.append("</ul>\n")
                    in_list = False
                output_lines.append(stripped + "\n")  # fallback for other text

        if in_list:
            output_lines.append("</ul>\n")

        with open(output_file, 'w') as f:
            f.writelines(output_lines)

    except FileNotFoundError:
        sys.stderr.write(f"Missing {input_file}\n")
        sys.exit(1)


if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.stderr.write("Usage: ./markdown2html.py README.md README.html\n")
        sys.exit(1)

    markdown_file(sys.argv[1], sys.argv[2])
