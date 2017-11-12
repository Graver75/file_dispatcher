from uuid import uuid4


class Helper:
    @staticmethod
    def generate_nodeid():
        return str(uuid4())