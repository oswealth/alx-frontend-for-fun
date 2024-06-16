#!/usr/bin/python3

"""
Markdown script using python.
"""
import sys
import os.path
import re
import hashlib

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print('Usage: ./markdown2html.py README.md README.html', file=sys.stderr)
        exit(1)

    if not os.path.isfile(sys.argv[1]):
        print('Missing {}'.format(sys.argv[1]), file=sys.stderr)
        exit(1)

    with open(sys.argv[1]) as read:
        with open(sys.argv[2], 'w') as html:
            unordered_start, ordered_start, paragraph = False, False, False
            
            for line in read:
                # Handle bold and emphasis
                line = line.replace('**', '<b>', 1).replace('**', '</b>', 1)
                line = line.replace('__', '<em>', 1).replace('__', '</em>', 1)

                # Handle MD5 conversion
                md5_matches = re.findall(r'\[\[(.+?)\]\]', line)
                for match in md5_matches:
                    md5_hash = hashlib.md5(match.encode()).hexdigest()
                    line = line.replace(f'[[{match}]]', md5_hash)

                # Handle removal of letter 'C'
                remove_c_matches = re.findall(r'\(\((.+?)\)\)', line)
                for match in remove_c_matches:
                    cleaned_text = ''.join(c for c in match if c.lower() != 'c')
                    line = line.replace(f'(({match}))', cleaned_text)

                length = len(line)
                headings = line.lstrip('#')
                heading_num = length - len(headings)
                unordered = line.lstrip('-')
                unordered_num = length - len(unordered)
                ordered = line.lstrip('*')
                ordered_num = length - len(ordered)
                
                # Handle headings
                if 1 <= heading_num <= 6:
                    line = '<h{}>{}</h{}>\n'.format(heading_num, headings.strip(), heading_num)

                # Handle unordered lists
                if unordered_num:
                    if not unordered_start:
                        html.write('<ul>\n')
                        unordered_start = True
                    line = '    <li>' + unordered.strip() + '</li>\n'
                if unordered_start and not unordered_num:
                    html.write('</ul>\n')
                    unordered_start = False

                # Handle ordered lists
                if ordered_num:
                    if not ordered_start:
                        html.write('<ol>\n')
                        ordered_start = True
                    line = '    <li>' + ordered.strip() + '</li>\n'
                if ordered_start and not ordered_num:
                    html.write('</ol>\n')
                    ordered_start = False

                # Handle paragraphs
                if not (heading_num or unordered_start or ordered_start):
                    if not paragraph and length > 1:
                        html.write('<p>\n')
                        paragraph = True
                    elif length > 1:
                        html.write('<br/>\n')
                    elif paragraph:
                        html.write('</p>\n')
                        paragraph = False

                if length > 1:
                    html.write(line)

            # Close any remaining open tags
            if unordered_start:
                html.write('</ul>\n')
            if ordered_start:
                html.write('</ol>\n')
            if paragraph:
                html.write('</p>\n')

    exit(0)
