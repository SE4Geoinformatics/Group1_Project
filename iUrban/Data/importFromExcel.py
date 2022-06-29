# 读取mac桌面text.xlsx文件内容后，将需要到字段信息（name,department,phonenumber,address,officeplace）存入mysql数据库实例，最终记得要关数据库和连接哦！
# 1 # 读取excel表的内容然后写入数据库
import xlrd
import pymysql
# 创建数据库连接
conn = pymysql.connect(host='localhost', user="root",
                       password='nihao12345', database='db1', charset='utf8')
cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
sql = "insert into parasaga (name,department,phonenumber,address,officeplace) values (%s,%s,%s,%s,%s)"
#打开文件
file = xlrd.open_workbook("/Users/lurj/Desktop/text.xlsx")
sheet_1 = file.sheet_by_index(0)  # 根据sheet页的排序选取sheet
row_content = sheet_1.row_values(0)  # 获取指定行的数据，返回列表，排序自0开始
row_number = sheet_1.nrows  # 获取有数据的最大行数
for i in range(2, row_number):
     name = sheet_1.cell(i, 0).value
     department = sheet_1.cell(i, 1).value
     phonenumber = sheet_1.cell(i, 2).value
     address = sheet_1.cell(i, 3).value
     officeplace = sheet_1.cell(i, 4).value
     values = (name, department, phonenumber, address, officeplace)
 #执行sql语句插入数据
     cursor.execute(sql, values)
     conn.commit()
cursor.close()
conn.close()
