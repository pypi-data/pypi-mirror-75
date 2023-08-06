"""async_get_web.py

todo
"""
__all__ = ["get_webpages", "get_urls"]

from typing import Iterable, List, Optional

from pydantic import BaseModel, HttpUrl, ValidationError
from requests import Response
from requests_html import AsyncHTMLSession as Session

from .validators import URLValidator
from .exceptions import *

_FILTER_EXTENSIONS_DEFAULT_VALUE = True


########################################
# get web pages
########################################
class WebpageResponse(BaseModel):
    link: str
    response: Optional[Response] = None
    error: Optional[Exception] = None

    @property
    def url(self):
        return self.response.url

    @property
    def title(self):
        return self.response.html.find("title", first=True).text

    class Config:
        arbitrary_types_allowed = True


def _make_get_webpage_async_function(
    async_session: Session, url: str, filter_extensions: bool
):
    async def get_async_url():
        try:
            valid_url = URLValidator(url=url)
        except ValidationError as e:
            return WebpageResponse(url=url, error=e)

        if filter_extensions and valid_url.is_file():
            return WebpageResponse(link=url, error=FileURL(url))

        try:
            response = await async_session.get(url)
        except Exception as e:
            return WebpageResponse(link=url, error=e)

        if response.status_code >= 400:
            return WebpageResponse(
                link=url, response=response, error=BadResponse(response.status_code)
            )

        content_type = response.headers.get("Content-Type")
        if "html" not in content_type:
            return WebpageResponse(
                link=url, response=response, error=BadContentType(content_type)
            )

        return WebpageResponse(link=url, response=response)

    return get_async_url


def get_webpages(
    urls: Iterable[str],
    *,
    async_session: Session = None,
    filter_extensions: bool = _FILTER_EXTENSIONS_DEFAULT_VALUE
) -> List[WebpageResponse]:
    session = async_session or Session()
    async_functions = [
        _make_get_webpage_async_function(session, url, filter_extensions)
        for url in urls
    ]
    webpages = session.run(*async_functions)
    return webpages


########################################
# get urls
########################################
def _make_get_url_async_function(async_session: Session, url: str):
    async def get_async_url():
        try:
            response = await async_session.get(url)
        except Exception:
            return None
        return response

    return get_async_url


def get_urls(urls: List[str], async_session: Session = None) -> List:
    session = async_session or Session()
    async_functions = [_make_get_url_async_function(session, url) for url in urls]
    responses = session.run(*async_functions)
    return responses
