#!/usr/bin/python3
# import telegram_send
import requests
import re
import yaml
#import os

#os.chdir('/home/antqt/Security-Alert/')
def load_urls(links_path):
	with open(links_path) as f:
		data = yaml.load(f,Loader=yaml.FullLoader)
	return data

def load_config(yaml_path):
	with open(yaml_path) as f:
		config = yaml.load(f,Loader=yaml.FullLoader)
		host=config['host']
		tuple_location=config['tuple_location']

		data_location=config['data_location']
		
		pages=config['pages']
		empty_page=config['empty_page']

		report_location=config['report_location']
		api_link=config['api_link']

	return host,tuple_location,data_location,pages,empty_page,report_location,api_link


def get_current_record(tuple_location,data_location,pages,empty_page,url,api_link):
	page=1
	all_res=''
	records={}

	session = requests.session()

	if(api_link==""):
		if(pages!=''):
			while (True):
				res = session.get(url+pages+str(page))
				if(empty_page in res.text): break
				all_res+=res.text
				page+=1
		else:
			all_res=session.get(url).text

		all_tuples=re.findall(tuple_location,all_res)


		for _tuple in all_tuples:
			data=[]
			data_on_1_line={}
			for _data_location in data_location:
				data.append(re.findall(data_location[_data_location],_tuple)[0])
			data_on_1_line[data[0]]=data[1:]
			records.update(data_on_1_line)
			
				
	else:
		all_res = session.get(api_link).json()
		all_tuples=all_res[tuple_location]

		for _tuple in all_tuples:
			data_list=[]
			data_on_1_line={}
			for _data_location in data_location:
				data_element ="" if data_location[_data_location] == "" else _tuple[data_location[_data_location]]
				data= "Pending" if data_element == None else data_element
				data_list.append(data)
			data_on_1_line[data_list[0]]=data_list[1:]
			records.update(data_on_1_line)

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
		yaml.dump(content, file)

def format_message(host,dictionary):
	message_list=[]
	for element in dictionary:
		link = dictionary[element][0] if 'https://' in dictionary[element][0] else host+dictionary[element][0]
		message="New update at {}\n\n[+]: {}".format(link,element)
		for _element in dictionary[element][1:]:
			message+='\n\n[+]: {}'.format(_element)
		message_list.append(message)
	return message_list
	

if __name__ == '__main__':
	urls = load_urls('resources/links.yaml')
	for url in urls:
		host,tuple_location,data_location,pages,empty_page,report_location,api_link=load_config(urls[url])	
		old_record=get_old_record(report_location)
		current_record=get_current_record(tuple_location,data_location,pages,empty_page,url,api_link)
		diff = { index : current_record[index] for index in set(current_record) - set(old_record) }

		if(len(diff)!=0):
			message_list=format_message(host,diff)
			# telegram_send.send(messages=message_list)
			write_yaml(report_location,current_record)

