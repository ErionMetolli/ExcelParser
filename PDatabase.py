import psycopg2

class PDatabase():
    
    connected = False

    def __init__(self, dbname, user, host, password):
        try:
                connProperties = "dbname='" + dbname + "' user='" + user + "' host='" + host + "' password='" + password + "'"
                print(connProperties)
                self.conn = psycopg2.connect(connProperties)
                # Commit everything as soon as the cursor executes a query
                self.conn.autocommit = True
                self.cur = self.conn.cursor()
                print("[PDatabase] Connected successfully.")
                self.connected = True
        except:
                print("[PDatabase] Unable to connect to database!")
                self.connected = False
			
	
    # insert query
    def insert(self, query):
        self.cur.execute(query)
        self.getQuery = query

    # delete query	
    def delete(self, query):
        self.cur.execute(query)
        self.getQuery = query

    # select query
    def select(self, query):
        self.cur.execute(query)
        self.rows = self.cur.fetchall()
        self.getQuery = query

    def getLastQuery(self):
        return self.getQuery
