import sys
import socketserver
import threading
import tkinter as tk
from tkinter import ttk
from tkinter import *
from app.http_proxy import MyProxy


class ProxyTab:

    def __init__(self, tab_parent, form):
        self.web_address = tk.StringVar()
        self.proxy_status = 0
        self.tab = ttk.Frame(tab_parent)
        self.form = form
        tab_parent.add(self.tab, text="Proxy Tab")

        message = '''
To start:


Go to Config tab and add website or edit or delete 

Then Click On Start Button
'''
        self.text_box = Text(self.tab)
        self.text_box.insert('end', message)
        self.text_box.config(state='disabled')
        self.text_box.pack()

        Button(self.tab, text='Start Proxy Blocking System', command=self.start_proxy, bg='green').pack()
        Button(self.tab, text='Close Proxy Blocking System', command=self.stop_proxy, bg='red').pack()

        self.status_text_box = Text(self.tab, height=1)
        self.status_text_box.pack()
        self.status_text_box.insert(tk.END, 'Proxy System Status: Deactivate')
        self.status_text_box.config(state='disabled')

        #On Linux: socketserver.ForkingTCPServer  On windows: socketserver.ThreadingTCPServer

        self.proxy_obj = socketserver.ThreadingTCPServer(('', 8000), MyProxy)
        self.my_thread = threading.Thread(target=self.proxy_obj.serve_forever, name='proxy')

    # Close  Proxy System: close server and close window
    def stop_proxy(self):
        self.form.destroy()
        self.proxy_obj.server_close()
        self.proxy_obj.shutdown()
        sys.exit(0)

    # Start Proxy System: using a new thread
    def start_proxy(self):
        self.status_text_box.pack_forget()
        self.status_text_box = Text(self.tab, height=1, bg='yellow')
        self.status_text_box.pack()
        self.status_text_box.insert(tk.END, 'Proxy System Status: Activate')
        self.status_text_box.config(state='disabled')

        self.my_thread.start()
