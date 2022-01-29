import pymysql

db = pymysql.connect(host='39.99.159.98',
                     user='root',
                     password='zsy@100618',
                     database='Finance_DB')
cursor = db.cursor()
# cursor.execute("insert into record(id) value(343242);")
# cursor.connection.commit()
cursor.execute("select * from record;")
a = cursor.fetchall()
print(a)
