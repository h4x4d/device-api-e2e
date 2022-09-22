from requests import Response


def write_log(response: Response):
    log = f"REQUEST:\n" \
          f"url: {response.request.url}\n" \
          f"data: {response.request.body}\n" \
          f"headers: {response.request.headers}\n\n" \
          f"RESPONSE:\n" \
          f"status_code: {response.status_code}\n" \
          f"data: {response.text}\n" \
          f"headers: {response.headers}"

    return log
