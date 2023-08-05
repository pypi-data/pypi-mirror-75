#!/usr/bin/python3
# -*- coding: utf-8 -*-
import pymysql.cursors
import os


# Возвращает строку типа DATE для SQL
def get_date_type(date):
    if date['bday'] == 0:
        return "`0'"
    return str(date['byear']) + '-' + str(date['bmonth']) + '-' + str(date['bday'])


# Информация из config
def get_con_info():
    path = os.path.abspath('')
    info = []
    path = path[:path.rfind('/')] + '/config.env'
    file = open(path)
    for line in file:
        if line.find('username=') != -1 or line.find('password=') != -1 or line.find('base_name=') != -1 or line.find('temporary_table=') != -1 or line.find('permanent_table=') != -1 or line.find('chromedriver_path=') != -1 or line.find('start_alert=') != -1 or line.find('error_alert=') != -1:
            info.append(line[line.find('"')+1:line.rfind('"')])
    return info


def get_connection(info):
    return pymysql.connect(
        host='localhost',
        user=info[0],
        password=info[1],
        db=info[2],
    )


# Сохранение + миграция + комит
def mySQL_save(people, info=None):
    if info == None:
        info_con = get_con_info()
    else:
        info_con = info
    con = get_connection(info_con)
    with con.cursor() as cursor:
        cursor.execute(f"DROP TABLE IF EXISTS `{info_con[3]}`;")
        cursor.execute(f"CREATE TABLE `{info_con[3]}` (`last_name` varchar(50) NOT NULL, `first_name` varchar(50) NOT NULL, `middle_name` varchar(50) NOT NULL, `birth_date` date NOT NULL, `position_id` int unsigned NOT NULL, `image_url` varchar(255) DEFAULT NULL, `url` varchar(255) NOT NULL, PRIMARY KEY (`last_name`,`first_name`,`middle_name`,`birth_date`,`position_id`)) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;")
        for person in people:
            sql = f"INSERT IGNORE INTO `{info_con[3]}` (`last_name`, `first_name`, `middle_name`, `birth_date`, `position_id`, `image_url`, `url`) VALUES (%s, %s, %s, %s, %s, %s, %s)"
            cursor.execute(sql, (person['last_name'][0].upper() + person['last_name'][1:],
                                 person['first_name'][0].upper() + person['first_name'][1:],
                                 person['middle_name'][0].upper() + person['middle_name'][1:],
                                 get_date_type({'bday': person['bday'], 'bmonth': person['bmonth'], 'byear': person['byear']}),
                                 person['position_id'],
                                 person['image_link'],
                                 person['link']
                                 )
                           )
        cursor.execute(f"DELETE LOW_PRIORITY FROM `{info_con[4]}`;")
        cursor.execute(f"INSERT INTO {info_con[2]}.{info_con[4]} SELECT * FROM {info_con[2]}.{info_con[3]};")
        cursor.execute(f"DROP TABLE IF EXISTS `{info_con[3]}`;")
    con.commit()


def get_len():
    info = get_con_info()
    con = get_connection(info)
    with con.cursor() as cursor:
        cursor.execute(f"SELECT COUNT(*) FROM `{info[4]}`")
        length = cursor.fetchall()
    return length[0][0]
