from SQL import MyDb
from utils.log import log


def next_month(month):
    yy = month[:4]
    mm = month[-2:]
    if mm == '12':
        month_ = str(int(yy) + 1) + "-01-01"
    else:
        month_ = yy + '-' + "%02d" % (int(mm) + 1) + '-01'
    return month_


class commodity(object):
    def __init__(self, _id):
        # 商品属性初始化
        self.info = list()
        self._id = _id  # 商品编号
        self._root_class = ''  # 分类
        self._class = ''  # 二级分类
        self._name = ''  # 名称
        self._model = ''  # 规格型号
        self._unit = ''  # 单位
        self._is_tax = True  # 是否含税
        self._gross = ''  # 毛利
        self._net_profit = ''  # 净利润
        self._profit_margin = ''  # 利润率
        self._company = ''  # 销售单位
        self._begin = {'quantity': 0, 'price': 0, 'value': 0}  # 期初
        self._purchase = {'quantity': 0, 'price': 0, 'value': 0}  # 购入
        self._sell = {'quantity': 0, 'price': 0, 'value': 0}  # 销售
        self._store = {'quantity': 0, 'price': 0, 'value': 0}  # 库存
        self._tax = {'value_add_tax': 0, 'additional': 0, 'stamp_duty': 0}  # 税费
        self.update_row()

    def update_row(self):
        # 更新行信息 储存在列表中
        # 0-6
        self.info = [self._id, self._root_class, self._class, self._name, self._model, self._unit, self._is_tax]
        # 7-18
        self.info += list(self._begin.values()) + list(self._purchase.values()) + list(self._sell.values()) + list(
            self._store.values())
        # 19
        self.info += [self._gross]
        # 20-22
        self.info += list(self._tax.values())
        # 23-25
        self.info += [self._net_profit, self._profit_margin, self._company]

    def get_id(self):
        return self._id

    def get_sell_dic(self):
        return self._sell

    def load_from_tb_store(self, row):
        """从期初表的行中获取数据"""
        print(row)
        self._id = row[0]
        self._root_class = row[3]  # 分类
        self._class = row[4]  # 二级分类
        self._name = row[5]  # 名称
        self._model = row[6]  # 规格型号
        self._unit = row[7]  # 单位
        self._is_tax = row[-1]  # 是否含税
        self._begin = {'quantity': row[8], 'price': row[9], 'value': row[10]}  # 购入
        self.update_row()

    def load_from_tb_buy(self, row):
        """从期初表的行中获取数据"""
        print(row)
        self._id = row[0]
        self._root_class = row[3]  # 分类
        self._class = row[4]  # 二级分类
        self._name = row[5]  # 名称
        self._model = row[6]  # 规格型号
        self._unit = row[7]  # 单位
        self._is_tax = row[-1]  # 是否含税
        if self._is_tax:
            self._purchase = {'quantity': row[8], 'price': row[9], 'value': row[11]}  # 购入
        else:
            self._purchase = {'quantity': row[8], 'price': row[10], 'value': row[12]}  # 购入
        self.update_row()

    def load_from_tb_sell(self, row):
        """从期初表的行中获取数据"""
        print(row)
        self._id = row[0]
        self._root_class = row[3]  # 分类
        self._class = row[4]  # 二级分类
        self._name = row[5]  # 名称
        self._model = row[6]  # 规格型号
        self._unit = row[7]  # 单位
        self._is_tax = row[-2]  # 是否含税
        if self._is_tax:
            self._sell = {'quantity': row[8], 'price': row[9], 'value': row[11]}  # 购入
        else:
            self._sell = {'quantity': row[8], 'price': row[10], 'value': row[12]}  # 购入
        self.update_row()

    def cat_with_sell_commodity(self, item):
        """链接两个商品信息
        期初 + 购入 - 销售 = 库存
        """
        # 销售额并入一个商品对象

        self._sell = item.get_sell_dic()
        for i, key in enumerate(self._store.keys()):
            self._store[key] = str(float(self._begin[key]) + float(self._purchase[key]) - float(self._sell[key]))
        self.update_row()


