import pymysql

pymysql.install_as_MySQLdb()
conn =pymysql.connect(host='127.0.0.1', user='root', passwd="root", port=3306, charset='utf8')

cur =conn.cursor

print(cur)
print(conn)


conn.close