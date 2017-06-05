import pymssql

class db_connection(object):

	def __init__(self, database=None):

		self.__database = database
		self.__cnxn = self.__get_connection()


	def __get_connection(self):

		if self.__database == 'np':
			__cnxn = pymssql.connect(server='10.10.20.5', user='bi_agent', password='abcd-1234', as_dict=False)
		elif self.__database == 'azure':
			__cnxn = pymssql.connect(server='payeasy.database.windows.net', user='bi_agent@payeasy',
			                       database='PAYEASY_DATA', password='abcd-1234', as_dict=False)
		else:
			print('Please choose your database...')

		return __cnxn

	def do_query(self, query_string, data=None):

		cursor = self.__cnxn.cursor()

		if data is None:
			cursor.execute(query_string)
			self.__cnxn.commit()
			return cursor.fetchall()
		else:
			cursor.execute(query_string, data)
			self.__cnxn.commit()

	def do_commit(self):

		self.__cnxn.commit()

#
# if __name__ == '__main__':
# 	test = db_connection('np').do_query('select top 10 * from [MIS_OPEN].[dbo].[BI_GA_USERS_SEARCH_NULL] ')
#
# 	sql_stat = ("select distinct(區), count(區) from dbo.store_information "
# 	            "where (google電話 is null or google電話 = '查無google資料' ) and 區 = '新店區' group by 區")
#
# 	test1 = db_connection('azure').do_query(sql_stat)
# 	print(test)
# 	print('')
# 	print(test1)
