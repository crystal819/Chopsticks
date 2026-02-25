import pyodbc

class ChopsticksDB():
    def __init__(self):
        conn_string_sch = (
            'Driver={SQL Server};'
            'Server=svr-cmp-01;'
            'Database=25svynarchT230;'
            'Trusted_Connection=yes;'
        )

        conn_string_home = (
            "Driver={SQL Server};"
            "Server=localhost\\SQLEXPRESS;"
            "Database=chopsticks;"
            "Trusted_Connection=yes;"
            "TrustServerCertificate=yes;"
        )

        try:
            pyodbc.connect(conn_string_sch, timeout=3)
            self.conn_string = conn_string_sch
        except:
            self.conn_string = conn_string_home
        
        return self.conn_string
    
    def _get_connection(self):
        return pyodbc.connect(self.conn_string)