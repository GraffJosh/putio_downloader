# putio_downloader
Auto downloader for putio (and I guess other similar sites?)

Update putio_downloader.py to reference the correct download folder.

A few things need to change for this to work.
`pip install easywebdav`
Use `pip show easywebdav` to find the folder it's stored in. 
add `allow_redirects=True` to client.py on line 97.

Move putio_downloader.service to /etc/systemd/system/putio_downloader.service
Edit this file to update user, python path, and directory to the downloader script. 
