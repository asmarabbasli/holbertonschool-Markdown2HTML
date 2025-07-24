#!/usr/bin/python3
"""
markdown2html.py

A simple Markdown to HTML converter.

Usage: ./markdown2html.py README.md README.html
"""

import sys
import os


def convert_heading(line):
    if line.startswith("#"):
        level = len(line) - len(line.lstrip('#'))
        text = line.strip('#').strip()
        return f"<h{level}>{text}</h{level}>"
    return None


def convert_unordered_list(line, in_list):
    if line.strip().startswith(("-", "*")):
        if not in_list:
            start = "<ul>\n"
        else:
            start = ""
        item = line.strip()[1:].strip()
        return start + f"<li>{item}</li>\n", True
    else:
        if in_list:
            return "</ul>\n" + line, False
        return line, False


def markdown_file(input_file, output_file):
    try:
        with open(input_file, 'r') as f:
            lines = f.readlines()

        output_lines = []
        in_list = False

        for line in lines:
            if line.strip() == "":
                continue

            heading = convert_heading(line)
            if heading:
                if in_list:
                    output_lines.append("</ul>\n")
                    in_list = False
                output_lines.append(heading + "\n")
            else:
                ul_line, in_list = convert_unordered_list(line, in_list)
                output_lines.append(ul_line)

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
