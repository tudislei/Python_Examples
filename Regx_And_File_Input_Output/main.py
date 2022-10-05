import os, traceback, json, re
from typing import Dict, List


def read_search_list(import_file_name: str) -> List[Dict[str,str]]:
	"""
	從 .sql 語句中, 讀取需要搜索的表格名, 例如 

	425598  CREATE TABLE "DATABASE_001"."TABLE_001"  (
	425599: 		  "INSTNO" VARCHAR(10 OCTETS) NOT NULL , 
	425600  		  "JNLNO" VARCHAR(20 OCTETS) NOT NULL , 

	425598  CREATE TABLE "DATABASE_001"."TABLE_002"  (
	425599: 		  "INSTNO" VARCHAR(10 OCTETS) NOT NULL , 
	425600  		  "JNLNO" VARCHAR(20 OCTETS) NOT NULL , 

	便會返回結果 [
		{"database":"DATABASE_001","table":"TABLE_001"},
		{"database":"DATABASE_001","table":"TABLE_002"}
	]
	"""

	result = []
	check_duplicated_dict = {} # 去除重複的 table name
	try:
		full_file_name = os.path.join(os.getcwd(),import_file_name)
		with open( full_file_name, encoding='UTF-8-sig') as f:
			lines = f.readlines()
			found_table_name_in_this_block = False
			one_block = ''
			not_found_index = 0
			for line_index, line in enumerate(lines):
				if len(line) == 1: # 如果是純換行
					if not found_table_name_in_this_block:
						# 在一個代碼塊中找不到 表格表, 就要報告出來, 檢查是否需要擴大搜索範圍
						not_found_index += 1
						print(f"""								
								NOT FOUND {not_found_index} !!!!
								{one_block}
								-----------------
						""")
					one_block = ''
					found_table_name_in_this_block = False 
				one_block += line
				line = line.upper()
				if 'CREATE TABLE' in line or 'COMMENT ON TABLE' in line:
					found_table_name_in_this_block = True
					temp_line = line.split('"')
					database = temp_line[-4].strip()
					table = temp_line[-2].strip()
					key = database + ' | ' + table
					if key not in check_duplicated_dict:
						result.append({
							"database":database,
							"table":table
						})
					check_duplicated_dict[key] = True

	except Exception as error:
		print( traceback.format_exc() )

	#print(json.dumps(result, indent = 3, ensure_ascii=False ))
	return result


def read_file(import_file_name: str) -> str:
	"""
	讀取已導出好的完整 chain job, 然後便可以直接在其中搜索
	"""
	result = ''
	try:
		full_file_name = os.path.join(os.getcwd(),import_file_name)
		with open(full_file_name, encoding='UTF-8-sig') as f:
			lines = f.readlines()
			for line in lines:
				result += line				
			#with open(  os.path.join(os.getcwd(), f'test_output_{import_file_name}.txt') , "w", encoding="utf-8-sig") as temp:
			#temp.write(result)
	except Exception as error:
		print( traceback.format_exc() )
	return result


def main():
	"""
	假設本地數據庫有一批排定運行的程序, 每天從遠端數據庫取數
	現在得知, 遠端數據庫有一批表格字段有更新, 但只有所有表格導出的 DDL語句
	以及 所有可能有關的字段名，但並沒有仔細的 更新記錄
	
	所以本程序可以用來在 DDL語中句提取表格名, 然後在導出的排定程序中搜索是否曾出現過這些表格名
	再進行下一步的檢查
	"""

	to_search_string = []
	to_search_string += read_search_list('to_search_list.sql')
	print( f' len(to_search_string) = {len(to_search_string)}' )
	
	full_result_string = ''
	full_result_string += read_file('adas_procedure_schedule.sql')
	full_result_string += read_file('bocs_procedure_schedule.sql')
	full_result_string = full_result_string.upper()

	for search_object in to_search_string:
		database = search_object.get("database")
		table = search_object.get("table")		
		reg_pattern='[^0-9a-zA-Z_\-]+' + table + '[^0-9a-zA-Z_\-.]+' # 前後如果是這些字符, 就不是要找的表格名
		reg_result = re.findall(reg_pattern, full_result_string)
		appear_times = len(reg_result)
		if appear_times > 0 :
			print( f'數據庫名 {database} . 表名 {table} 在三條 chain 中出現 {appear_times} 次')
			times_with_at_symbol = full_result_string.count(table + '@') # 表名接at符號代表直接從遠端數據庫這張表中取數
			if times_with_at_symbol > 0 :
				print( f'	{table}@ 出現 {times_with_at_symbol} 次')				


if __name__ == '__main__':
	main()