from fastapi import Request


def get_endpoint_from_request(request: Request) -> str:
    return str(request.url).replace(str(request.base_url), "")
