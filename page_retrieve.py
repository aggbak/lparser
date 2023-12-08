import json
import requests
from lxml import etree
from io import StringIO, BytesIO
import glob


def main():
    headers = {
        "Accept": "*/*",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate, br",
        "content-type": "application/json",
        "Origin": "https://www.lush.com",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "Pragma": "no-cache",
        "Cache-Control": "no-cache",
        "TE": "trailers"
    }

    payload_str = '[{"operationName":"ProductCollections","variables":{"id":"UHJvZHVjdDo5MjE4","channel":"us","languageCode":"EN_US"},"query":"query ProductCollections($id: ID, $slug: String, $channel: String, $languageCode: LanguageCodeEnum!) {\n product(id: $id, slug: $slug, channel: $channel) {\n collections {\n id\n name\n slug\n translation(languageCode: $languageCode) {\n name\n __typename\n }\n __typename\n }\n __typename\n }\n}"}]'
    payload_obj = json.loads(payload_str, strict=False)
    result = requests.post("https://www.lush.com/api/gateway", headers=headers, data=payload_str)
    print(result)
    print(result.text)
    
if __name__ == "__main__":
    main()