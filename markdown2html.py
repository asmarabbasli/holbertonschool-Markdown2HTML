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

def markdown_file(input_file, output_file):
    try:
        with open(input_file, 'r') as f:
            lines = f.readlines()

        output_lines = []
        in_list = False

        for line in lines:
            stripped = line.strip()

            # Handle blank line
            if not stripped:
                if in_list:
                    output_lines.append("</ul>")
                    in_list = False
                continue

            # Handle list item
            if stripped.startswith("* ") or stripped.startswith("- "):
                if not in_list:
                    output_lines.append("<ul>")
                    in_list = True
                output_lines.append(f"<li>{stripped[2:].strip()}</li>")
                continue

            # Close list if line is not a list item
            if in_list:
                output_lines.append("</ul>")
                in_list = False

            # Handle heading
            heading = convert_heading(stripped)
            if heading:
                output_lines.append(heading)
            else:
                # Treat remaining text as paragraph
                output_lines.append(f"<p>{stripped}</p>")

        # Close list at end of file
        if in_list:
            output_lines.append("</ul>")

        with open(output_file, 'w') as f:
            for line in output_lines:
                f.write(f"{line}\n")

    except FileNotFoundError:
        sys.stderr.write(f"Missing {input_file}\n")
        sys.exit(1)


if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.stderr.write("Usage: ./markdown2html.py README.md README.html\n")
        sys.exit(1)

    markdown_file(sys.argv[1], sys.argv[2])
