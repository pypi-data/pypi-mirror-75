import tkinter as tk
from .EventBase import EventBase
from .StyleBase import StyleBase

class Image(tk.Label, EventBase, StyleBase):
    pass