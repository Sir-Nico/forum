import sqlite3
import os
import datetime


DB_PATH = "../forum.db"


class Connection():
    # Context manager which makes code more readable and safer to execute
    def __init__(self):
        self.conn = sqlite3.connect(DB_PATH)
        self.c = self.conn.cursor()
    
    def __enter__(self):
        return self
    
    def __exit__(self, excType, excValue, traceback):
        
        self.conn.commit()
        self.conn.close()

        if excType:
            print(excType)
        if excValue:
            print(excValue)
        if traceback:
            print(traceback)


def init_tables():
    with Connection() as db:
        db.c.execute("DROP TABLE IF EXISTS messages")
        # content: message body, i.e. "Hello everyone!"
        # poster: user ID of original poster
        # post_time: Time message was posted
        # id: message ID
        db.c.execute("""CREATE TABLE messages (
            content TEXT,
            poster INT,
            post_time TEXT,
            id INT  -- Unique message ID
        )""")
        log(f"Successfully created Message Table at {os.path.abspath(DB_PATH)}")

        db.c.execute("DROP TABLE IF EXISTS users")
        # NOTE: Will expand on this later, but just need to get the ball rolling
        db.c.execute("""CREATE TABLE users (
            user_id INT,
            username TEXT,
            password TEXT
        )""")
    log(f"Successfully created User Table at {os.path.abspath(DB_PATH)}")


def fetch_message(id):
    with Connection() as db:
        db.c.execute("SELECT * FROM messages WHERE id = ?", [id])
        message = db.c.fetchall()[0]
    return message

def create_post(content):
    with Connection() as db:
        db.c.execute("""INSERT INTO messages(
            content,
            poster,
            post_time,
            id                        -- Some of the values are None as of now
        ) VALUES (?, ?, ?, ?)""", [content, None, datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S"), 0])
    log(f"Successfully added message {None} to database at {os.path.abspath(DB_PATH)}")


# Function for testing, messing around, whatever really.
def whatever():
    with Connection() as db:
        pass


# Outputs actions done by the database interface to a text file
# Example: "[28/03/2023]: Successfully initialised databases to <path to database>"
def log(status):
    with open("../db.log", "a") as f:
        current_time = datetime.datetime.now()
        current_time = current_time.strftime("%d/%m/%Y %H:%M:%S") # Formaterer informasjonen fra datetime
        f.write(f"[{current_time}]: {status}\n")        


def main():
    # init_tables()
    create_post("Hello World!")


if __name__ == "__main__":
    main()