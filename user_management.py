
import hashlib
import sqlite3


def create_hash(string):
    byte_string = string.encode("utf-8")
    sha256_hash = hashlib.sha256(byte_string).hexdigest()
    return sha256_hash

def log_func(username, password):

    password_hash = create_hash(password)

    with sqlite3.connect('inventory.db') as conn:
        users = conn.cursor()
        # Query to users info
        try:
            users.execute("""SELECT sha256 
                        FROM users
                        WHERE user_name=?
                        """, (username,))
            sha256 = users.fetchone()[0]
        except TypeError:
            return False
        if password_hash == sha256:
            return True
        
        return False