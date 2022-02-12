ll = ["1712100491", "2021-11-20 00:00:00", "广州莱贝生活用品有限公司", "28日用杂品", "12*份数盒", "饭盒", "None", "个",
      "1", "0", "3000", "0", "3000",
      "P92467050-55-5190.09", "0"]


def process_list(list_):

    def float_(string):
        if string == 'None':
            return 0
        else:
            return float(string)

    tax = int(list_[-1])
    quantity = float_(list_[8])
    price_with_tax = float_(list_[9])
    price_without_tax = float_(list_[10])
    value_with_tax = float_(list_[11])
    value_without_tax = float_(list_[12])

    # 如果四个价格都有那么直接返回原列表
    if price_with_tax and price_without_tax and value_with_tax and value_without_tax:
        return list_

    # 如果四个价格不全且含税
    if tax:
        if not price_with_tax:
            # 如果商品含税 且单价为空 则计算单价
            price_with_tax = value_with_tax / quantity
        else:
            # 否则计算总金额
            value_with_tax = price_with_tax * quantity

        # 计算商品未税额
        price_without_tax = price_with_tax / 1.13
        value_without_tax = value_with_tax / 1.13
    else:
        if not price_without_tax:
            # 如果商品未税 且单价为空 则计算单价
            price_without_tax = value_without_tax / quantity
        else:
            # 否则计算总金额
            value_without_tax = price_without_tax * quantity
        # 计算商品含税额
        price_with_tax = price_without_tax * 1.13
        value_with_tax = value_without_tax * 1.13

    list_[9:13] = [str(price_with_tax), str(price_without_tax),
                   str(value_with_tax), str(value_without_tax)]
    return list_

print(process_list(ll))
