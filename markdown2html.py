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


def is_ordered_list_item(line):
    """Check if the line matches a strict ordered list item: starts with '*' followed by space."""
    return re.match(r'^\* .+', line)


def markdown_file(input_file, output_file):
    try:
        with open(input_file, 'r') as f:
            lines = f.readlines()

        output_lines = []
        in_ordered_list = False

        for line in lines:
            stripped = line.strip()

            # Blank line closes list
            if not stripped:
                if in_ordered_list:
                    output_lines.append("</ol>")
                    in_ordered_list = False
                continue

            # Ordered list item
            if is_ordered_list_item(stripped):
                if not in_ordered_list:
                    output_lines.append("<ol>")
                    in_ordered_list = True
                output_lines.append(f"<li>{stripped[2:].strip()}</li>")
                continue

            # Close list if current line is not a list item
            if in_ordered_list:
                output_lines.append("</ol>")
                in_ordered_list = False

            # Heading
            heading = convert_heading(stripped)
            if heading:
                output_lines.append(heading)
            else:
                output_lines.append(f"<p>{stripped}</p>")

        # Close ordered list at end if needed
        if in_ordered_list:
            output_lines.append("</ol>")

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
