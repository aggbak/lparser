import pycurl
from io import BytesIO, StringIO
import gzip
import os
import base64
import json
import sqlite3

def get_ingredients_page(page_num: int):
    headers = {
        "Origin": "https://www.lush.com",
        "Accept-Language":"en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate",
        "content-type": "application/json",
        "Connection": "keep-alive",
        "Accept": "*/*",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:126.0) Gecko/20100101 Firefox/126.0"
        }
    req_headers = [f"{header_key}: {header_value}" for header_key, header_value in headers.items()]
    ingredients_search_payload = r'[{"operationName":"algoliaSearch","variables":{"indexName":"pages","query":"","facetFilters":["isPublished:true","pageType:ingredient","page_clients:commerce_web","page_channels:us"],"page":2},"query":"query algoliaSearch($indexName: String!, $query: String, $facetFilters: [String], $page: Int, $per_page: Int) {\n  algoliaSearch(\n    indexName: $indexName\n    query: $query\n    facetFilters: $facetFilters\n    page: $page\n    per_page: $per_page\n  ) {\n    results {\n      id\n      name\n      slug\n      pageType\n      EN {\n        name\n        __typename\n      }\n      EN_AE {\n        name\n        __typename\n      }\n      EN_CA {\n        name\n        __typename\n      }\n      EN_US {\n        name\n        __typename\n      }\n      AR {\n        name\n        __typename\n      }\n      CS {\n        name\n        __typename\n      }\n      DE {\n        name\n        __typename\n      }\n      DE_AT {\n        name\n        __typename\n      }\n      ES {\n        name\n        __typename\n      }\n      FR {\n        name\n        __typename\n      }\n      FR_CA {\n        name\n        __typename\n      }\n      HU {\n        name\n        __typename\n      }\n      IT {\n        name\n        __typename\n      }\n      JA {\n        name\n        __typename\n      }\n      NL {\n        name\n        __typename\n      }\n      PL {\n        name\n        __typename\n      }\n      PT {\n        name\n        __typename\n      }\n      SV {\n        name\n        __typename\n      }\n      ZH_HANT {\n        name\n        __typename\n      }\n      ZH_HANT_TW {\n        name\n        __typename\n      }\n      __typename\n    }\n    facets {\n      name\n      items {\n        name\n        count\n        __typename\n      }\n      __typename\n    }\n    pagination {\n      total\n      per_page\n      current_page\n      last_page\n      next_page\n      prev_page\n      __typename\n    }\n    __typename\n  }\n}"}]'
    ingredients_search_payload = r'[{"operationName":"algoliaSearch","variables":{"indexName":"pages","query":"","facetFilters":["isPublished:true","pageType:ingredient","page_clients:commerce_web","page_channels:us"],"page":%d},"query":"query algoliaSearch($indexName: String!, $query: String, $facetFilters: [String], $page: Int, $per_page: Int) {\n  algoliaSearch(\n    indexName: $indexName\n    query: $query\n    facetFilters: $facetFilters\n    page: $page\n    per_page: $per_page\n  ) {\n    results {\n      id\n      name\n      slug\n      pageType\n      EN {\n        name\n        __typename\n      }\n      \n      EN_US {\n        name\n        __typename\n      }   \n      __typename\n    }\n   pagination {\n      total\n      per_page\n      current_page\n      last_page\n      next_page\n      prev_page\n      __typename\n    }\n    __typename\n  }\n}"}]' % (page_num)
    api_gateway = "https://www.lush.com/api/gateway"
    io_payload = StringIO(ingredients_search_payload)
    response_buffer = BytesIO()
    pycurl_connect = pycurl.Curl()
    
    pycurl_connect.setopt(pycurl.URL, api_gateway)
    pycurl_connect.setopt(pycurl.POST, 1)

    pycurl_connect.setopt(pycurl.READDATA, io_payload)
    pycurl_connect.setopt(pycurl.POSTFIELDSIZE, len(ingredients_search_payload))
    
    pycurl_connect.setopt(pycurl.HTTPHEADER, req_headers)
    
    pycurl_connect.setopt(pycurl.WRITEDATA, response_buffer)

    pycurl_connect.perform()
    pycurl_connect.close()

    response_bytes = response_buffer.getvalue()
    string = response_bytes.decode('iso-8859-1')
    # print(string)
    gunzipped = gzip.decompress(response_bytes)
    gunzipped_str = gunzipped.decode()
    pycurl_connect.close()

    return gunzipped_str

def get_ingredients_and_ids(page_result: str):
    page_obj = json.loads(page_result)
    results = page_obj[0]["data"]["algoliaSearch"]["results"]
    return [{"id": base64.b64decode(res["id"]).decode(), "name": res["name"], "slug":res["slug"]} for res in results]

def generate_ingredients_and_ids(page_result: str):
    page_obj = json.loads(page_result)
    results = page_obj[0]["data"]["algoliaSearch"]["results"]
    return ({"id": base64.b64decode(res["id"]).decode(), "name": res["name"], "slug":res["slug"]} for res in results)

def get_pagination(page_result: str):
    page_obj = json.loads(page_result)
    results = page_obj[0]["data"]["algoliaSearch"]["pagination"]
    return results

def generate_all_ingredients():
    # Prime generator with first page results
    page_result = get_ingredients_page(1)
    pagination_info = get_pagination(page_result)
    last_page = pagination_info["last_page"]

    for page_num in range(1, last_page):
        internal_results = get_ingredients_page(page_num)
        for item in generate_ingredients_and_ids(internal_results):
            yield item
            

def main():
    con = sqlite3.connect("lush_db.db")
    cur = con.cursor()
    for x in generate_all_ingredients():
        slug = x["slug"]
        name = x["name"]
        id = int(x["id"].replace("Page:", ""))
        print(x)
        cur.execute("INSERT INTO INGREDIENTS VALUES(?, ?, ?)", (id, name, slug))
    con.commit()
    con.close()


if __name__ == "__main__":
    main()