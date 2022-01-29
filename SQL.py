import pymysql


class MyDb(object):
    def __init__(self):
        # 连接数据库
        self.db = pymysql.connect(host='39.99.159.98',
                                  user='root',
                                  password='zsy@100618',
                                  database='Finance_DB')
        self.cursor = self.db.cursor()
        # print('连接数据库成功')

    def execute(self, task):
        # 执行SQL语句 以字符串形式传入
        # self.cursor.execute("use Finance_DB;")
        self.cursor = self.db.cursor()
        try:
            self.cursor.execute(task)
            self.cursor.connection.commit()
        except:
            self.db.rollback()
        self.cursor.close()

    def upload(self, table, dic):
        print('开始上载数据')
        task = 'insert into {}(id, source, date, Specifications, model, quantity) ' \
               'values({},{},{},{},{},{});'.format(table,
                                                   dic['采购单号'],
                                                   dic['采购单位'],
                                                   dic['采购日期'],
                                                   dic['规格'],
                                                   dic['型号'],
                                                   dic['数量'])
        self.execute(task)

        print('上载数据成功')

    def query(self):
        self.execute("select * from record;")
        temp = self.cursor.fetchall()
        return temp

    def delete(self, datas):
        task = 'delete from record where id in ({});'.format(datas)
        self.execute(task)
        print(task)
        print('出库成功')


def main():
    MDB = MyDb()
    # MDB.execute('CREATE TABLE EMPLOYEE (FIRST_NAME  CHAR(20) NOT NULL,'
    #             'LAST_NAME  CHAR(20),AGE INT,SEX CHAR(1),INCOME FLOAT )')


if __name__ == '__main__':
    main()
