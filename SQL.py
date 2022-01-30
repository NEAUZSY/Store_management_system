import pymysql


class MyDb(object):
    def __init__(self):
        # 连接数据库
        self.db = pymysql.connect(host='39.99.159.98',
                                  user='finance',
                                  password='finance',
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
        default = 0
        dic['规格型号'] = '个'
        dic['含税进价'] = default
        dic['未税进价'] = default
        # keys = 'id，kind，name，source，model，unit，quantity，cost_withtax，cost_withouttax'
        task = 'insert into {} ' \
               'values({},"{}","{}","{}","{}","{}",{},{},{});'.format(table,
                                                                      dic['商品编号'],
                                                                      dic['类别'],
                                                                      dic['商品名称'],
                                                                      dic['商品来源'],
                                                                      dic['规格型号'],
                                                                      dic['单位'],
                                                                      dic['数量'],
                                                                      dic['含税进价'],
                                                                      dic['未税进价'])
        print(task)
        self.execute(task)

        print('上载数据成功')

    def query(self):
        self.execute("select * from store;")
        temp = self.cursor.fetchall()
        return temp

    def delete(self, datas):
        task = 'delete from store where id in ({});'.format(datas)
        self.execute(task)
        print(task)
        print('出库成功')


def main():
    MDB = MyDb()
    # MDB.execute('CREATE TABLE EMPLOYEE (FIRST_NAME  CHAR(20) NOT NULL,'
    #             'LAST_NAME  CHAR(20),AGE INT,SEX CHAR(1),INCOME FLOAT )')


if __name__ == '__main__':
    main()
