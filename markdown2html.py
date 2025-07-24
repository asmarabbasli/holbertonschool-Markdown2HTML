#!/usr/bin/python3
"""
markdown2html.py

A simple Markdown to HTML converter.

Usage: ./markdown2html.py README.md README.html
"""

import sys
import re


def convert_heading(line):
    """Convert Markdown headings (# to ######) to HTML <h1> to <h6>."""
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
        in_ul = False
        in_ol = False
        in_paragraph = False

        for line in lines:
            stripped = line.strip()

            # Blank line: close any open tags (paragraph, lists)
            if not stripped:
                if in_paragraph:
                    output_lines.append("</p>")
                    in_paragraph = False
                if in_ul:
                    output_lines.append("</ul>")
                    in_ul = False
                if in_ol:
                    output_lines.append("</ol>")
                    in_ol = False
                continue

            # Check for heading
            heading = convert_heading(stripped)
            if heading:
                # Close any open tags before heading
                if in_paragraph:
                    output_lines.append("</p>")
                    in_paragraph = False
                if in_ul:
                    output_lines.append("</ul>")
                    in_ul = False
                if in_ol:
                    output_lines.append("</ol>")
                    in_ol = False

                output_lines.append(heading)
                continue

            # Ordered list detection (e.g. 1. item)
            ol_match = re.match(r'^(\d+)\.\s+(.*)', stripped)
            if ol_match:
                if in_paragraph:
                    output_lines.append("</p>")
                    in_paragraph = False
                if in_ul:
                    output_lines.append("</ul>")
                    in_ul = False
                if not in_ol:
                    output_lines.append("<ol>")
                    in_ol = True
                output_lines.append(f"<li>{ol_match.group(2)}</li>")
                continue

            # Unordered list detection (e.g. * item or - item)
            if stripped.startswith("* ") or stripped.startswith("- "):
                if in_paragraph:
                    output_lines.append("</p>")
                    in_paragraph = False
                if in_ol:
                    output_lines.append("</ol>")
                    in_ol = False
                if not in_ul:
                    output_lines.append("<ul>")
                    in_ul = True
                output_lines.append(f"<li>{stripped[2:].strip()}</li>")
                continue

            # Otherwise, normal paragraph text
            if not in_paragraph:
                # Close any open lists before starting paragraph
                if in_ul:
                    output_lines.append("</ul>")
                    in_ul = False
                if in_ol:
                    output_lines.append("</ol>")
                    in_ol = False
                output_lines.append(f"<p>{stripped}")
                in_paragraph = True
            else:
                # Continue paragraph on new line with a space
                output_lines[-1] = output_lines[-1] + ' ' + stripped

        # Close any open tags at the end of the file
        if in_paragraph:
            output_lines.append("</p>")
        if in_ul:
            output_lines.append("</ul>")
        if in_ol:
            output_lines.append("</ol>")

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
