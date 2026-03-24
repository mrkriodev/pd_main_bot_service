class MainBackendError(Exception):
    """Failures when talking to the main pumpdump backend API."""


class MainBackendConfigError(MainBackendError):
    """Missing or invalid configuration (e.g. admin token)."""


class MainBackendHttpSessionError(MainBackendError):
    """aiohttp client is missing or closed."""


class MainBackendRegistrationError(MainBackendError):
    def __init__(
        self,
        message: str,
        *,
        status: int | None = None,
        body: str | None = None,
    ) -> None:
        super().__init__(message)
        self.status = status
        self.body = body
