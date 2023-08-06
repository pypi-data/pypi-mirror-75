"""async_get_web
"""

from pydantic import BaseModel, HttpUrl
from pathlib import PurePath

########################################
# validators
########################################

_WEB_EXTENSIONS = ("htm", "php", "asp")


class URLValidator(BaseModel):
    url: HttpUrl

    def is_file(self):
        if not self.url.path:
            return False
        path = PurePath(self.url.path)
        ext = path.suffix[1:]
        if not ext:
            return False
        return not ext.lower().startswith(_WEB_EXTENSIONS)
