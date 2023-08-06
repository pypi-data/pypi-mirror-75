import pymysql


mysql_dict = {'host':'localhost'}


def get_conn():
    conn = pymysql.connect(**mysql_dict)
    return conn
