import hashlib
import binascii
import os

from model.DbConnection import DbConnection

db_ = DbConnection(database="P1_Database")

def add_user(firstname, name, email, password):
    if db_.query("SELECT * FROM P1_Database.User WHERE Email=%s", (email, )):
        return False

    # 1) convert password to bytes
    pwd_bytes = bytes(password, 'utf-8')

    # 2) generate random salt, result is in bytes
    salt_bytes = os.urandom(16)

    # 3) calculate hash
    hash_bytes = hashlib.pbkdf2_hmac('sha256', pwd_bytes, salt_bytes, 100000)

    # 4) convert to hex-string
    salt_string = binascii.hexlify(salt_bytes).decode('utf-8')
    hash_string = binascii.hexlify(hash_bytes).decode('utf-8')

    # 5) save to db
    sql = (
        'INSERT INTO P1_Database.User (Firstname, Name, Email, pwd_hash, pwd_salt) '
        'VALUES ( %(new_firstname)s, %(new_name)s, %(new_email)s, %(new_hash)s, %(new_salt)s );'
    )
    params = {
        'new_firstname': firstname,
        'new_name': name,
        'new_email': email,
        'new_hash': hash_string,
        'new_salt': salt_string,
    }
    # execute and done!
    result = db_.execute(sql, params)
    return result


def verify_credentials(email, password):

    # 1) get hash and salt from db
    sql = 'SELECT pwd_hash, pwd_salt FROM P1_Database.User WHERE Email=%(check_email)s;'
    params = {
        'check_email': email
    }
    result = db_.query(sql, params, True)

    # when user does not exist, we do not need to look further
    if not result:
        return False

    # 'username' is PK so there can only be one row
    db_user = result[0]

    # get hash and salt from result
    db_hash_string = db_user['pwd_hash']
    db_salt_string = db_user['pwd_salt']

    # 2) calculate hash with ENTERED PASSWORD and SAVED SALT
    # firstly convert both to bytes
    pwd_bytes = bytes(password, 'utf_8')
    db_salt_bytes = binascii.unhexlify(db_salt_string)

    # calculate new hash
    hash_bytes = hashlib.pbkdf2_hmac('sha256', pwd_bytes, db_salt_bytes, 100000)

    # convert to string to compare
    hash_string = binascii.hexlify(hash_bytes).decode('utf-8')

    # 3) db_hash is shorter than hash_string so if it is part of the hash_string, it is okay
    return db_hash_string in hash_string

# test
if __name__ == "__main__":
    if input("Table 'users' will be truncated, continue? (y/n)").lower() == "y":
        db_.execute("DELETE FROM users;")

        add_user('myuser', 'mypassword')
        add_user('youruser', 'yourpassword')
        print(verify_credentials('myuser', 'mypassword'))
        print(verify_credentials('myuser', 'wrongpassword'))
        print(verify_credentials('wronguser', 'anypassword'))
        print(verify_credentials('youruser', 'yourpassword'))

        add_user('firstuser', 'samepassword')
        add_user('otheruser', 'samepassword')
        hashes = db_.query("SELECT pwd_hash FROM users WHERE username IN ('firstuser', 'otheruser');", dictionary=True)
        print(hashes[0])
        print(hashes[1])

        add_user("'; DROP TABLE users; --", "'; SELECT username, password FROM users; --")

