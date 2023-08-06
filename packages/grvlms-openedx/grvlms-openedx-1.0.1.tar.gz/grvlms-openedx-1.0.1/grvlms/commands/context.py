# pylint: disable=too-few-public-methods
class Context:
    def __init__(self, root, user, remote_config):
        self.root = root
        self.user = user
        self.remote_config = remote_config
