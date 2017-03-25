import dropbox
import sys

dbx = dropbox.Dropbox('vK3D7j1Xny8AAAAAAAAPzlnZhnrxVLWwHT1WIi0CBr_06RCap_qYYE7NQsGr6KDm')
ip_file='ip.txt'

def get_ext_ip():
	ip = ''
	
	try:
		md, res = dbx.files_download('/'+ip_file)
		ip = res.content
	except:
		print("Error:", sys.exc_info()[0])
	
	return ip


def main():
	ext_ip = get_ext_ip()
	
	if not ext_ip:
		print "Unable to get ip from Dropbox. Quitting"
		exit()
	
	print "Retrieved server's IP is "+ext_ip
	#TODO:have an initial API call to check server availability
	
	#TODO:have the polling in a separate thread
	
	res = dbx.files_list_folder('')
	while True:
		folder_result = dbx.files_list_folder_longpoll(res.cursor)
		
		if folder_result.changes is True:
			res = dbx.files_list_folder_continue(res.cursor)
			print "New changes: "
			for meta in res.entries:
				print meta.name
				if meta.name == ip_file:
					ext_ip = get_ext_ip()
					print ext_ip
				

if __name__ == "__main__":
        main()

