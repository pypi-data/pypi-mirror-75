

class PyUnitObject:
    def __init__(self, pyukey):
        self.key = pyukey

    def get_return_object_name(self):
        if isinstance(self.key, str):
            return str(self.key).split(".")[1]
        return self.key
