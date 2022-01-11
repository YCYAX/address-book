import os
import pandas


class AddressBook:
    # 初始化
    def __init__(self):
        # 路径
        self.path = "address_book.csv"
        # 需要的列表名
        self.name = []
        self.address = []
        self.number = []
        # 循环值
        self.while_number = 0
        # 搜索需要用到的列表
        self.search_list = [
            "姓名",
            "地址",
            "电话"
        ]

    # 路径检测
    def address_book_csv(self):
        if os.path.exists(self.path) is False:
            # 创建表
            address_book = pandas.DataFrame(columns=["姓名", "地址", "电话"])
            address_book.to_csv(self.path, sep=',', index=False, encoding='gb18030')
            print("\033[4;30;41m初始化成功\033[0m")

    # 写入功能
    def address_book_write(self):
        print("请依次输入姓名，地址，电话。")
        while True:
            # 接受信息并存入字典dict
            name = str(input("姓名："))
            address = str(input("地址："))
            number = str(input("电话："))
            self.name.append(name)
            self.address.append(address)
            self.number.append(number)
            if name == " ":
                print("不要输入空的内容")
                return AddressBook.address_book_write(self)
            if address == " ":
                print("不要输入空的内容")
                return AddressBook.address_book_write(self)
            if number == " ":
                print("不要输入空的内容")
                return AddressBook.address_book_write(self)
            dict = {
                "姓名": name,
                "地址": address,
                "电话": number
            }
            print("添加成功")
            # 读取csv
            address_book_csv = pandas.read_csv(self.path, encoding='gb18030')
            # 如果为空直接写入
            if address_book_csv.empty is True:
                data = pandas.DataFrame(dict, index=[1])
                data.to_csv(self.path, sep=',', index=False, encoding='gb18030')
            # 不为空合并表
            else:
                data = pandas.DataFrame(dict, index=[1])
                data_csv = address_book_csv.append(data, ignore_index=True)
                data_csv.to_csv(self.path, sep=',', index=False, encoding='gb18030')
            yes_or_no = input("是否继续添加[y/n]")
            if yes_or_no == "y":
                pass
            else:
                break
        return AddressBook.main(self)

    # 查询功能
    def address_book_search(self):
        # 读表
        address_book_csv = pandas.read_csv(self.path, encoding='gb18030')
        print("输入1使用姓名查找")
        print("输入2使用地址查找")
        print("输入3使用电话查找")
        print("输入q即可退出查询")
        while True:
            try:
                while True:
                    search_number = input()
                    if search_number == "q":
                        return AddressBook.main(self)
                    elif type(int(search_number)) is int:
                        if 1 <= int(search_number) <= 3:
                            search_number = int(search_number)
                            while True:
                                print("输入查找的信息：")
                                search_txt = input()
                                # 对应快速查找
                                top = self.search_list[search_number - 1]
                                # 查找对应标题
                                top_info = address_book_csv[top]
                                if search_number != 3:
                                    info = address_book_csv.index[top_info == search_txt]
                                else:
                                    info = address_book_csv.index[top_info == int(search_txt)]
                                # 对应索引
                                info_index = info.tolist()
                                info_list = []
                                # 预定义人数为0
                                people = 0
                                # 循环3列
                                for column_number in range(len(self.search_list)):
                                    top = self.search_list[column_number]
                                    info_value = address_book_csv.iloc[info_index][top]
                                    info_value_list = info_value.tolist()
                                    # 定义人数
                                    people = len(info_value_list)
                                    # 把查找的信息存入列表
                                    for people_number in range(people):
                                        info_value_list_str = ''.join(str(info_value_list[people_number]))
                                        info_list.append(info_value_list_str)
                                # 整理列表信息
                                # 每个人
                                for people_number in range(people):
                                    info_list_str = []
                                    # 每一列
                                    for column_number in range(3):
                                        info_lis_value = info_list[people_number + column_number * people]
                                        info_list_str.append(info_lis_value)
                                    info_str = ','.join(info_list_str)
                                    print(info_str)
                                yes_or_no = input("是否继续当前查询[y/n]")
                                if yes_or_no == "y":
                                    pass
                                else:
                                    return AddressBook.address_book_search(self)
                        else:
                            print("请输入小于等于3的数字")
            except:
                print("请输入整数")
                return AddressBook.address_book_search(self)

    # 按照指定要求排序展示
    def address_book_sort(self):
        while True:
            print("输入1按输入方式排序")
            print("输入2按姓名排序")
            print("输入3按地址排序")
            print("输入4按电话排序")
            print("输入q退出排序")
            try:
                sort_number = input()
                # 默认方式排序
                # 为1输出默认
                if sort_number == "q":
                    return AddressBook.main(self)
                if int(sort_number) == 1:
                    csv = pandas.read_csv(self.path, encoding='gb18030')
                    info = csv.sort_index()
                    print(info)
                # 其余方式
                if 1 < int(sort_number) <= 4:
                    csv = pandas.read_csv(self.path, encoding='gb18030')
                    info = csv.sort_values(by=self.search_list[int(sort_number) - 2])
                    print(info)
                else:
                    print("请输入小于等于4的数字")
            except:
                print("请输入整数")

    # 修改写入值
    def address_book_change(self):
        # 读取
        address_book_csv = pandas.read_csv(self.path, encoding='gb18030')
        while True:
            change_or_delete = str(input("修改/删除/退出修改[c/d/q]:"))
            if change_or_delete == "c":
                print("输入姓名查找修改")
                # 查找对应
                search_txt = str(input())
                top_info = address_book_csv["姓名"]
                info = address_book_csv.index[top_info == search_txt]
                info_index = info.tolist()
                # 输入新的
                address = input("输入新的地址:")
                number = input("输入新的号码:")
                try:
                    # 修改
                    address_book_csv.loc[info_index[0], "地址"] = address
                    address_book_csv.loc[info_index[0], "电话"] = number
                    # 写入
                    address_book_csv.to_csv(self.path, sep=',', index=False, encoding='gb18030')
                    print("修改成功")
                    yes_or_no = input("是否继续修改[y/n]")
                    if yes_or_no == "y":
                        pass
                    else:
                        return AddressBook.address_book_change(self)
                except:
                    print("修改的数据有错误")
                    return AddressBook.address_book_change(self)
            elif change_or_delete == "d":
                print("输入姓名查找修改")
                # 查找对应
                search_txt = str(input())
                top_info = address_book_csv["姓名"]
                info = address_book_csv.index[top_info == search_txt]
                info_index = info.tolist()
                delete = address_book_csv.index[[info_index[0]]]
                address_book_csv.drop(delete, inplace=True)
                address_book_csv.to_csv(self.path, sep=',', index=False, encoding='gb18030')
                print("修改成功")
                yes_or_no = input("是否继续修改[y/n]")
                if yes_or_no == "y":
                    pass
                else:
                    return AddressBook.address_book_change(self)
            elif change_or_delete == "q":
                return AddressBook.main(self)
            else:
                print("输入c或d")
                return AddressBook.address_book_change(self)

    # 主程序
    def main(self):
        AddressBook.address_book_csv(self)
        print("欢迎使用通讯录系统")
        print("--------------")
        print("\033[4;30;41m输入数字使用功能\033[0m")
        print("1.通讯录写入功能")
        print("2.通讯录修改功能")
        print("3.通讯录搜索功能")
        print("4.通讯录展示功能")
        print("--------------")
        while True:
            try:
                input_number = int(input("输入功能序号："))
                if input_number < 1 or input_number > 4:
                    print("请输入正确的序号")
                elif input_number == 1:
                    AddressBook.address_book_write(self)
                elif input_number == 2:
                    AddressBook.address_book_change(self)
                elif input_number == 3:
                    AddressBook.address_book_search(self)
                elif input_number == 4:
                    AddressBook.address_book_sort(self)
            except:
                print("请输入整数")


if __name__ == "__main__":
    run = AddressBook()
    run.main()
