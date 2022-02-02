import pymysql
from datetime import datetime


class MyDb(object):
    def __init__(self):
        # 连接数据库
        self.db = pymysql.connect(host='39.99.159.98',
                                  user='finance',
                                  password='finance',
                                  database='Finance_DB')
        self.cursor = self.db.cursor()
        self.dic = {}
        self.delete_id = ''
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
        # self.cursor.close()

    def upload(self, table, dic):
        print('开始上载数据')
        default = 0
        if not dic['单位']:
            dic['单位'] = '个'
        # keys = 'id，kind，name，source，model，unit，quantity，cost_withtax，cost_withouttax'
        task = 'insert into {} ' \
               'values({},"{}","{}","{}","{}","{}","{}",' \
               '"{}",{},{},{},{},{},"{}",{});'.format(table,
                                                      dic['序号'],
                                                      dic['日期'],
                                                      dic['往来单位'],
                                                      dic['一级分类'],
                                                      dic['二级分类'],
                                                      dic['商品名称'],
                                                      dic['规格型号'],
                                                      dic['单位'],
                                                      dic['数量'],
                                                      dic['单价（含税）'],
                                                      dic['单价（未税）'],
                                                      dic['金额（含税）'],
                                                      dic['金额（未税）'],
                                                      dic['备注/序列号'],
                                                      dic['是否含税'])
        # print(task)
        self.execute(task)

        # print('上载数据成功')
        self.dic = dic
        self.refresh_store('add')

    def query(self, table):
        if table == 'tb_buy':
            self.execute("select input_what from %s;" % table)
            flags = self.cursor.fetchall()
            # print(flags)
            selects = []
            for flag in flags:
                if flag[0]:
                    # 含税
                    selects.append(
                        'id,date,source,root_class,class,name,model,unit,quantity,'
                        'price_withtax,value_withtax,remark from tb_buy where input_what=1;')
                else:
                    selects.append(
                        'id,date,source,root_class,class,name,model,unit,quantity,'
                        'price_withouttax,value_withouttax,remark from tb_buy where input_what=0;')
            # print(temp)
            for select in selects:
                # print(select)
                self.execute("select %s;" % select)
            temp = self.cursor.fetchall()
            return temp
        elif table == 'tb_store':
            self.execute("select * from %s;" % table)
            temp = self.cursor.fetchall()
            return temp

    def delete(self, datas):
        task = 'delete from tb_store where id in ({});'.format(datas)
        self.execute(task)
        # print(task)
        # print('出库成功')
        self.delete_id = datas
        self.refresh_store('delete')

    def add_sell_info(self, dics):
        # 增加sell表数据 输入为包含多个字典的列表
        for d in dics:
            task = 'insert into tb_sell ' \
                   'values({},"{}","{}","{}","{}","{}","{}",' \
                   '"{}",{},{},{},{},{},"{}",{});'.format(d['序号'],
                                                          d['日期'],
                                                          d['往来单位'],
                                                          d['一级分类'],
                                                          d['二级分类'],
                                                          d['商品名称'],
                                                          d['规格型号'],
                                                          d['单位'],
                                                          d['数量'],
                                                          d['单价'],
                                                          float(d['单价']) / 1.13,
                                                          d['金额'],
                                                          float(d['金额']) / 1.13,
                                                          d['备注/序列号'],
                                                          d['是否含税'])
            print(task)
            self.execute(task)
        print('更新出售信息表完成')

    def refresh_store(self, method):
        """根据入库信息和出库信息刷新库存单"""
        print('刷新库存', method)
        if method == 'add':
            dic = self.dic
            if dic['是否含税']:
                # 输入的是含税价
                dic['单价'] = dic['单价（含税）']
                dic['金额'] = dic['金额（含税）']
            else:
                dic['单价'] = dic['单价（未税）']
                dic['金额'] = dic['金额（未税）']
            task = 'insert into tb_store ' \
                   'values({},"{}","{}","{}","{}","{}","{}",' \
                   '"{}",{},{},{},"{}",{});'.format(dic['序号'],
                                                    dic['日期'],
                                                    dic['往来单位'],
                                                    dic['一级分类'],
                                                    dic['二级分类'],
                                                    dic['商品名称'],
                                                    dic['规格型号'],
                                                    dic['单位'],
                                                    dic['数量'],
                                                    dic['单价'],
                                                    dic['金额'],
                                                    dic['备注/序列号'],
                                                    dic['是否含税'])
            print(task)
            self.execute(task)
        elif method == 'delete':
            pass


def main():
    MDB = MyDb()
    # MDB.execute('CREATE TABLE EMPLOYEE (FIRST_NAME  CHAR(20) NOT NULL,'
    #             'LAST_NAME  CHAR(20),AGE INT,SEX CHAR(1),INCOME FLOAT )')


if __name__ == '__main__':
    main()
