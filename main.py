import requests

with open('curl.txt', 'r') as curl_file:
    curl_string = curl_file.read().strip()

def main(curl_string):
    # Parse url and params
    _, url, leftover = curl_string.split("'", 2)
    url_base, params_string = url.split('?', 1)

    # remove params_string protections
    params_string = params_string.replace("%7B", "{")
    params_string = params_string.replace("%7D", "}")
    params_string = params_string.replace("%22", '"')
    params_string = params_string.replace("%2F", '/')

    params = []
    for item in params_string.split('&'):
        params.append(tuple(item.split('=')))
    params = tuple(params)

    #accept should be changed
    headers_list = leftover.split("-H '")
    del headers_list[0]
    headers = {}
    for item in headers_list:
        item = item.split("'")[0]
        item = item.split(": ")
        if item[0] == "Cookie":
            cookie_string = item[1]
            continue
        headers.update({item[0]: item[1]})

    cookies = {}
    for item in cookie_string.split("; "):
        item = item.split("=")
        cookies.update({item[0]: item[1]})

    response = requests.get(url_base, headers=headers, params=params, cookies=cookies)
    print(response.json())
    return url_base, headers, params, cookies


if __name__ == "__main__":
    main(curl_string)
