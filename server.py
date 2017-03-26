from subprocess import Popen, PIPE
from time import sleep
import dropbox
import os

ip_file='/ip.txt'
dbx = None

def dropbox_init():
	global dbx

	key_file = open(os.path.expanduser("~")+"/.private-syncing/key.txt")
	key = key_file.read().strip()

	dbx = dropbox.Dropbox(key)


def dropbox_update_ip(new_ip):
        dbx.files_upload(new_ip, ip_file, mode=dropbox.files.WriteMode('overwrite', None))


def get_ext_ip():
	ext_ip = ''
	p = Popen(["dig", "+short", "myip.opendns.com", "@resolver1.opendns.com"], stdout=PIPE, stderr=PIPE)

	if p.wait() == 0:
		ext_ip = p.stdout.read()
	else:
		print p.stderr.read()+' '+str(p.poll())

	return ext_ip.strip()


def main():
	dropbox_init()

	old_ext_ip = ext_ip = get_ext_ip()
	sleep_time_seconds = 30

	if not ext_ip:
		print "Couldn't get the initial IP address. Check yur network connection"
		print "Exitting..."
		exit()

	print "Initial IP address is "+ext_ip
	dropbox_update_ip(ext_ip)


	while True:
		print "Sleep for "+str(sleep_time_seconds)+" seconds"
		sleep(sleep_time_seconds)
		
		ext_ip = get_ext_ip()
		if not ext_ip:
			print "failed to get external IP address. Will try again after next timeut"
		else:
			if(old_ext_ip != ext_ip):
				print time.strftime("%c")+" Ip has changed from "+old_ext_ip+" to "+ext_ip
				dropbox_update_ip(ext_ip)
				old_ext_ip = ext_ip
			else:
				print "IP is still the same. Continue"

if __name__ == "__main__":
        main()
