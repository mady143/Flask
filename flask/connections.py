import sqlite3

conn = sqlite3.connect('testing.db')
print("Opened database successfully")

# conn.execute('CREATE TABLE students (firstname TEXT, lastname TEXT, email TEXT, address TEXT, city TEXT, pincode TEXT)')
print("Table created successfully")
conn.close()