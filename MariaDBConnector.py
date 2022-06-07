import mariadb
import sys

# facade around mariaDB connector
class MariaDBConnector:

    def __init__(self):
        try:
            self.conn = mariadb.connect(
                user="python",
                password="1234",
                host="127.0.0.1",
                port=3309,
                database="sensamag_sp"
            )
            self.cursor = self.conn.cursor()
        except mariadb.Error as e:
            print(f"Error connecting to MariaDB Platform: {e}")
            sys.exit(1)
