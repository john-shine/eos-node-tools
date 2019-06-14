import sqlite3


class HealthStatistics:

    def __init__(self, database):
        self.conn = database
        self.table = 'health_statistics'

    def create_table(self):
        try:
            self.conn.execute('CREATE TABLE IF NOT EXISTS %s (server VARCHAR(120), method VARVHAR(60), consumed INT, is_up INT)' % self.table)
        except Exception as e:
            print(e)
            self.conn.rollback()

        self.conn.commit()

    def insert_health(self, server, method, consumed, is_up):
        try:
            self.conn.execute('INSERT INTO %s (server, method, consumed, is_up) VALUES (?, ?, ?, ?)' % self.table, (server, method, consumed, is_up))
        except Exception as e:
            print(e)
            self.conn.rollback()

        self.conn.commit()


if __name__ == '__main__':

    import os
    import sys

    sys.path.pop(sys.path.index(os.path.dirname(os.path.realpath(__file__))))
    sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

    from settings.database import db_name
    db_conn = sqlite3.connect(db_name)
    db_conn.set_trace_callback(print)
    
    hs = HealthStatistics(db_conn)

    hs.create_table()
