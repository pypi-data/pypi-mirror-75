class StawalletException(Exception):
    def __init__(self, logger, message):
        """
        :param message: error message
        """
        self.message = message
        logger.error(f"Stawallet REST Error: {message}")


class StawalletHttpException(StawalletException):
    def __init__(self, logger, http_status_code: int, error: map):
        super(StawalletHttpException, self).__init__(f"http exception code {http_status_code} because of: {str(error)}")
        self.http_status_code = http_status_code


class StawalletUnknownException(StawalletException):
    def __init__(self, logger, message=""):
        super(StawalletUnknownException, self).__init__(f"unknown exception: {message}")
