import json
import requests
from lxml import etree
from io import StringIO, BytesIO
import glob
import pycurl
import base64

class LushCollection():

    def __init__(self, name: str, slug: str, id: str) -> None:
        self.name = name
        self.slug = slug
        self.encoded_id = id
        self.id = base64.b64decode(self.encoded_id).decode()


def main():
    # Starting URL 
    base_url = "https://www.lush.com/_next/data/production-fc6e68c6/us/en_us.json?channel=us&language=en_us"

    headers =  {   
        "Host": "www.lush.com",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:125.0) Gecko/20100101 Firefox/125.0",
        "Accept": "*/*",
        "Accept-Language": "en-US,en;q=0.5",
        # "Accept-Encoding": "gzip, deflate, br",
        "x-nextjs-data": "1",
        "sentry-trace": "99c0ba2dec064a84abc8c45e9e58b35b-a93021845075e2b3-0",
        "baggage": "sentry-environment=production,sentry-release=commerce%402.44.1,sentry-public_key=6f67d17ea2354e9885202e18fcb5a8a9,sentry-trace_id=99c0ba2dec064a84abc8c45e9e58b35b,sentry-sample_rate=0,sentry-transaction=%2F%5Bchannel%5D%2F%5Blanguage%5D,sentry-sampled=false",
        "Connection": "keep-alive",
        "Cookie": "lush-commerce-cookies=%7B%22necessary%22%3Atrue%2C%22statistical%22%3Atrue%2C%22chat%22%3Atrue%2C%22reviews%22%3Atrue%7D; guestId=aacce9ee-7663-49ea-9b40-8f7aeb886a7a; __cf_bm=Gkhx4qgg35cKuSXH1nF_hHb7DJz3EZu5sH_ApcAua7g-1714449071-1.0.1.1-ltTQ40i_.GhtMwx9Bu9Ok4yrcyQ2TrqJHU885gqVl9QuN5naXeWFlNateuXaFCxd5RjDeXdHJTdWzzc2GTCrxA",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "Pragma": "no-cache",
        "Cache-Control": "no-cache",
        "TE": "trailers"
    }
    # response = requests.get(base_url, headers=headers)
    # print(response.text)

    response_buffer = BytesIO()
    pycurl_connect = pycurl.Curl()
    pycurl_connect.setopt(pycurl.URL, base_url)
    generate_headers = [f"{header_key}: {header_value}" for header_key, header_value in headers.items()]
    pycurl_connect.setopt(pycurl.HTTPHEADER, generate_headers)
    pycurl_connect.setopt(pycurl.WRITEDATA, response_buffer)
    pycurl_connect.perform()
    pycurl_connect.close()

    response_bytes = response_buffer.getvalue()
    string = response_bytes.decode('iso-8859-1')
    print(string)
    json_value = json.loads(string)
    
    collections = json_value["pageProps"]["collections"]["items"]
    # Get the names and slugs of each collection

    for collection_item in collections:
        cur_item = LushCollection(collection_item["collection"]["name"],
                                  collection_item["collection"]["slug"],
                                  collection_item["collection"]["id"])
        print(cur_item.id)

if __name__ == "__main__":
    main()