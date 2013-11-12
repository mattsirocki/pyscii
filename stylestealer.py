#!/usr/bin/python -u

import contextlib, os, pickle, re, string, sys, urllib2

PRE = re.compile(r'<pre>(.*?)</pre>', re.I | re.S)

def _jn(*args):
    return os.path.normpath(os.path.join(*args))

def get_letter(letter, style):
    url = 'http://www.network-science.de/ascii/ascii.php?TEXT={}&FONT={}&RICH=no&FORM=left'.format(letter, style)

    with contextlib.closing(urllib2.urlopen(url)) as f:
        html = f.read()

    return os.linesep.join(x for x in PRE.findall(html)[1].strip('\n').splitlines() if x)

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

if __name__ == '__main__':
    for style_name in sys.argv[1:]:
        try:
            style = get_style(style_name)
        except KeyboardInterrupt:
            print
            sys.exit(1)