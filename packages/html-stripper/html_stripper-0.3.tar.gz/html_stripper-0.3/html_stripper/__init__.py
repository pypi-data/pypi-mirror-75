import re
from html.parser import HTMLParser

_markedsectionclose = re.compile(r"]\s*]\s*>")
_msmarkedsectionclose = re.compile(r"]\s*>")
_markedsectionclose2 = re.compile(r">")


class HTMLStripper(HTMLParser):
    def __init__(self):
        self.reset()
        self.strict = False
        self.convert_charrefs = True
        self.fed = []

    def handle_data(self, d):
        tag = self.get_starttag_text().lower()
        if not tag or not tag.startswith(("<script", "<style", "<head", "<title", "<meta")):
            self.fed.append(d)
        else:
            pass

    def parse_marked_section(self, i, report=1):
        match = None
        rawdata = self.rawdata
        assert rawdata[i:i+3] == "<![", "unexpected call to parse_marked_section()"
        sectName, j = self._scan_name(i+3, i)
        if j < 0:
            return j
        if sectName in ["temp", "cdata", "ignore", "include", "rcdata"]:
            # look for standard ]]> ending
            match = _markedsectionclose.search(rawdata, i+3)
        elif sectName in ["if", "else", "endif"]:
            # look for MS Office ]> ending
            match = _msmarkedsectionclose.search(rawdata, i+3)
        else:
            # probably some broken tag, just skip to closing ">"
            match = _markedsectionclose2.search(rawdata, i+1)
        if not match:
            return -1
        if report:
            j = match.start(0)
            self.unknown_decl(rawdata[i+3: j])
        return match.end(0)

    def get_data(self):
        return " ".join(self.fed)


def strip_multiple_newlines(text):
    return re.sub(r"(\r?\n *)+", "\n", re.sub(r" {2,}", "", re.sub(r"\t+", "", text))).strip()


def strip_tags(html):
    s = HTMLStripper()
    s.feed(html)
    return s.get_data()
