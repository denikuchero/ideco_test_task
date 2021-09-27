import sqlite3


def create_db():
    conn = sqlite3.connect('db_test.db')
    command = '''CREATE TABLE status_app (
                                    id INTEGER PRIMARY KEY,
                                    status  INTEGER DEFAULT NULL
                                   );'''
    cursor = conn.cursor()
    cursor.execute(command)
    conn.commit()
    cursor.close()


def write_db():
    conn = sqlite3.connect('db_test.db')
    command = '''INSERT INTO status_app (
                                    status
                                   ) VALUES (0) ;'''
    cursor = conn.cursor()
    cursor.execute(command)
    conn.commit()
    cursor.close()

write_db()
# create_db()