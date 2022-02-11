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
		host=config['host']
		tuple_location=config['tuple_location']
		link_location=config['link_location']
		name_location=config['name_location']
		
		pages=config['pages']
		empty_page=config['empty_page']

		report_location=config['report_location']
		api_link=config['api_link']
		description=config['description']

	return host,tuple_location,link_location,name_location,pages,empty_page,report_location,api_link,description


def get_current_record(tuple_location,link_location,name_location,pages,empty_page,url,api_link,description):
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
			link=re.findall(link_location,_tuple)
			name=re.findall(name_location,_tuple)
			records.update(dict(zip(name,link)))
	else:
		all_res = session.get(api_link).json()
		all_tuples=all_res[tuple_location]


		for _tuple in all_tuples:
			_description=_tuple[description]
			if(_description==None): _description="Pending..."
			name=_tuple[name_location]
			records[name]=_description

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
		link = dictionary[element] if 'https://' in dictionary[element] else host+dictionary[element]
		message="New update at {}\n\n[+]: {}\n\n[+]: {}".format(link,element)
		message_list.append(message)
	return message_list
	

if __name__ == '__main__':
	urls = load_urls('resources/links.yaml')
	for url in urls:
		host,tuple_location,link_location,name_location,pages,empty_page,report_location,api_link,description=load_config(urls[url])	
		old_record=get_old_record(report_location)
		current_record=get_current_record(tuple_location,link_location,name_location,pages,empty_page,url,api_link,description)
		diff = { index : current_record[index] for index in set(current_record) - set(old_record) }

		if(len(diff)!=0):
			message_list=format_message(host,diff)
			telegram_send.send(messages=message_list)
			write_yaml(report_location,current_record)
