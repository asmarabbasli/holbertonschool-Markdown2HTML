#!/usr/bin/python3
"""
markdown2html.py

A simple Markdown to HTML converter.

Usage: ./markdown2html.py README.md README.html
"""

import sys
import re


def convert_heading(line):
    """Convert Markdown headings (#) to HTML <h1> to <h6>."""
    match = re.match(r'^(#{1,6})\s+(.*)', line)
    if match:
        level = len(match.group(1))
        text = match.group(2).strip()
        return f"<h{level}>{text}</h{level}>"
    return None


def is_list_item(line):
    """Check if the line is a Markdown list item."""
    return re.match(r'^\s*[-*]\s+.+', line)


def markdown_file(input_file, output_file):
    try:
        with open(input_file, 'r') as f:
            lines = f.readlines()

        output_lines = []
        in_list = False

        for line in lines:
            stripped = line.strip()

            # Handle blank lines
            if not stripped:
                if in_list:
                    output_lines.append("</ul>")
                    in_list = False
                continue

            # Handle list items
            if is_list_item(line):
                if not in_list:
                    output_lines.append("<ul>")
                    in_list = True
                item_text = re.sub(r'^\s*[-*]\s+', '', line).strip()
                output_lines.append(f"<li>{item_text}</li>")
                continue

            # Close list if we're no longer in one
            if in_list:
                output_lines.append("</ul>")
                in_list = False

            # Handle headings
            heading = convert_heading(stripped)
            if heading:
                output_lines.append(heading)
            else:
                output_lines.append(f"<p>{stripped}</p>")

        # Close any list left open at the end of file
        if in_list:
            output_lines.append("</ul>")

        with open(output_file, 'w') as f:
            f.write("\n".join(output_lines) + "\n")

    except FileNotFoundError:
        sys.stderr.write(f"Missing {input_file}\n")
        sys.exit(1)


if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.stderr.write("Usage: ./markdown2html.py README.md README.html\n")
        sys.exit(1)

    markdown_file(sys.argv[1], sys.argv[2])
