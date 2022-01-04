import telegram_send
import requests
import re
import yaml



def load_urls(links_path):
	with open(links_path) as f:
		data = yaml.load(f,Loader=yaml.FullLoader)
	return data

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


def get_current_record(tuple_location,link_location,name_location,pages,empty_page,url):
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
		all_res=requests.get(url).text

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

def format_message(dictionary):
	message_list=[]
	for element in dictionary:
		message="New update at {}\n\n[+]: {}".format(dictionary[element],element)
		message_list.append(message)
	return message_list

if __name__ == '__main__':
	urls = load_urls('links.yaml')
	for url in urls:
		tuple_location,link_location,name_location,pages,empty_page,report_location=load_config(urls[url])	
		old_record=get_old_record(report_location)
		current_record=get_current_record(tuple_location,link_location,name_location,pages,empty_page,url)
		diff = { index : current_record[index] for index in set(current_record) - set(old_record) }

		if(len(diff)!=0):
			print(diff)
			# message_list=format_message(diff)
			# telegram_send.send(messages=message_list)
			write_yaml(report_location,current_record)
