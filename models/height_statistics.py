
class HeightStatistics:

    def __init__(self, database):
        self.conn = database
        self.table = 'height_statistics'

    def create_table(self):
        try:
            self.conn.execute('CREATE TABLE IF NOT EXISTS %s (id INT, server VARCHAR(120), height INT, timestamp INT)' % self.table)
        except Exception as e:
            print(e)
            self.conn.rollback()

        self.conn.commit()

    def get_last_id(self):
        try:
            cur = self.conn.execute('SELECT max(id) FROM %s' % self.table)
            row = cur.fetchone()
        except Exception as e:
            print(e)
            self.conn.rollback()

            return -1

        self.conn.commit()

        return int(row[0])

    def insert_or_update_height(self, iid, server, height, timestamp):
        try:
            self.conn.execute('INSERT INTO %s (id, server, height, timestamp) VALUES (?, ?, ?, ?)' % self.table, (iid, server, height, int(timestamp)))
        except Exception as e:
            print(e)
            self.conn.rollback()

        self.conn.commit()


if __name__ == '__main__':
    import os
    import sys

    sys.path.pop(sys.path.index(os.path.dirname(os.path.realpath(__file__))))
    sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

    import sqlite3
    from settings.database import db_name

    db_conn = sqlite3.connect(db_name)
    db_conn.set_trace_callback(print)

    hs = HeightStatistics(db_conn)

    hs.create_table()
