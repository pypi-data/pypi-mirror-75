from magicdb.Models import DateModel
from datetime import datetime
from typing import Any
from pydantic import BaseModel
from fastapi import Request as FastAPIRequest
from fastapi import Response as FastApiResponse
import json
from typing import Optional

from magicapi.Utils.random_utils import random_str

from magicapi.Decorators.background_tasks import run_in_background
from magicapi.Decorators.parse_objects import parse_objects

# from magicapi import settings
from magicapi import g


class Error(BaseModel):
    error_class: str
    error_dict: Any


class Response(BaseModel):
    body: Any
    headers: dict
    status_code: int


class Request(BaseModel):
    request_id: str
    body: Any
    headers: dict
    cookies: dict
    url: str
    url_path: str
    root_url: str
    query_params: dict
    ip_address: str
    method: str
    scheme: str
    port: Optional[int]
    # added from aws context
    aws_request_id: str = None
    log_group_name: str = None
    log_stream_name: str = None
    function_name: str = None
    memory_limit_in_mb: str = None
    # added from aws event
    request_id: str = None
    domain_name: str = None
    api_id: str = None
    # created_urls
    log_group_url: str = None
    stream_url: str = None


class Times(BaseModel):
    time_received: datetime
    time_done: datetime
    secs_took: float


class Call(DateModel):
    request: Request
    response: Response = None
    error: Error = None
    times: Times

    class Meta:
        collection_name = "_calls"


@run_in_background
@parse_objects
def save_call(call: Call):
    call.save()


async def get_request_body(request: FastAPIRequest):
    # first try json, then body, then form...
    errors = []
    try:
        result = await request.json() or None
        return result
    except Exception as json_error:
        errors.append(f"json_error {json_error}")

    try:
        result = await request.form() or None
        return dict(result)
    except Exception as form_error:
        errors.append(f"form_error {form_error}")

    try:
        result = await request.body() or None
        return result
    except Exception as body_error:
        errors.append(f"body_error {body_error}")

    if g.settings.print_level > 1:
        print("get_request_body_errors", errors)

    return None


def make_body_jsonable(body):
    try:
        json.dumps(body)
        return body
    except TypeError as _:
        pass

    # now try making string
    try:
        body_str = str(body)
        return body_str
    except TypeError as _:
        pass

    return None


def safe_loads(body):
    if body is None:
        return body
    try:
        return json.loads(body)
    except TypeError as _:
        pass

    try:
        return str(body)
    except TypeError as _:
        pass

    return None


async def make_request_obj_from_request(request: FastAPIRequest):
    body = await get_request_body(request)
    jsonable_body = make_body_jsonable(body)

    request_obj = Request(
        request_id=random_str(30),
        body=jsonable_body,
        headers=dict(request.headers),
        cookies=dict(request.cookies),
        url=str(request.url),
        url_path=request.url.path,
        root_url=str(request.url).replace(request.url.path, ""),
        query_params=dict(request.query_params),
        ip_address=request.client.host,
        method=request.method,
        scheme=request.url.scheme,
        port=request.url.port,
    )

    aws_fields = ['aws_request_id', 'log_group_name', 'log_stream_name', 'function_name', 'memory_limit_in_mb']

    if 'aws.context' in request.scope:
        context = request.scope['aws.context']
        [setattr(request_obj, field, getattr(context, field)) for field in aws_fields]

        cloudwatch_base_url = 'https://console.aws.amazon.com/cloudwatch/home?region=us-east-1#logStream:group='
        request_obj.log_group_url = f'{cloudwatch_base_url}{request_obj.log_group_name}'
        request_obj.stream_url = f'{request_obj.log_group_url};stream={request_obj.log_stream_name}'.replace(
            '[$LATEST]', '%5B$LATEST%5D').replace('logStream', 'logEventViewer')

    if 'aws.event' in request.scope:
        event = request.scope['aws.event']
        request_context = event.get('requestContext')
        if request_context:
            request_obj.request_id = request_context.get('requestId')
            request_obj.domain_name = request_context.get('domainName')
            request_obj.api_id = request_context.get('apiId')

    return request_obj


async def make_call_from_request_and_response(
        request: FastAPIRequest,
        response: Optional[FastApiResponse],
        error: Optional[Exception],
        times_dict: dict,
):
    if not g.settings.save_calls:
        return

    request_obj = await make_request_obj_from_request(request)

    response_obj = (
        None
        if not response
        else Response(
            body=safe_loads(response.body),
            headers=dict(response.headers),
            status_code=response.status_code,
        )
    )

    error_obj = (
        None
        if not error
        else Error(
            error_class=str(error.__class__),
            error_dict=make_body_jsonable(error.__dict__),
        )
    )

    # maybe wrap this whole thing w a try catch just in case so it does not fuck up everything else
    # will do this once I test this out for a while... prob

    call = Call(
        request=request_obj,
        response=response_obj,
        error=error_obj,
        times=Times(**times_dict),
    )

    save_call(call)
