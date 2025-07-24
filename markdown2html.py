#!/usr/bin/python3
"""
markdown2html.py

A simple Markdown to HTML converter.

Usage: ./markdown2html.py README.md README.html
"""

import sys


def convert_heading(line):
    if line.startswith("#"):
        heading_level = line.count("#")
        heading_text = line.strip("# ").strip()
        heading = f"<h{heading_level}>{heading_text}</h{heading_level}>"
        return heading
    return None


def markdown_file(name, output):
    try:
        with open(name, 'r') as file:
            markdown_lines = file.readlines()

        converted_lines = []
        in_list = False

        for i, line in enumerate(markdown_lines):
            stripped = line.strip()

            if not stripped:
                # Empty line, close list if open
                if in_list:
                    converted_lines.append("</ul>")
                    in_list = False
                continue

            # Handle unordered list
            if stripped.startswith("- "):
                if not in_list:
                    converted_lines.append("<ul>")
                    in_list = True
                item = stripped[2:].strip()
                converted_lines.append(f"<li>{item}</li>")
            else:
                if in_list:
                    converted_lines.append("</ul>")
                    in_list = False
                # Handle heading
                heading = convert_heading(line)
                if heading:
                    converted_lines.append(heading)
                else:
                    converted_lines.append(stripped)

        if in_list:
            converted_lines.append("</ul>")  # Close final list if still open

        with open(output, 'w') as file:
            for line in converted_lines:
                file.write(f"{line}\n")

    except FileNotFoundError:
        sys.stderr.write(f"Missing {name}\n")
        sys.exit(1)


if __name__ == '__main__':
    if len(sys.argv) != 3:
        sys.stderr.write("Usage: ./markdown2html.py README.md README.html\n")
        sys.exit(1)

    markdown_file(sys.argv[1], sys.argv[2])
