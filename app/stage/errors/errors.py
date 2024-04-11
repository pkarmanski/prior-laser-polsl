class StageConnectionError(Exception):
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return self.msg


class StageOpenSessionError(Exception):
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return self.msg


class StageCloseSessionError(Exception):
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return self.msg


class StageExecuteError(Exception):
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return self.msg
