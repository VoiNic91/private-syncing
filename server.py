from subprocess import Popen, PIPE
from time import sleep
import dropbox

ip_file='/ip.txt'
dbx = dropbox.Dropbox('vK3D7j1Xny8AAAAAAAAPzlnZhnrxVLWwHT1WIi0CBr_06RCap_qYYE7NQsGr6KDm')

def dropbox_update_ip(new_ip):
	dbx.files_upload(new_ip, ip_file)

def get_ext_ip():
	ext_ip = ''
	p = Popen(["dig", "+short", "myip.opendns.com", "@resolver1.opendns.com"], stdout=PIPE, stderr=PIPE)
	
	if p.wait() == 0:
		ext_ip = p.stdout.read()
	else:
		print p.stderr.read()+' '+str(p.poll())
		
	return ext_ip.strip()
	


def main():
		
	sleep_time_seconds = 30
	ext_ip = '000'
	while True:
		print "Sleep for "+str(sleep_time_seconds)+" seconds"
		sleep(sleep_time_seconds)
		
		bt = bytearray(ext_ip)
		bt[0]+=1
		ext_ip = str(bt)

		print "Ip has changed from "+old_ext_ip+" to "+ext_ip
		dropbox_update_ip(ext_ip)
			
	
if __name__ == "__main__":
        main()
