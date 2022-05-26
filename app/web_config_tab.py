import tkinter as tk
from tkinter import ttk
from tkinter import *

from tkinter import messagebox as ms

from database import db


class WebConfigTab:

    def __init__(self, tab_parent):
        self.web_address = tk.StringVar()

        self.tab = ttk.Frame(tab_parent)
        tab_parent.add(self.tab, text="Web Config")

        self.style = ttk.Style()
        self.style.theme_use('clam')

        # Add a Treeview widget
        self.tree = ttk.Treeview(self.tab, column=("c1", "c2"), show='headings', height=15)
        self.tree.column("# 1", anchor=CENTER)
        self.tree.heading("# 1", text="ID")
        self.tree.column("# 2", anchor=CENTER)
        self.tree.heading("# 2", text="Web Address")

        # Insert the data in Treeview widget
        self.get_all_web_sites()

        self.tree.pack()

        self.refresh_btn = ttk.Button(self.tab, text="REFRESH", command=self.refresh_tree)
        self.refresh_btn.pack()
        self.del_btn = ttk.Button(self.tab, text="Delete", command=self.delete)
        self.del_btn.pack()
        self.edit_btn = ttk.Button(self.tab, text="Edit", command=self.edit)
        self.edit_btn.pack()
        self.buttonCommit = ttk.Button(self.tab, text="Add", command=self.add_web_to_db)
        self.buttonCommit.pack()

        self.web_address_label = tk.Label(self.tab, text="Insert Web Address")
        self.web_address_entry = tk.Entry(self.tab, textvariable=self.web_address)
        self.web_address_entry.pack()
        self.web_address_label.pack()

    def refresh_tree(self):
        self.delete_all_items_in_tree()
        self.get_all_web_sites()

    def get_all_web_sites(self):
        all_web_sites = db.get_all_web_sites()
        for index, item in enumerate(all_web_sites, start=1):
            self.tree.insert('', 'end', text=str(index), values=(f'{index}', f'{item[2]}', f'{item[0]}'))

    def delete_all_items_in_tree(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

    def edit(self):
        # Get selected item to Edit
        web_address = self.web_address.get()
        curItem = self.tree.focus()
        selected_item = self.tree.item(curItem)
        if not selected_item['values']:
            ms.showerror('Error!', 'Plz select from table and press the button !!!')
        else:
            db.update_web_sites(selected_item['values'], web_address)
            ms.showinfo('Success!', 'Your Web Address is Edited!')
            self.web_address.set('')
            self.delete_all_items_in_tree()
            self.get_all_web_sites()

    def delete(self):
        # Get selected item to Delete
        curItem = self.tree.focus()
        selected_item = self.tree.item(curItem)
        if not selected_item['values']:
            ms.showerror('Error!', 'Plz select from table and press the button !!!')
        else:
            db.delete_web_from_db(selected_item['values'])
            ms.showinfo('Success!', 'Your Web Address is Deleted!')
            self.delete_all_items_in_tree()
            self.get_all_web_sites()

    def add_web_to_db(self):
        web_address = self.web_address.get()
        if not web_address:
            ms.showerror('Error!', 'Input your web address !!!')
        else:

            is_exist = db.exist_web_address(web_address)
            if is_exist:
                ms.showerror('Error!', 'Your Web Address Does Exist !!!')
            else:
                db.add_web_to_db(web_address)
                ms.showinfo('Success!', 'Your Web Address is Added To DataBase!')
                self.delete_all_items_in_tree()
                self.get_all_web_sites()

        self.web_address.set('')
