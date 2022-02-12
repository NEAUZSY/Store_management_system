import pymysql
task = "UPDATE tb_store SET quantity=1.0,value=(SELECT prince FROM (SELECT prince FROM tb_store WHERE id=0102927151) as temp)*1.0 WHERE id=0102927151;"
db = pymysql.connect(host='39.99.159.98',
                     user='root',
                     password='zsy@100618',
                     database='Finance_DB')
cursor = db.cursor()
# cursor.execute("insert into record(id) value(343242);")
# cursor.connection.commit()
cursor.execute(task)
a = cursor.fetchall()
print(a)
