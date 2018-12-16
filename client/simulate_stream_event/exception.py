class MyException(Exception):
    def __init__(self, message):
        super().__init__(self)
        self.message = message

    def get_message(self):
        print(self.message)


class ConnectionException(MyException):
    def __init__(self):
        mess = 'ConnectionError: The server is not available, please try it later!'
        super().__init__(mess)


class ServerRequestException(MyException):
    def __init__(self, text):
        mess = 'ServerRequestError: Server Error! ' + text
        super().__init__(mess)


class ReadFileException (MyException):
    def __init__(self, path):
        mess = "ReadFileError: The input path '" + path + "' does not exist or is empty!"
        super().__init__(mess)
