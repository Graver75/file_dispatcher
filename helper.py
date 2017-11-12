from uuid import uuid4


class Helper:
    @staticmethod
    def generate_node_id():
        return str(uuid4())