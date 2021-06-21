import re

class Parser(object):

    def __init__(self, raw_text: bytes):
        self.text = raw_text

    def convert_to_paragraphs(self) -> str:
        text = self.text.replace('\r', '')
        text = text.replace('\n', '')
        rslt = re.sub(r'\s+',' ', text)
        rslt = rslt.strip()

        return rslt
