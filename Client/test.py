from SQL import MyDb


def next_month(month):
    yy = month[:4]
    mm = month[-2:]
    if mm == '12':
        month_ = str(int(yy) + 1) + "-01-01"
    else:
        month_ = yy + '-' + "%02d" % (int(mm) + 1) + '01'
    return month_


class Income_Table(object):
    def __init__(self, month, db):
        self.db = db
        self.query_month = month
        data = self.get_data()
        for i in data:
            for j in i:
                print(j)
            print('-'*50)

    def get_data(self):
        """获取数据库个表单中符合所查询月份的所有数据"""
        task = "SELECT * FROM tb_store WHERE date < '{}';".format(self.query_month + "-01")
        self.db.execute(task)
        store_data = self.db.cursor.fetchall()

        next_m = next_month(self.query_month)
        task = "SELECT * FROM tb_buy WHERE date >= '{}' AND date < '{}';".format(self.query_month + "-01", next_m)
        self.db.execute(task)
        buy_data = self.db.cursor.fetchall()

        task = "SELECT * FROM tb_sell WHERE date >= '{}' AND date < '{}';".format(self.query_month + "-01", next_m)
        self.db.execute(task)
        sell_data = self.db.cursor.fetchall()

        return [store_data, buy_data, sell_data]


if __name__ == '__main__':
    it = Income_Table('2021-12', MyDb())
    it.get_data()
