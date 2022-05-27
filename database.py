import sqlite3
from datetime import datetime


class DatabaseHandler:
    connection = sqlite3.connect('./HttpProxyBlocker.db', check_same_thread=False)
    cursor = connection.cursor()

    def __init__(self):
        self.create_tables()
        self.insert_data_to_tables_for_start()

    def create_tables(self):
        # make database and users (if not exists already) table at programe start up

        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS block_list (
        ID INTEGER PRIMARY KEY AUTOINCREMENT,
        created_at DATE ,
        web_address TEXT NOT NULL ,
        status INTEGER default 1
        )
''')

        self.connection.commit()

    def insert_data_to_tables_for_start(self):
        result = self.check_data_exist('block_list')
        if not result:
            block_list_insert = 'INSERT INTO block_list(created_at, web_address) VALUES(?,?)'
            web_list = [(datetime.now(), 'httpvshttps')]
            self.cursor.executemany(block_list_insert, web_list)

        self.connection.commit()

    def check_data_exist(self, table_name):
        query = (f'SELECT * FROM {table_name}')
        self.cursor.execute(query)
        result = self.cursor.fetchall()
        if result:
            return True
        else:
            return False

    def exist_web_address(self, web_address):
        find_web_address = ('SELECT * FROM block_list WHERE web_address = ?')
        self.cursor.execute(find_web_address, (web_address,))
        result = self.cursor.fetchall()
        if result:
            return True
        else:
            return False

    def add_web_to_db(self, web_address):
        insert = 'INSERT INTO block_list(created_at, web_address) VALUES(?,?);'
        self.cursor.execute(insert, [datetime.now(), web_address])
        self.connection.commit()

    def delete_web_from_db(self, selected_item):
        delete = """UPDATE block_list set status = 0 WHERE ID = ?;"""
        self.cursor.execute(delete, (selected_item[2], ))
        self.connection.commit()

    def get_all_web_sites(self):
        all_web_sites = ('SELECT * FROM block_list where status = 1')
        self.cursor.execute(all_web_sites)
        result = self.cursor.fetchall()
        if result:
            return result
        else:
            return False

    def get_all_name_web_sites(self):
        all_web_sites = ('SELECT web_address FROM block_list where status = 1')
        self.cursor.execute(all_web_sites)
        result = self.cursor.fetchall()
        if result:
            return result
        else:
            return False


    def update_web_sites(self, selected_item, web_site):
        update = """UPDATE block_list set web_address = ? WHERE ID = ?;"""
        self.cursor.execute(update, (web_site, selected_item[2]))
        self.connection.commit()


db = DatabaseHandler()