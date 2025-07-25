#!/usr/bin/python3
"""
markdown2html.py

Markdown to HTML converter with support for:
- Headings (#)
- Ordered lists (*)
- Unordered lists (-)
- Multiline paragraphs with <br/>
- Bold (**text**)
- Emphasis (__text__)
- [[text]] → MD5 hash
- ((text)) → remove all 'c' and 'C'

Usage: ./markdown2html.py README.md README.html
"""

import sys
import re
import hashlib


def parse(text):
    # MD5 conversion: [[text]]
    text = re.sub(r'

\[

\[(.*?)\]

\]

', lambda m: hashlib.md5(m.group(1).encode()).hexdigest(), text)

    # Remove 'c' and 'C': ((text))
    text = re.sub(r'\(\((.*?)\)\)', lambda m: re.sub(r'[cC]', '', m.group(1)), text)

    # Bold: **text**
    text = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', text)

    # Emphasis: __text__
    text = re.sub(r'__(.*?)__', r'<em>\1</em>', text)

    return text


def convert_heading(line):
    match = re.match(r'^(#{1,6})\s+(.*)', line)
    if match:
        level = len(match.group(1))
        return f"<h{level}>{parse(match.group(2).strip())}</h{level}>"
    return None


def is_ordered_list_item(line):
    return re.match(r'^\s*\*\s+.+', line)


def is_unordered_list_item(line):
    return re.match(r'^\s*-\s+.+', line)


def markdown_file(input_file, output_file):
    try:
        with open(input_file, 'r') as f:
            lines = f.readlines()

        output_lines = []
        in_ordered_list = False
        in_unordered_list = False
        paragraph_buffer = []

        def flush_paragraph():
            if paragraph_buffer:
                output_lines.append("<p>")
                for i, line in enumerate(paragraph_buffer):
                    content = parse(line.strip())
                    if i > 0:
                        output_lines.append("<br/>")
                    output_lines.append(content)
                output_lines.append("</p>")
                paragraph_buffer.clear()

        for line in lines:
            stripped = line.strip()

            if not stripped:
                flush_paragraph()
                if in_ordered_list:
                    output_lines.append("</ol>")
                    in_ordered_list = False
                if in_unordered_list:
                    output_lines.append("</ul>")
                    in_unordered_list = False
                continue

            heading = convert_heading(stripped)
            if heading:
                flush_paragraph()
                if in_ordered_list:
                    output_lines.append("</ol>")
                    in_ordered_list = False
                if in_unordered_list:
                    output_lines.append("</ul>")
                    in_unordered_list = False
                output_lines.append(heading)
                continue

            if is_ordered_list_item(line):
                flush_paragraph()
                if not in_ordered_list:
                    if in_unordered_list:
                        output_lines.append("</ul>")
                        in_unordered_list = False
                    output_lines.append("<ol>")
                    in_ordered_list = True
                item = re.sub(r'^\s*\*\s+', '', line).strip()
                output_lines.append(f"<li>{parse(item)}</li>")
                continue

            if is_unordered_list_item(line):
                flush_paragraph()
                if not in_unordered_list:
                    if in_ordered_list:
                        output_lines.append("</ol>")
                        in_ordered_list = False
                    output_lines.append("<ul>")
                    in_unordered_list = True
                item = re.sub(r'^\s*-\s+', '', line).strip()
                output_lines.append(f"<li>{parse(item)}</li>")
                continue

            # Regular paragraph line
            paragraph_buffer.append(stripped)

        flush_paragraph()
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
