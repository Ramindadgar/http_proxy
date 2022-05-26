import tkinter as tk
from tkinter import ttk

from app.proxy_tab import ProxyTab
from app.web_config_tab import WebConfigTab


if __name__ == '__main__':
    form = tk.Tk()
    form.title("Welcome to Proxy Blocker app!")
    form.geometry("1150x900")
    tab_parent = ttk.Notebook(form)
    tab_parent.pack(expand=1, fill='both')

    start_proxy = ProxyTab(tab_parent, form)
    web_config_tab = WebConfigTab(tab_parent)

    form.mainloop()
