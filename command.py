class Command:
    def __init__(self) -> None:
        pass

    def run(self, text: str):
        print("Running " + text + " command")


class OpenFile(Command):
    
    def run(self):
        super().run("OpenFile")

