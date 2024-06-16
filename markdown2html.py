#!/usr/bin/python3

"""
Markdown script using python.
"""
import sys
import os.path

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print('Usage: ./markdown2html.py README.md README.html', file=sys.stderr)
        exit(1)

    if not os.path.isfile(sys.argv[1]):
        print('Missing {}'.format(sys.argv[1]), file=sys.stderr)
        exit(1)

    with open(sys.argv[1]) as read:
        with open(sys.argv[2], 'w') as html:
            html.write("")  # Create an empty HTML file
    exit(0)
