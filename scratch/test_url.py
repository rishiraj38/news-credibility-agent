import requests

url = "https://news.google.com/read/CBMiowFBVV95cUxQRFc2NmJFRVRQZzI5VUNvRFJnVWdvTjdueWJEakExUHBhZVFfM0M1eU9tanBsZENDZzdDelFTTEdGOWsxRVJkVjFnVmcyc0xmbWFZbm9ESDRDcVBjM0RSR3JrSnhfTXR6aDhsNERQQlBrUVN3QVJpenJrQzZMVkVUSi1jMUN2cFptaWlsOUJFTU5CQVFJcUpOdHQ1cGpmSUVua2hV0gGqAUFVX3lxTFBRRmtaVFUxVG05OUdSR1FlSHBNV0Vrd1NRTlNhY3NtVExuYWs4cW91Tmp4NWNfVGhqSFZWQnlfX0laNndkcFppMnZaQzB1RW5LTm5zYmFHc0xSY2N1VmJtYjRFZnhkU0pRek5aWlVJWXl5c0lEdWQtZlc2M0stSUtTYXN1WHQxY0RhaXNPSXl6ME50M2x5M2UxU245VldZVmtXTWhGMGczRThn?hl=en-IN&gl=IN&ceid=IN%3Aen"

headers = {
    "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Mobile/15E148 Safari/604.1"
}

resp = requests.get(url, headers=headers, allow_redirects=True)
print(f"Status Code: {resp.status_code}")
print(f"Final URL: {resp.url}")
content = resp.text
print(f"Body length: {len(content)}")

# Look for the destination URL in the body
if "base64" in content or "window.location" in content:
    print("Found potential JS redirect")
