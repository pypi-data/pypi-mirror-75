import tkinter as tk
from .EventBase import EventBase
from .StyleBase import StyleBase

class Button(tk.Button, EventBase, StyleBase):
    @property
    def label(self):
        return self["text"]

    @label.setter
    def label(self, value):
        self["text"] = value