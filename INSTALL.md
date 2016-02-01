#Installation

For manual installation on Ubuntu 14.04 (AWS EC2) and is not meant for any real operational use.

Start with the basic python installs:

```
sudo apt-get update
sudo apt-get install python-pip python-dev nginx git
sudo pip install virtualenv
```

Clone the repo:

```
git clone https://github.com/roomthily/esip_badger.git
```

Set up the virtualenv:

```
cd esip_badger
virtualenv badger_env
source badger_env/bin/activate
```

Install flask and gunicorn:

```
pip install gunicorn flask svgwrite
```

Test the app in gunicorn locally if you like:

```
gunicorn --bind 0.0.0.0:8000 badger:app
```

And exit the virtualenv:

```
deactivate
```

Add a configuration for upstart:

```
sudo nano /etc/init/badger.conf
```

with this configuration:

```
description "gunicorn app server for esip badger"

start on runlevel [2345]
stop on runlevel [!2345]

respawn
setuid ubuntu
setgid www-data        

env PATH=/home/ubuntu/esip_badger/badger_env/bin
chdir /home/ubuntu/esip_badger
exec gunicorn -b 0.0.0.0:8000 --workers 3 --bind unix:esip_badger.sock -m 007 badger:app
```

And now the config for nginx:

```
sudo nano /etc/nginx/sites-available/esip_badger
```

with this configuration:

```
server {
        listen 80;
        server_name {Public IP | host};

        location / {
                include proxy_params;
                proxy_pass http://unix:/home/ubuntu/esip_badger/esip_badger.sock;
        }
}
```

Set up a symlink for sites-enabled:

```
sudo ln -s /etc/nginx/sites-available/esip_badger /etc/nginx/sites-enabled
```

For restarting the gunicorn service and nginx:

```
sudo restart badger
sudo service nginx restart
```


