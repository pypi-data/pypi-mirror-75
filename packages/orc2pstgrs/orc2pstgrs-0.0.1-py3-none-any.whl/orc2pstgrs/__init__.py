import pandas as pd
import cx_Oracle
import psycopg2 as pg2
from sqlalchemy import create_engine
import numpy as np
from datetime import date
from datetime import datetime

class dataload:

	def oracleDBconnection(host_name,port,service_name,user_name,password_orc):
    	dsn = cx_Oracle.makedsn(host_name,port,service_name)
    	conn = cx_Oracle.connect(user= user_name, password= password_orc, dsn=dsn)
    	print('Connection successfuly created to Orcale Database')
    	return conn


	def postgresDBconnection(user,password,host,port_pos,database_name):
    	engine = create_engine('postgresql://{}:{}@{}:{}/{}'.format(user,password,host,port_pos,database_name))
    	print('Connection successfuly created to Postgresql Database')
    	return engine


	def TableDetails(table_name_of_orcle,table_name_use_to_save_in):
    	df_ora = pd.read_sql('SELECT * FROM {}'.format(table_name_of_orcle), con=oracle_DB_connection(host_name,port,service_name,user_name,password_orc))
    	df_ora = df_ora.to_sql(table_name_use_to_save_in, postgres_DB_connection(user,password,host,port_pos,database_name), index = False, if_exists = 'append', chunksize=1000)
    	trasfer_details = 'Table secessfully copy to postgresql Database'
    	return trasfer_details


	def GettablewithSQL(query,table_name_use_to_save_in):
    	df_ora = pd.read_sql(query, con=oracle_DB_connection(host_name,port,service_name,user_name,password_orc))
    	df_ora = df_ora.to_sql(table_name_use_to_save_in, postgres_DB_connection(user,password,host,port_pos,database_name), index = False, if_exists = 'append', chunksize=1000)
    	trasfer_details = 'Table secessfully copy to postgresql Database'
    	return trasfer_details


#gettablewithSQL('SELECT * FROM employees','TEST')


#You can use upper program with following specification

#oracle_DB_connection(host_name,port,service_name,user_name,password_orc)
#postgres_DB_connection(user,password,host,port_pos,database_name)
#table_details(table_name_of_orcle,table_name_use_to_save_in)
#copytable_orcpsg_getlog()
#gettablewithSQL(query,table_name_use_to_save_in) / eg:- gettablewithSQL('SELECT * FROM employees','TEST')
