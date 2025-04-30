from getpass import getpass
import mysql.connector
import warnings
warnings.filterwarnings('ignore')


# connection establishment
cnx = mysql.connector.connect(user=input('User:'),
                              password=getpass('Password:'),
                              host='localhost',
                              allow_local_infile=True)

cursor = cnx.cursor(buffered=True)

# creation break point database
create_break_point_db = '''
create database if not exists break_point_db character set utf8
'''

# use break point database
use_break_point_db = '''
use break_point_db
'''

# creation bp_no table
create_table_bp_no = '''
create table if not exists bp_no (
    bp_id int unsigned not null auto_increment,
    break_point varchar(10) not null,
    bp_status enum('Approved', 'Published', 'Closed'),
    batch varchar(10),
    bp_date date,
    model varchar(20) not null,
    part_change enum('Before change', 'After change'),
    part_operation enum('Add', 'Update', 'Replace', 'Delete'),
    part_number varchar(20) not null,
    ch_part_name varchar(50) not null,
    en_part_name varchar(100),
    workshop enum('SW', 'PS', 'AS', 'COMP', 'ES') not null,
    comment varchar(100),
    constraint pk_bp_no primary key (bp_id)
)
'''

# uploading bp_no data
upload_bp_no_data = '''
load data local infile 'bp_project/csv_data/bp_no.csv'
into table bp_no
fields terminated by ';' 
lines terminated by '\n' 
ignore 1 rows
(bp_id, break_point, bp_status, batch, bp_date, model, part_change, part_operation, part_number, ch_part_name, en_part_name, workshop, comment);
'''

# execution sql scripts
cursor.execute(create_break_point_db)
cursor.execute(use_break_point_db)
cursor.execute(create_table_bp_no)
cursor.execute(upload_bp_no_data)
cnx.commit()

if cnx.is_connected():
    cursor.close()
    cnx.close()