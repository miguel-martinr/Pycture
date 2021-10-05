from abc import abstractclassmethod, ABC
import tkinter as tk


class Cmd:
    def run(cmd_name: str):
        print("Running " + cmd_name + " command")


class OpenImage(Cmd):
    def run():
        super.run("OpenImage")


class CmdBtn:
    def __init__(self, text: str, master: tk.Frame, cmd: Cmd) -> None:
        self.cmd = cmd  # Temp
        self.text = text
        self.setButton(master)

    def setButton(self, master: tk.Frame):
        self.btn = tk.Button(master=master, text=self.text, width=10, command=lambda foo: self.cmd.run())


class ControlBar(tk.Frame):
    def __init__(self, main_window: tk.Tk) -> None:
        super().__init__(main_window)
        self.setUI(main_window)

    def setUI(self, main_window: tk.Tk):
        main_window.rowconfigure(0, weight=1)
        commands = [CmdBtn("Open", master=self, cmd=OpenImage())]
        for i, cmd in enumerate(commands):
          main_window.columnconfigure(i, weight=5)
          cmd.btn.grid(row=0, column=i)
        self.grid(sticky="nsew")

