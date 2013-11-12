import re
import urllib2

re_pre = re.compile(r'<pre>(.*?)</pre>', re.I | re.S)

def get_letter(letter, style):
    f = urllib2.urlopen('http://www.network-science.de/ascii/ascii.php?TEXT={}&FONT={}&RICH=no&FORM=left'.format(letter, style))
    html = f.read()
    f.close()
    return re_pre.findall(html)[1].strip()


