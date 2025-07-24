#!/usr/bin/python3

"""
markdown2html.py

A simple Markdown to HTML converter.

Usage: ./markdown2html.py README.md README.html
"""

import sys


def convert_unordered_list(line, in_list):

    ul_line = ""
    if line.startswith("-"):
        unordered_list = line.strip("-")
        if not in_list:
            ul_line = ul_line + "<ul>\n"
            in_list = True
        ul_line+=f"\t<li>{unordered_list.strip()}</li>\n"
        return ul_line
    else:
        ul_line+="</ul>\n"
        in_list = False

    return line


def convert_heading(line):
    if line.startswith("#"):
        heading_level = line.count("#")
        heading_text = line.strip("# ").strip()
        heading = f"<h{heading_level}>{heading_text}</h{heading_level}>"
        return heading
    return line


def markdown_file(name, output):
    try:
        with open(name, 'r') as file:
            markdown_lines = file.readlines()

        converted_lines = []
        in_list = False
        for line in markdown_lines:
            converted_line = convert_heading(line)
            converted_line = convert_unordered_list(converted_line, in_list)
            converted_lines.append(f"{converted_line}\n")

        with open(output, 'w') as file:
            for line in converted_lines:
                file.write(line)

    except FileNotFoundError:
        sys.stderr.write(f"Missing {name}\n")
        sys.exit(1)


if __name__ == '__main__':
    if len(sys.argv) != 3:
        sys.stderr.write("Usage: ./markdown2html.py README.md README.html\n")
        sys.exit(1)

    markdown_file(sys.argv[1], sys.argv[2])
    