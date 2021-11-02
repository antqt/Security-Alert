import telegram_send
import requests
import re
import yaml




# url= 'https://github.com/NotCl0ne/school-project/pulls'
url='https://github.com/projectdiscovery/nuclei-templates/pulls'

def load_config(yaml_path):
	with open(yaml_path) as f:
		config = yaml.load(f,Loader=yaml.FullLoader)
		tuple_location=config['tuple_location']
		link_location=config['link_location']
		name_location=config['name_location']
		
		pages=config['pages']
		empty_page=config['empty_page']

		report_location=config['report_location']
	return tuple_location,link_location,name_location,pages,empty_page,report_location


def get_current_record(tuple_location,link_location,name_location,pages,empty_page):
	page=1
	all_res=''

	session = requests.session()
	if(pages!=''):
		while (True):
			res = requests.get(url+pages+str(page))
			if(empty_page in res.text): break
			all_res+=res.text
			page+=1
	else:
		all_res=requests.get(url)

	all_tuples=re.findall(tuple_location,all_res)


	records={}
	for _tuple in all_tuples:
		link=re.findall(link_location,_tuple)
		name=re.findall(name_location,_tuple)
		records.update(dict(zip(name,link)))

	return records

def get_old_record(location):
	try:
		with open(location) as f:
			records = yaml.load(f,Loader=yaml.FullLoader)
	except:
		print("Can't find old records!")
		records={}

	return records

def write_yaml(destination,content):
	with open(destination, 'w') as file:
		documents = yaml.dump(content, file)

if __name__ == '__main__':
	
	tuple_location,link_location,name_location,pages,empty_page,report_location=load_config('github.yaml')
	
	old_record=get_old_record(report_location)
	
	current_record=get_current_record(tuple_location,link_location,name_location,pages,empty_page)

	diff = { index : current_record[index] for index in set(current_record) - set(old_record) }

	if(len(diff)!=0):
		telegram_send.send(messages=diff)
		write_yaml(report_location,current_record)
