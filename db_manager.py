import sqlite3


def init_database(self):
    self.conn = sqlite3.connect('computers.db')
    self.cursor = self.conn.cursor()
    self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS statuses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE
        )
    ''')
    self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS computers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            ip_address TEXT,
            mac_address TEXT,
            cpu TEXT,
            ram TEXT,
            os TEXT,
            notes TEXT,
            status_id INTEGER REFERENCES statuses(id)
        )
    ''')
    self.cursor.execute("SELECT COUNT(*) FROM statuses")
    if self.cursor.fetchone()[0] == 0:
        default_statuses = [('В работе',), ('На ремонте',), ('Списан',), ('Резерв',)]
        self.cursor.executemany("INSERT INTO statuses (name) VALUES (?)", default_statuses)
    self.conn.commit()


def get_all_statuses(self):
    self.cursor.execute("SELECT id, name FROM statuses ORDER BY id")
    return self.cursor.fetchall()


def add_computer_db(self, computer_data):
    status_id = computer_data.get('status_id', 1) if 'status_id' in computer_data else 1
    self.cursor.execute('''
        INSERT INTO computers (name, ip_address, mac_address, cpu, ram, os, notes, status_id)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', (computer_data['name'], computer_data['ip_address'], computer_data['mac_address'],
          computer_data['cpu'], computer_data['ram'], computer_data['os'],
          computer_data['notes'], status_id))
    self.conn.commit()


def edit_computer_db(self, computer_data, computer_id):
    status_id = computer_data.get('status_id', 1) if 'status_id' in computer_data else 1
    self.cursor.execute('''
        UPDATE computers 
        SET name=?, ip_address=?, mac_address=?, cpu=?, ram=?, os=?, notes=?, status_id=?
        WHERE id=?
    ''', (computer_data['name'], computer_data['ip_address'], computer_data['mac_address'],
          computer_data['cpu'], computer_data['ram'], computer_data['os'], computer_data['notes'],
          status_id, computer_id))
    self.conn.commit()


def delete_computer_db(self, computer_id):
    self.cursor.execute("DELETE FROM computers WHERE id=?", (computer_id,))
    self.conn.commit()


def select_all_computers_db(self):
    self.cursor.execute("""
        SELECT c.id, c.name, c.ip_address, c.mac_address, c.cpu, c.ram, c.os, c.notes, s.name
        FROM computers c
        LEFT JOIN statuses s ON c.status_id = s.id
    """)
    return self.cursor.fetchall()


def get_statistics_db(self):
    self.cursor.execute("SELECT COUNT(*) FROM computers")
    total_count = self.cursor.fetchone()[0]
    self.cursor.execute("""
        SELECT s.name, COUNT(c.id)
        FROM statuses s
        LEFT JOIN computers c ON s.id = c.status_id
        GROUP BY s.id, s.name
        ORDER BY s.id
    """)
    status_counts = self.cursor.fetchall()
    return total_count, status_counts
