import os
import requests

from fastapi import Body, Header, Request, Response, status
from typing import Any, Annotated

from authgw.validator import validate_request


def generate_routes(app):

    @app.post(os.environ.get("API_PREFIX", "") + "/getRefreshToken")
    def generate_refresh_token(request: Request, response: Response, authorization: Annotated[str | None, Header()] = None):
        additional_details = {
            "method": request.method,
            "url": str(request.url),
            "headers": repr(request.headers),
            "queryParams": repr(request.query_params),
            "pathParams": repr(request.path_params),
            "clientDetails": repr(request.client)
        }
        validation, status, msg = validate_request._validate_token_request(auth=authorization)
        response.status_code = status
        return msg
        
    @app.get(os.environ.get("API_PREFIX", "") + "/{route_path:path}")
    @validate_request.validate
    def route_get(route_path: str, request: Request, response: Response, authorization: Annotated[str | None, Header()] = None, payload: Any = Body(None)):
        additional_details = {
            "method": request.method,
            "url": str(request.url),
            "headers": repr(request.headers),
            "queryParams": repr(request.query_params),
            "pathParams": repr(request.path_params),
            "clientDetails": repr(request.client)
        }
        r = requests.get("{}/{}/{}".format(os.environ.get("PROXY_URL"), os.environ.get("PROXY_PREFIX"), route_path), headers=dict(request.headers), params=request.query_params, json=payload)
        response.status_code = r.status_code
        try:
            return r.json()
        except:
            return r.text


    @app.post(os.environ.get("API_PREFIX", "") + "/{route_path:path}")
    @validate_request.validate
    def route_post(route_path: str, request: Request, response: Response, authorization: Annotated[str | None, Header()] = None, payload: Any = Body(None)):
        additional_details = {
            "method": request.method,
            "url": str(request.url),
            "headers": repr(request.headers),
            "queryParams": repr(request.query_params),
            "pathParams": repr(request.path_params),
            "clientDetails": repr(request.client)
        }
        r = requests.post("{}/{}/{}".format(os.environ.get("PROXY_URL"), os.environ.get("PROXY_PREFIX"), route_path), headers=dict(request.headers), params=request.query_params, json=payload)
        response.status_code = r.status_code
        try:
            return r.json()
        except:
            return r.text


    @app.put(os.environ.get("API_PREFIX", "") + "/{route_path:path}")
    @validate_request.validate
    def route_put(route_path: str, request: Request, response: Response, authorization: Annotated[str | None, Header()] = None, payload: Any = Body(None)):
        additional_details = {
            "method": request.method,
            "url": str(request.url),
            "headers": repr(request.headers),
            "queryParams": repr(request.query_params),
            "pathParams": repr(request.path_params),
            "clientDetails": repr(request.client)
        }
        r = requests.put("{}/{}/{}".format(os.environ.get("PROXY_URL"), os.environ.get("PROXY_PREFIX"), route_path), headers=dict(request.headers), params=request.query_params, json=payload)
        response.status_code = r.status_code
        try:
            return r.json()
        except:
            return r.text
    
    @app.delete(os.environ.get("API_PREFIX", "") + "/{route_path:path}")
    @validate_request.validate
    def route_delete(route_path: str, request: Request, response: Response, authorization: Annotated[str | None, Header()] = None, payload: Any = Body(None)):
        additional_details = {
            "method": request.method,
            "url": str(request.url),
            "headers": repr(request.headers),
            "queryParams": repr(request.query_params),
            "pathParams": repr(request.path_params),
            "clientDetails": repr(request.client)
        }
        r = requests.delete("{}/{}/{}".format(os.environ.get("PROXY_URL"), os.environ.get("PROXY_PREFIX"), route_path), headers=dict(request.headers), params=request.query_params, json=payload)
        response.status_code = r.status_code
        try:
            return r.json()
        except:
            return r.text