class company(object):
    def __init__(self, name):
        self.name = name
        self.direct = ''
        self.commodity_list = list()

    def is_exist(self, commodity_id):
        """检查该公司中是否存在了同id商品，存在则返回True， 否则False"""
        for item in self.commodity_list:
            if item.get_id() == commodity_id:
                return True
        return False

    def add_commodity(self, item: commodity):
        """
        添加商品方法，在该公司所拥有的商品列表中添加一个商品
        :param item:一个商品对象
        :return:
        """
        item._company = self.name
        item.update_row()
        self.commodity_list.append(item)

    def get_name(self):
        return self.name


class company_in(company):
    """
    定义一个公司类，公司的商品列表中保存着属于这个公司的商品
    """

    def __init__(self, name):
        super().__init__(name)
        # 这个公司的属性‘方向’为'IN'
        self.direct = 'IN'


class company_out(company):
    """
    定义一个公司类，公司的商品列表中保存着属于这个公司的商品
    """

    def __init__(self, name):
        super().__init__(name)
        # 这个公司的属性‘方向’为'OUT'
        self.direct = 'OUT'


class frame(object):
    """
    所有数据，主要包含各公司
    """

    def __init__(self):
        self.company_in_list = list()
        self.company_out_list = list()

    def add_company(self, item: company):
        """
        添加公司方法
        :param item:一个公司对象
        :return:
        """
        if item.direct == 'IN':
            self.company_in_list.append(item)
        elif item.direct == 'OUT':
            self.company_out_list.append(item)
        else:
            raise Exception(log('出错了'))

    def is_exist(self, company_name, direct):
        """检查该公司中是否存在了同id商品，存在则返回True， 否则False"""
        if direct == 'IN':
            for item in self.company_in_list:
                if item.get_name() == company_name:
                    return True
            return False
        elif direct == 'OUT':
            for item in self.company_out_list:
                if item.get_name() == company_name:
                    return True
            return False
        else:
            raise Exception(log('出错了'))

    def get_company(self, company_name, direct):
        """通过公司名称获取公司对象"""
        if not self.is_exist(company_name, direct):
            # 如果不存在这家公司，将无法获取公司对象
            log('出错了，没有这家公司')
            return

        if direct == 'IN':
            for _company in self.company_in_list:
                if _company.get_name() == company_name:
                    return _company
        elif direct == 'OUT':
            for _company in self.company_out_list:
                if _company.get_name() == company_name:
                    return _company
        else:
            raise Exception(log('出错了'))

    def cat_tables(self):
        """链接出库和入库方向的多个表 期初 + 购入 - 销售 = 库存"""
        commodity_sell_list = list()
        commodity_no_sell_list = list()
        for company_out_ in self.company_out_list:
            # 在减项公司里遍历
            for item_out in company_out_.commodity_list:
                # 在某一个减项公司中遍历商品
                for company_in_ in self.company_in_list:
                    # 在增项公司遍历
                    for item_in in company_in_.commodity_list:
                        # 在某一个增项公司里遍历商品
                        if item_in.get_id() == item_out.get_id():
                            # 如果减向有相同id的商品，便合并两个商品的信息
                            # 将增项商品对象复制一份
                            item = item_in
                            item.cat_with_sell_commodity(item_out)
                            commodity_sell_list.append(item)
                            break
            commodity_sell_list.append(['小计', '', company_out_.name])

        for company_in_ in self.company_in_list:
            # 在增项公司遍历
            for item_in in company_in_.commodity_list:
                # 在某一个增项公司里遍历商品
                for company_out_ in self.company_out_list:
                    # 在减项公司里遍历
                    for item_out in company_out_.commodity_list:
                        # 在某一个减项公司中遍历商品
                        if item_in.get_id() != item_out.get_id():
                            # 如果减项没有相同id的商品，添加这个商品到无出售列表
                            commodity_no_sell_list.append(item_in)
                            break
                    break

        # 在某一个减项公司中遍历商品
        # for company_add in self.company_in_list:
        #     # 在增项公司里遍历
        #     for item_in in company_add.commodity_list:
        #         # 在某一个增项公司中遍历商品
        #         # 将商品对象复制一份
        #         item = item_in
        #         flag = "小计"
        #         for company_out_ in self.company_out_list:
        #             # 在减项公司遍历
        #             for item_out in company_out_.commodity_list:
        #                 # 在某一个减项公司里遍历商品
        #                 if item_in.get_id() == item_out.get_id():
        #                     # 如果减向有相同id的商品，便合并两个商品的信息
        #                     item.cat_with_sell_commodity(item_out)
        #                     flag = '有出售'
        #                     break
        #                 else:
        #                     flag = '无出售'
        #         commodity_list.append(['数据', flag, item])
        #     commodity_list.append(['小计', '', company_add.name])
        return commodity_sell_list, commodity_no_sell_list


