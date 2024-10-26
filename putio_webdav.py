#installed as "putio_downloader.service"
#sudo systemctl restart putio_downloader.service
import easywebdav
#from urllib.request import build_opener, Request, ProxyHandler, HTTPSHandler

import os
import sys
import time
from datetime import datetime
root_download_folder = "/home/joshgraff/media"
remote_root_directory = "/JPG/Box"
watch_folders = ['tv','movies','applications','music']
permissions_mask = 0o755
min_file_size = 20
scan_delay_time = 60
download_failures = 0
max_download_retries = 5
delete_after_download = True


def download_recurse(webdav:easywebdav, dir_name:str,root_download_folder:str):
    download_failures = 0
#    print(dir_name)
    for file in webdav.ls(dir_name):
        if file.name == dir_name:
            continue
 #       print(file)
        sys.stdout.flush()
        if file.name[-1] == "/":
            download_recurse(webdav,file.name,root_download_folder)
        else:
            if file.size > min_file_size:
                # print("exists: ",webdav.exists(file.name))          #print for the log
                # sys.stdout.flush()
                download_failures = download_failures + 1             #we count up for failures.
                filename = file.name.split("/")[-1]                 #get the name of the file
                local_dir_name = root_download_folder+dir_name.replace(remote_root_directory,"")
                if not os.path.exists(local_dir_name):#if we're making a directory
  #                  print("new dir: ",local_dir_name)
                    os.makedirs(local_dir_name)
                    os.chmod(local_dir_name,permissions_mask)
                now = datetime.now()
                dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
                print("Downloading ", file.name," at: ",dt_string)
                webdav.download(file.name,local_dir_name+filename) # download it into the right directory
                os.chmod(local_dir_name+filename,permissions_mask)
                local_file_size = os.path.getsize(local_dir_name+filename) #validate that the sizes match? Maybe do a checksum someday?
                if file.size == local_file_size:
                    download_failures = 0
                if not download_failures and delete_after_download: #download_failures is 0 on successs
                    webdav.delete(file.name)
    return download_failures



webdav = easywebdav.connect('webdav.put.io',username='torchwood899',password='putio455',protocol='https')
while webdav:
#    print("success:",webdav)
#    print(webdav.ls('/JPG/Box'))
    sys.stdout.flush()
    for dir in watch_folders:
        download_failures = download_recurse(webdav, "/JPG/Box/"+dir,root_download_folder)
    if download_failures > max_download_retries:
        break
    time.sleep(scan_delay_time)
