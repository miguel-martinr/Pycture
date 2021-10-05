class Command:
    def __init__(self) -> None:
        pass

    def run(self):
        pass


class OpenFile(Command):
    def run(self):
        print("Opens File and loads it in editor")
