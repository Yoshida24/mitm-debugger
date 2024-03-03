import re

target_url_regex = "^https://www.example.xyz.*"
replace_src_html = """<div id="app"></div>"""
insert_js = """
    <script>window.alert("intercept!")</script>
"""


def get_request_info(flow):
    request_info = {
        "method": flow.request.method,
        "url": flow.request.url,
        "path": flow.request.path,
        "query_parameters": dict(flow.request.query),
        "headers": dict(flow.request.headers),
        "body": flow.request.text,
    }
    return request_info


def intercept_example(flow):
    from pprint import pprint

    request_info = get_request_info(flow)
    pprint(request_info)

    # 正規表現で判定
    if re.search(target_url_regex, request_info["url"]):
        replaced_html_with_js = replace_src_html + insert_js
        flow.response.text = flow.response.text.replace(
            replace_src_html, replaced_html_with_js
        )


def response(flow):
    intercept_example(flow)
