#!/usr/bin/python -u

import argparse, stylestealer, sys
import contextlib, os, pickle, re, string, sys, urllib2
import re

from collections import defaultdict




LETTER = re.compile(r'[a-zA-Z],[0-9]+,[0-9]+.*?(?=[a-zA-Z],[0-9]+,[0-9]+)', re.S)
PRE = re.compile(r'<pre>(.*?)</pre>', re.I | re.S)





def _jn(*args):
    return os.path.normpath(os.path.join(*args))

def get_letter(letter, style):
    url = 'http://www.network-science.de/ascii/ascii.php?TEXT={}&FONT={}&RICH=no&FORM=left'.format(letter, style)

    with contextlib.closing(urllib2.urlopen(url)) as f:
        html = f.read()

    template = '\n'.join(x for x in PRE.findall(html)[1].splitlines() if x)

    return (_width(template), _height(template), template)

def get_style(style_name):
    style_file = _jn(os.path.dirname(__file__), 'styles', '{}.style'.format(style_name))

    try:
        with open(style_file, 'rb') as f:
            print 'Loading Style', style_name
            return pickle.load(f)
    except:
        print 'Stealing Style', style_name

    style = {}
    print ' ',
    for letter in string.ascii_letters:
        print letter,
        style[letter] = get_letter(letter, style_name)
    print

    with open(style_file, 'wb')  as f:
        pickle.dump(style, f)

    return style




def template_width(template):
    return len(max(template.split('\n'), key=len))

def template_height(template):
    return len(template.split('\n'))






def load_style(style_name):
    with open('styles/{}.style2'.format(style_name), 'rb') as f:
        style_definition = f.read()

    style = {}

    for x in _LETTER.findall(style_definition):
        match = x.strip().split('\n', 1)
        data  = match[0].split(',')
        data[1:3] = map(int, data[1:3])
        style[data[0]] = (data[1], data[2], match[1])

    return style



def format(text, style, dx, dy):
    x, y, min_x, min_y, max_x, max_y = 0, 0, 0, 0, 0, 0

    output = defaultdict(lambda: defaultdict(lambda: ' '))

    for letter in text:
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

        x, y = x + template_x + dx, y + template_y + dy


    for y in range(min_y, max_y):
        for x in range(min_x, max_x):
            sys.stdout.write(output[y][x])
        sys.stdout.write('\n')

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('text',                                     help='text to format')
    parser.add_argument('-x', action='store',      default=0,       help='x offset', type=int)
    parser.add_argument('-y', action='store',      default=0,       help='x offset', type=int)
    parser.add_argument('--style', action='store', default='ascii', help='style name')

    arguments = parser.parse_args()

    #style = stylestealer.get_style(arguments.style)
    style = load_style(arguments.style)

    format(arguments.text, style, arguments.x, arguments.y)
