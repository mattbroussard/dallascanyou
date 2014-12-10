
import os
import psycopg2
import urlparse


class DB:
    
    conn = None

    def __init__(self):
        pass

    def __enter__(self):
        urlparse.uses_netloc.append("postgres")
        url = urlparse.urlparse(os.environ.get("DATABASE_URL", ""))
        
        self.conn = psycopg2.connect(
            database=url.path[1:],
            user=url.username,
            password=url.password,
            host=url.hostname,
            port=url.port
        )

        self.setupIfNeeded()

        return self
    
    def setupIfNeeded(self):
        cursor = self.conn.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS posts (id SERIAL NOT NULL PRIMARY KEY, userID VARCHAR(256), timestamp VARCHAR(256), authorName text, content text)")

    def get(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT userID, authorName, timestamp, content FROM posts ORDER BY id DESC LIMIT 50")
        rows = cursor.fetchall()
        print rows
        print len(rows)
        def rowToDict(row):
            return {k:v for k,v in zip(row, ("userID", "authorName", "timestamp", "content"))}
        return [rowToDict(row) for row in rows]

    def put(self, record):
        cursor = self.conn.cursor()
        cursor.execute(
            "INSERT INTO posts(userID, authorName, timestamp, content) VALUES(%s, %s, %s, %s)",
            (
                record["userID"],
                record["authorName"],
                record["timestamp"],
                record["content"]
            )
        )

    def __exit__(self, exitType, value, traceback):
        self.conn.close()
