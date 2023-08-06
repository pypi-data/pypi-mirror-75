class InsertError(Exception):
    def __init__(self, msg, original_exception):
        super(InsertError, self).__init__("{} : {}".format(msg, original_exception))
        self.original_exception = original_exception


class GetError(Exception):
    def __init__(self, msg, original_exception):
        super(GetError, self).__init__("{} : {}".format(msg, original_exception))
        self.original_exception = original_exception


class RemoveError(Exception):
    def __init__(self, msg, original_exception):
        super(RemoveError, self).__init__("{} : {}".format(msg, original_exception))
        self.original_exception = original_exception


class UpdateError(Exception):
    def __init__(self, msg, original_exception):
        super(UpdateError, self).__init__("{} : {}".format(msg, original_exception))
        self.original_exception = original_exception


class HeartbeatError(Exception):
    def __init__(self, msg, original_exception):
        super(HeartbeatError, self).__init__("{} : {}".format(msg, original_exception))
        self.original_exception = original_exception
