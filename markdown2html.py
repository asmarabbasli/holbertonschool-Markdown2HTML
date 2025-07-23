'''#!/usr/bin/env python3
"""Script to validate markdown to HTML conversion arguments"""

import sys
import os

if len(sys.argv) != 3:
    print("Usage: ./markdown2html.py README.md README.html", file=sys.stderr)
    exit(1)

input_file = sys.argv[1]

if not os.path.isfile(input_file):
    print(f"Missing {input_file}", file=sys.stderr)
    exit(1)

# If we get here, everything is fine
exit(0)
'''

#!/usr/bin/env python3
"""Converts Markdown headings to HTML"""

import sys
import os

# Check for correct number of arguments
if len(sys.argv) != 3:
    print("Usage: ./markdown2html.py README.md README.html", file=sys.stderr)
    exit(1)

input_file = sys.argv[1]
output_file = sys.argv[2]

# Check if input file exists
if not os.path.isfile(input_file):
    print(f"Missing {input_file}", file=sys.stderr)
    exit(1)

try:
    with open(input_file, 'r') as md_file, open(output_file, 'w') as html_file:
        for line in md_file:
            stripped = line.strip()
            if stripped.startswith("#"):
                # Count leading '#' to determine heading level
                level = len(stripped) - len(stripped.lstrip('#'))
                text = stripped.lstrip('#').strip()
                if 1 <= level <= 6:
                    html_file.write(f"<h{level}>{text}</h{level}>\n")
except Exception as e:
    print(f"Error: {e}", file=sys.stderr)
    exit(1)

exit(0)
