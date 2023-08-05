import selectors
import ssl
import xmlrpc.client


class CookiesTransport(xmlrpc.client.Transport):
    """Retains cookies over its lifetime."""

    # Note context option - it's required for success
    def __init__(self):
        super().__init__()
        self._cookies = []

    def send_headers(self, connection, headers):
        if self._cookies:
            connection.putheader("Cookie", "; ".join(self._cookies))
        super().send_headers(connection, headers)

    def parse_response(self, response):
        # This check is required if in some responses we receive no cookies at all
        if response.msg.get_all("Set-Cookie"):
            for header in response.msg.get_all("Set-Cookie"):
                cookie = header.split(";", 1)[0]
                self._cookies.append(cookie)
        return super().parse_response(response)


class PubClient:
    def __init__(self, endpoint_url, username, password):
        self.endpoint_url = endpoint_url
        self.username = username
        self.password = password
        self.transport = CookiesTransport()

        self.proxy = xmlrpc.client.ServerProxy(
            self.endpoint_url, transport=self.transport
        )

    def login(self):
        return self.proxy.auth.login_password(self.username, self.password)

    def list_targets(self):
        return self.proxy.client.list_targets()
