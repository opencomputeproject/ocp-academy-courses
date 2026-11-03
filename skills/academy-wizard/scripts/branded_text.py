"""Apply the Academy's visible OCP Ready trademark without changing metadata."""
from functools import wraps
from html.parser import HTMLParser
import re

class _VisibleTrademark(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=False)
        self.parts = []
        self.stack = []

    def handle_starttag(self, tag, attrs):
        self.parts.append(self.get_starttag_text())
        if tag not in {'area','base','br','col','embed','hr','img','input','link','meta','param','source','track','wbr'}:
            self.stack.append(tag)

    def handle_startendtag(self, tag, attrs):
        self.parts.append(self.get_starttag_text())

    def handle_endtag(self, tag):
        self.parts.append('</'+tag+'>')
        if tag in self.stack:
            index=len(self.stack)-1-self.stack[::-1].index(tag)
            del self.stack[index:]

    def handle_data(self, data):
        if not any(tag in {'script','style','title','textarea'} for tag in self.stack):
            data=re.sub(r'OCP Ready™', 'OCP Ready<sup class="brand-trademark">TM</sup>', data)
        self.parts.append(data)

    def handle_entityref(self,name):self.parts.append('&'+name+';')
    def handle_charref(self,name):self.parts.append('&#'+name+';')
    def handle_comment(self,data):self.parts.append('<!--'+data+'-->')
    def handle_decl(self,data):self.parts.append('<!'+data+'>')

def format_trademarks(document):
    parser=_VisibleTrademark();parser.feed(document);parser.close()
    return ''.join(parser.parts)

def visible_trademarks(renderer):
    @wraps(renderer)
    def decorated(*args,**kwargs):return format_trademarks(renderer(*args,**kwargs))
    return decorated
