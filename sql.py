import sqlite3


class SQLiter:
    def __init__(self, database):
        self.connection = sqlite3.connect(database)
        self.cursor = self.connection.cursor()

    def insert(self, lat, ru):
        with self.connection:
            return self.cursor.execute('INSERT INTO twords(lat_word, ru_word) VALUES (?, ?)', (lat, ru))

    def select_all(self):
        with self.connection:
            return self.cursor.execute('SELECT * FROM twords').fetchall()

    def select_single(self, rownum):
        with self.connection:
            return self.cursor.execute('SELECT * FROM twords WHERE id = ?', (rownum,)).fetchall()[0]

    def count_rows(self):
        with self.connection:
            result = self.cursor.execute('SELECT * FROM twords').fetchall()
            return len(result)

    def clr(self):
        return self.cursor.execute('DELETE FROM twords')

    def close(self):
        self.connection.commit()
        self.connection.close()
