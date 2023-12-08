import requests
from lxml import etree
from io import StringIO, BytesIO
import glob

def main():
    xml_files = glob.glob("*xml")
    for xml_file in xml_files:
        tree = etree.parse(xml_file)
        root = tree.getroot()
        for base_url in root.getchildren():
            for url in base_url:
                # if url.text and "https" in url.text and "/p/" in url.text and "en_us" in url.text:
                if url.text and "json" in url.text:
                    print(url.text)

if __name__ == "__main__":
    main()