class Income_Table(object):
    def __init__(self, month, db):
        self.db = db
        self.query_month = month
        data = self.get_data()

        self.Frame = self.wash_data(data)

    def get_data(self):
        """获取数据库个表单中符合所查询月份的所有数据"""
        task = "SELECT * FROM tb_store WHERE date < '{}';".format(self.query_month + "-01")
        self.db.execute(task)
        store_data = self.db.cursor.fetchall()

        next_m = next_month(self.query_month)
        task = "SELECT * FROM tb_buy WHERE date >= '{}' AND date < '{}';".format(self.query_month + "-01", next_m)
        # print(self.query_month + "-01", next_m)
        self.db.execute(task)
        buy_data = self.db.cursor.fetchall()

        task = "SELECT * FROM tb_sell WHERE date >= '{}' AND date < '{}';".format(self.query_month + "-01", next_m)
        print(task)
        self.db.execute(task)
        sell_data = self.db.cursor.fetchall()
        # 期初 购入 出售
        return [store_data, buy_data, sell_data]

    @staticmethod
    def wash_data(tables):
        """
        清洗数据
        :param tables: 获取的数据表
        :return: Null
        """
        store_data, buy_data, sell_data = tables[0], tables[1], tables[2]
        washed_table = []  # 清洗好的数据
        Frame = frame()  # 创建一个总数据结构对象

        for row in store_data:
            # 获取该数据的不同字段
            _id = row[0]
            _company = row[2]
            if Frame.is_exist(_company, 'IN'):
                # 如果之前存在了这个公司，那么向这个公司添加商品
                Company = Frame.get_company(_company, 'IN')
                if not Company.is_exist(_id):
                    # 如果这家公司没有这个商品那么向这家公司添加这个商品
                    item = commodity(_id)
                    item.load_from_tb_store(row)
                    Company.add_commodity(item)
            else:
                # 如果这个公司之前不存在，那么创建一个公司，并将商品放到这个公司里
                Company = company_in(_company)
                item = commodity(_id)
                item.load_from_tb_store(row)
                Company.add_commodity(item)
                Frame.add_company(Company)

        for row in buy_data:
            # 获取该数据的不同字段
            _id = row[0]
            _company = row[2]
            if Frame.is_exist(_company, 'IN'):
                # 如果之前存在了这个公司，那么向这个公司添加商品
                Company = Frame.get_company(_company, 'IN')
                if not Company.is_exist(_id):
                    # 如果这家公司没有这个商品那么向这家公司添加这个商品
                    item = commodity(_id)
                    item.load_from_tb_buy(row)
                    Company.add_commodity(item)
            else:
                # 如果这个公司之前不存在，那么创建一个公司，并将商品放到这个公司里
                Company = company_in(_company)
                item = commodity(_id)
                item.load_from_tb_buy(row)
                Company.add_commodity(item)
                Frame.add_company(Company)

        for row in sell_data:
            # 获取该数据的不同字段
            _id = row[0]
            _company = row[2]
            if Frame.is_exist(_company, 'OUT'):
                # 如果之前存在了这个公司，那么向这个公司添加商品
                Company = Frame.get_company(_company, 'OUT')
                if not Company.is_exist(_id):
                    # 如果这家公司没有这个商品那么向这家公司添加这个商品
                    item = commodity(_id)
                    item.load_from_tb_sell(row)
                    Company.add_commodity(item)
            else:
                # 如果这个公司之前不存在，那么创建一个公司，并将商品放到这个公司里
                Company = company_out(_company)
                item = commodity(_id)
                item.load_from_tb_sell(row)
                Company.add_commodity(item)
                Frame.add_company(Company)

        return Frame

    @staticmethod
    def generate_data(self):
        Frame = self.Frame
        with_sell, without_sell = Frame.cat_tables()
        income_table = with_sell + without_sell
        return income_table


if __name__ == '__main__':
    it = Income_Table('2022-01', MyDb())
    data_list = it.generate_data(it)
    print(0)
    # a = commodity(1)
    # print(a.info)
    # print(len(a.info))
