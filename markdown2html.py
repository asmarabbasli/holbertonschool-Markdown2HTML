#!/usr/bin/python3
"""
markdown2html.py

Markdown to HTML converter with support for headings,
ordered lists (*), unordered lists (-), and ignores plain text.

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
    """Identify ordered list items starting with '*' followed by a space."""
    return re.match(r'^\s*\*\s+.+', line)


def is_unordered_list_item(line):
    """Identify unordered list items starting with '-' followed by a space."""
    return re.match(r'^\s*-\s+.+', line)


def markdown_file(input_file, output_file):
    try:
        with open(input_file, 'r') as f:
            lines = f.readlines()

        output_lines = []
        in_ordered_list = False
        in_unordered_list = False

        for line in lines:
            stripped = line.strip()

            # Blank line closes any open list
            if not stripped:
                if in_ordered_list:
                    output_lines.append("</ol>")
                    in_ordered_list = False
                if in_unordered_list:
                    output_lines.append("</ul>")
                    in_unordered_list = False
                continue

            # Ordered list item (*)
            if is_ordered_list_item(line):
                if not in_ordered_list:
                    if in_unordered_list:
                        output_lines.append("</ul>")
                        in_unordered_list = False
                    output_lines.append("<ol>")
                    in_ordered_list = True
                item = re.sub(r'^\s*\*\s+', '', line).strip()
                output_lines.append(f"<li>{item}</li>")
                continue

            # Unordered list item (-)
            if is_unordered_list_item(line):
                if not in_unordered_list:
                    if in_ordered_list:
                        output_lines.append("</ol>")
                        in_ordered_list = False
                    output_lines.append("<ul>")
                    in_unordered_list = True
                item = re.sub(r'^\s*-\s+', '', line).strip()
                output_lines.append(f"<li>{item}</li>")
                continue

            # Close any open list before heading
            if in_ordered_list:
                output_lines.append("</ol>")
                in_ordered_list = False
            if in_unordered_list:
                output_lines.append("</ul>")
                in_unordered_list = False

            # Headings
            heading = convert_heading(stripped)
            if heading:
                output_lines.append(heading)
            else:
                # Ignore non-markdown plain text
                continue

        # Close any remaining open lists
        if in_ordered_list:
            output_lines.append("</ol>")
        if in_unordered_list:
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
