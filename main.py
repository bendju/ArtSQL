from database import *

db = ArtSQL(name=STRING, age=INTEGER, email=STRING, score=FLOAT)
db2 = ArtSQL(name=STRING, age=INTEGER, email=STRING)

db.add_data(name='beni', age=10, email='beni@gmail.com', score=1.3)
db.add_data(name='beni', age=10, email='beni@gmail.com')
for _ in range(10):
    db2.add_data(name='beni', age=10, email='hello@gmail.com')

print(db2.get_all_data())