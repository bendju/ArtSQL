from database import *

db = ArtSQL(name=STRING, age=INTEGER, email=STRING)
db2 = ArtSQL(name=STRING, age=INTEGER, email=STRING)

db.add_data(name='beni', age=10, email='beni@gmail.com')
for _ in range(100):
    db2.add_data(name='beni', age=10, email='beni@gmail.com')
