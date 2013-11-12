#!/usr/bin/python -u

import argparse
import collections
import contextlib
import os
import pickle
import re
import string
import sys
import urllib2

PRE = re.compile(r'<pre>(.*?)</pre>', re.I | re.S)

#
# Script Error
#

def error(message):
    print message
    sys.exit(1)

#
# Template Retriever
#

def get_letter(letter, style):
    url = 'http://www.network-science.de/ascii/ascii.php?TEXT={}&FONT={}&RICH=no&FORM=left'.format(letter, style)

    with contextlib.closing(urllib2.urlopen(url)) as f:
        html = f.read()

    template = '\n'.join(x for x in PRE.findall(html)[1].splitlines() if x)

    return (template_width(template), template_height(template), template)

def get_style(style_name):
    style_file = os.path.normpath(os.path.join(os.path.dirname(__file__), 'styles', '{}.style'.format(style_name)))

    try:
        with open(style_file, 'rb') as f:
            print 'Loading Style', style_name
            return pickle.load(f)
    except:
        print 'Stealing Style', style_name

    style = {}
    print ' ',
    for letter in string.ascii_letters + '`1234567890-=~!@#$%^&*()_+[]{},.<>/?\'"\\|':
        sys.stdout.write(letter)
        style[letter] = get_letter(letter, style_name)
    sys.stdout.write('\n')

    with open(style_file, 'wb')  as f:
        pickle.dump(style, f)

    return style

#
# Template Calculators
#

def template_width(template):
    return len(max(template.split('\n'), key=len))

def template_height(template):
    return len(template.split('\n'))

#
# Money Maker
#

def format(text, style, dx, dy):
    x, y, min_x, min_y, max_x, max_y = 0, 0, 0, 0, 0, 0

    output = collections.defaultdict(lambda: collections.defaultdict(lambda: ' '))
    style  = get_style(arguments.style)

    if ',' in dx:
        dx = map(int, dx.split(',') + ['0'])
        if len(dx) != len(text):
            error('-x needs one value for between each letter')
    else:
        dx = int(dx)
    if ',' in dy:
        dy = map(int, dy.split(',') + ['0'])
        if len(dy) != len(text):
            error('-y needs one value for between each letter')
    else:
        dy = int(dy)

    _dx = lambda x: int(dx[x]) if type(dx) is list else int(dx)
    _dy = lambda x: int(dy[x]) if type(dy) is list else int(dy)

    for _letter, letter in enumerate(text):
        template_x, template_y, template = style[letter]

        min_x, min_y = min(min_x, x), min(min_y, y)

        for _y, line in enumerate(template.splitlines()):
            space = True
            for _x, character in enumerate(line):
                if space and character == ' ':
                    continue
                space = False
                output[y + _y][x + _x] = character
            max_x = max(max_x, x + _x + 1)
        max_y = max(max_y, y + _y + 1)

        x, y = x + template_x + _dx(_letter), y + _dy(_letter)

    for y in range(min_y, max_y):
        for x in range(min_x, max_x):
            sys.stdout.write(output[y][x])
        if y < max_y - 1:
            sys.stdout.write('\n')

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('text',                                     help='text to format')
    parser.add_argument('-x', action='store',      default='0',       help='x offset')
    parser.add_argument('-y', action='store',      default='0',       help='y offset')
    parser.add_argument('--style', action='store', default='ascii', help='style name')

    arguments = parser.parse_args()

    format(arguments.text, arguments.style, arguments.x, arguments.y)