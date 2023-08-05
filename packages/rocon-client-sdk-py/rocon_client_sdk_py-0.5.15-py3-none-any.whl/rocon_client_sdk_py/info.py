from rocon_client_sdk_py.__init__ import __name__ as NAME
from rocon_client_sdk_py.__init__ import __description__ as DESCRIPTION
from rocon_client_sdk_py.__init__ import __version__ as VERSION
from rocon_client_sdk_py.__init__ import __author__ as AUTHOR
from rocon_client_sdk_py.__init__ import __author_email__ as AUTHOR_EMAIL
from rocon_client_sdk_py.__init__ import __repository_url__ as REPOSITORY_URL
from rocon_client_sdk_py.__init__ import __download_url__ as DOWNLOAD_URL
from rocon_client_sdk_py.__init__ import __license__ as LICENSE

class Info():

    @property
    def name(self):
        return NAME

    @property
    def description(self):
        return DESCRIPTION

    @property
    def version(self):
        return VERSION

    @property
    def author(self):
        return AUTHOR

    @property
    def author_email(self):
        return AUTHOR_EMAIL

    @property
    def repository_url(self):
        return REPOSITORY_URL

    @property
    def download_url(self):
        return DOWNLOAD_URL

    @property
    def license(self):
        return LICENSE


info = Info()

