# Djangosite template

This is a Django Template for [CapRover](https://caprover.com/docs/get-started.html) (Docker) - deployment & web server manager with Nginx and Let's Encrypt.

### Prerequisites:

- A VPS server.
- A domain.
- npm installed
- Python 3.
- Github or similar.

## Table of contents
- [Import repository](#import-repository)
- [Set up VPS](#Set_up_VPS)
  * [1. Order a VPS](#Order_a_VPS)
  * [2. Configure passwordless login](#configure-passwordless-login)
  * [Install Docker](#install-docker)
  * [Configure Firewall](#configure-firewall)
- [Caprover Instalation](#caprover-instalation)
  * [1 Install CapRover ](#1-install-caprover)
  * [2 Connect Root Domain](#2-connect-root-domain)
  * [3 Install CapRover CLI](#3-install-caprover-cli)
- [Create Django App](#create-django-app)
  * [Create Persistent Directories](#create-persistent-directories)
  * [Add environmental variables](#add-environmental-variables)
  * [Add custom NGINX config](#add-custom-nginx-config)
- [Prepare app for deployment](#prepare-app-for-deployment)
  * [Create virtual enviroment](#create-virtual-enviroment)
  * [Clone project from git](#clone-project-from-git)
  * [Captain file (Docker)](#captain-file-docker)
  * [Create settings_dev.py](#Create-dev-settings)
  * [Make translation files](#make-translation-files)
  * [Test your site](#test-your-site)
  * [Change static files](#Change-Static-Files)
  * [Commit changes](#commit-changes)
- [Deploy to CapRover](#deploy-to-caprover)
  * [Create Superuser](#create-superuser)
  * [Login to Django Admin](#Login-to-Django-Admin)

## Import repository <a name="import-repository"></a>

Create a new github/gitlab/bitbucket repository for your project.
Lets name it **mydomain** if you plan to run a website with **mydomain.tld** domain.

Import this repository https://github.com/osxisl/django-caprover.

> (Optional) To simplify you copy&past during this tutorial, change mydomain.com and mydomain in this ```README.md``` file right in GitHub editor to your actual domain and app name.
In GitHub editor activate Find and Replace by pressing *Command+Option+F*(Mac OS) or *Ctrl+Alt+F*(other OS).
Write ```mydomain.com``` and pres "Return/Enter" then write ```youractualdomain.tld``` and hit "Return/Enter". Then press "All" button.
Repeate this procedure replacing ```mydomain``` for ```youractualdomain``` and ```YOUR_SERVER_IP``` to your VPS IP ardesss.

*Now you can use your version of ```README.md``` as a simple copy & paste tutorial.*

## Set up VPS <a name="Set_up_VPS"></a>

*The easiest way to start is to create [CapRover Droplet](https://marketplace.digitalocean.com/apps/caprover) via DigitalOcean one-click app -[great tutorial on Youtube](https://www.youtube.com/watch?v=pIF5B-D8jD4).*

Another way is to get any VPS with Ubuntu 18.04 and set up CapRover manually.

### Order a VPS (for example on [Contabo](https://contabo.com/en/vps/vps-s-ssd/))<a name="Order_a_VPS"></a>

### Configure [passwordless login](https://help.dreamhost.com/hc/en-us/articles/216499537-How-to-configure-passwordless-login-in-Mac-OS-X-and-Linux):<a name="configure-passwordless-login"></a>

Add VPS server IP to host file by adding a new line to your /etc/hosts file:
```
sudo nano /etc/hosts
```
Add following line  (127.0.0.1 replace with your VPS IP):
```
YOUR_SERVER_IP   djangovps
```
Go to your home dir:
```
cd
```
Generate ssh key:
```
ssh-keygen -t rsa
```
Add public key part to the VPS:
```
cat ~/.ssh/id_rsa.pub | ssh root@djangovps "mkdir ~/.ssh; cat >> ~/.ssh/authorized_keys"
```
Enter root password.

> If password login to root is blocked, then login to server with available user and enter: ```sudo su``` then ```nano /root/.ssh/authorized_keys``` and paste there your pub key - run ```cat ~/.ssh/id_rsa.pub``` on your local machine to find it.

Now connect to VPS by simply typing:
```
ssh root@djangovps
```
Create new user:
```
adduser djangouser
```
Give this user sudo rights:
```
usermod -aG sudo djangouser
```
Edit /etc/ssh/sshd_config (on server)
```
sudo nano /etc/ssh/sshd_config
```
Change PermitRootLogin value to:
```
PermitRootLogin prohibit-password
```
Restart the ssh server
```
sudo service ssh restart
```
On the client. You should now be able to ssh in with your key without a password and you should not be able to ssh in as **root** user without a key:
```
ssh root@djangovps
```

###  Install Docker - [ Fresh official instruction](https://docs.docker.com/engine/install/ubuntu/)<a name="install-docker"></a>
```
sudo apt-get update &&
sudo apt-get install \
    apt-transport-https \
    ca-certificates \
    curl \
    gnupg-agent \
    software-properties-common
```
```
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
```
```
sudo add-apt-repository \
   "deb [arch=amd64] https://download.docker.com/linux/ubuntu \
   $(lsb_release -cs) \
   stable"
```
```
sudo apt-get update && sudo apt-get install docker-ce docker-ce-cli containerd.io
```
Verify that Docker Engine is installed correctly
```
sudo docker run hello-world
```

### Configure Firewall<a name="configure-firewall"></a>
```
ufw allow 80,443,3000,996,7946,4789,2377/tcp; ufw allow 7946,4789,2377/udp;
```

## Caprover instalation<a name="caprover-instalation"></a>

### 1 Install CapRover - [official instruction](https://caprover.com/docs/get-started.html#step-1-caprover-installation)<a name="1-install-caprover"></a>

```
docker run -p 80:80 -p 443:443 -p 3000:3000 -v /var/run/docker.sock:/var/run/docker.sock -v /captain:/captain caprover/caprover
```

You will see a bunch of outputs on your screen. Once the CapRover is initialized, you can visit ```http://YOUR_SERVER_IP:3000``` in your browser and login to CapRover using the default password ```captain42```. You can change your password later. However, do not make any changes in the dashboard. We'll use the command line tool to setup the server.

### 2 Connect root domain<a name="2-connect-root-domain"></a>
Let's say you own mydomain.com. You can set \*.test.mydomain.com as an A-record in your DNS settings to point to the IP address of the server where you installed CapRover. Note that it can take several hours for this change to take into effect. It will show up like this in your DNS configs:

- *TYPE*: A record
- *HOST*: \*.test (or any other)
- *POINTS TO*: YOUR_SERVER_IP
- *TTL*: (doesn't really matter)

To confirm, go to [https://mxtoolbox.com/DNSLookup.aspx](https://mxtoolbox.com/DNSLookup.aspx) and enter ```randomthing123.test.mydomain.com``` and check if IP address resolves to the IP you set in your DNS. Note that ```randomthing123``` is needed because you set a wildcard entry in your DNS by setting ```\*.test``` as your host, not ```test```.

### 3 Install CapRover CLI (on local machine)<a name="3-install-caprover-cli"></a>
Assuming you have npm installed on your local machine (e.g., your laptop), simply run (add sudo if needed):
```
npm install -g caprover
```
Then, run
```
caprover serversetup
```
Follow the steps and login to your CapRover instance. When prompted to enter the root domain, enter ```test.mydomain.com``` assuming that you set ```\*.test.mydomain.com``` to point to your IP address in step #2. Now you can access your CapRover from ```captain.test.mydomain.com```

## Create Django app<a name="create-django-app"></a>

You can repeat this step for each django app you want to add to CapRover.

| Type     |  Host |      Value     |    TTL    |
| ---------|:-----:|:--------------:|----------:|
| A Record |   *   | YOUR_SERVER_IP | Automatic |
| A Record |   @   | YOUR_SERVER_IP | Automatic |
| A Record |   www | YOUR_SERVER_IP | Automatic |

1. Connect your domain ```mydomain.com``` to you server by adding three A records like in a table above.
2. Go to ```https://captain.test.mydomain.com/#/apps```
Write a name for your app (I'll use **```mydomain```** as an app name) then select **"Has Persistent Data"** checkbox and click *"Create New App"* button.
 We need **"Has Persistent Data"** selected to serve static and media files directly from our server.
3. Go to mydomain app **HTTP Setiings** and press *"Connect New Domain"*, where you can put ```mydomain.com```
4. Enable HTTPS for this domain. And then select checkbox *"Force HTTPS by redirecting all HTTP traffic to HTTPS"*
5. Set **Container HTTP Port** to 8001

> If it's not the first app on the same VPS, use another port like 8002, 8003, etc.

### Create Persistent Directories for your app<a name="create-persistent-directories"></a>

Login to server:
```
ssh root@djangovps
```
Go to nginx shared directory and create your app directory (Change *mydomain* for your app name) and directories to store your static, media and db(if you plan to use sqlite) files persistent:
```
cd /captain/data/nginx-shared/ && mkdir mydomain && cd mydomain && mkdir static media db
```

Go to mydomain App Configs ```https://captain.test.mydomain.com/#/apps/details/mydomain``` and add three Persistent Directories by pressing **"Add Persistent Directory"** and **"Set specific host path"** for each:
>Change *mydomain* for your app name.
1. Path in App: ```/usr/src/app/staticfiles``` Path on Host: ```/captain/data/nginx-shared/mydomain/static```
2. Path in App: ```/usr/src/app/media``` Path on Host: ```/captain/data/nginx-shared/mydomain/media```
3. Path in App: ```/usr/src/app/db``` Path on Host: ```/captain/data/nginx-shared/mydomain/db```

### Add environmental variables
On the top of the same page add Environmental Variables in Bulk mode:
```
CAPROVER=True
CR_SECRET_KEY=YOUR_DJANGO_SECRET_KEY
CR_HOSTS=mydomain.com
CR_USESQLITE=True
WEB_CONCURRENCY=4
CR_DB_NAME=mydomain
CR_DB_USER=mydomainadmin
CR_DB_PASSWORD=YOUR_DB_PASSWORD
CR_DB_HOST=srv-captain--mydomain-db
CR_DB_PORT=5432

```
> Add CR_DB_NAME, CR_DB_USER, CR_DB_PASSWORD, CR_DB_HOST and CR_DB_PORT, if you plan to use PostgreSQL instead of Sqlite DB. You can easily install PostgreSQL as oneclick App in Caprover.

### Add custom NGINX config
Go to mydomain app **HTTP Setiings** and press **Edit Default NGINX Configuration button**. Then add these line at the beginning of the file:

> Change *mydomain.com* for your app domain.

```
# CUSTOM SETTINGS START
server {
    server_name www.mydomain.com;
    return 301 $scheme://mydomain.com$request_uri;
}

# Expires map
map $sent_http_content_type $expires {
    default                    off;
    text/html                  epoch;
    text/css                   max;
    application/javascript     max;
    ~image/                    max;
}
# CUSTOM SETTINGS END
```
Then after ```set $upstream http://<%-s.localDomain%>:<%-s.containerHttpPort%>;``` insert:
```
        # CUSTOM SETTINGS START

        gzip  on;
        gzip_comp_level 6;
        gzip_types 
            text/plain
            text/css
            text/js
            text/xml
            text/javascript
            application/javascript
            application/x-javascript
            application/json
            application/xml
            application/xml+rss
            application/rss+xml
            image/svg+xml;
        gzip_vary on;
        gzip_disable "msie6";

        # CUSTOM SETTINGS END
```
And After:
```
# Used by Lets Encrypt
        location /.well-known/acme-challenge/ {
            root <%-s.staticWebRoot%>;
        }
```
Insert:
> change *mydomain* for your app name you used when created persistance folders.
```
        # CUSTOM SETTINGS START

        # Used for STATIC FILES
        location /static/ {
            root /nginx-shared/mydomain;
        }

        # Used for MEDIA FILES
        location /media/ {
            root /nginx-shared/mydomain;
        }

        # Used for txt and other webroot FILES
        location  ~ ^/ads.txt$ {
            root /nginx-shared/mydomain/static;
        }

        location  ~ ^/robots.txt$ {
            root /nginx-shared/mydomain/static;
        }

        location  ~ ^/site.webmanifest$ {
            root /nginx-shared/mydomain/static;
        }

        location  ~ ^/favicon.ico$ {
            root /nginx-shared/mydomain/static;
        }

        location  ~ ^/favicon-16x16.png$ {
            root /nginx-shared/mydomain/static;
        }

        location  ~ ^/favicon-32x32.png$ {
            root /nginx-shared/mydomain/static;
        }

        location  ~ ^/apple-touch-icon.png$ {
            root /nginx-shared/mydomain/static;
        }

        location  ~ ^/android-chrome-192x192.png$ {
            root /nginx-shared/mydomain/static;
        }

        location  ~ ^/android-chrome-512x512.png$ {
            root /nginx-shared/mydomain/static;
        }

        # Used for sitemap FILES
        location ~ ^/sitemap.xml$ {
            root /nginx-shared/mydomain/static/xml;
        }

        location ~ ^/sitemap_[a-z0-9-]+.xml$ {
            root /nginx-shared/mydomain/static/xml;
        }

        location ~ ^/sitemap_[a-z0-9-]+.xml.gz$ {
            root /nginx-shared/mydomain/static/xml;
        }

        location ~ ^/[a-z0-9-]+.xml$ {
            root /nginx-shared/mydomain/static/xml;
        }

        location ~ ^/[a-z0-9-]+.xml.gz$ {
            root /nginx-shared/mydomain/static/xml;
        }

        expires $expires;
        # CUSTOM SETTINGS END
```
Save the config.

## Prepare app for deployment

### Create virtual enviroment
In terminal go to your development folder and Create & Activate Virtual Enviroment:
```
python3 -m venv mydomainenv && source mydomainenv/bin/activate
```

### Clone project from git
After import clone your new repo to your local machine:
```
git clone https://github.com/<yourusername>/mydomain.git
```
cd into project folder
```
cd mydomain && pip install -r requirements.txt
```
### Open mydomain project in your code editor.


### Edit Captain file (Docker)<a name="captain-file-docker"></a>
Change 8001 port in **captain-definition** and in **/utils/run.sh** file, if you plan to set a different port for your CapRover app.

### Create dev settings file ```settings_dev.py``` in */djangosite* directory near the *settings.py* file.<a name="Create-dev-settings"></a>

```
import os
from pathlib import Path
from .settings import BASE_DIR

SECRET_KEY = 'YOUR_DJANGO_SECRET_KEY'

DEBUG = True

ALLOWED_HOSTS = ['127.0.0.1',]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': str(BASE_DIR / 'db/db.sqlite3'),
    }
}
```

### In */homepage* directory in the ```views.py``` file change *title* and *title* for each view.

### Make translation files
```
django-admin makemessages -l ko -l nb -l nl -l pl -l pt -l sv -l tr -l vi -l zh_Hans -l ms -l ja -l it -l id -l hi -l he -l fr -l es -l el -l de -l da -l ar -l uk -l ru
```

### Test your site
Run migration:
```
mkdir db && python manage.py migrate
```
create dev superuser:
```
python manage.py createsuperuser
```
```
python manage.py runserver
```
Go to [http://127.0.0.1:8000/](http://127.0.0.1:8000/) and verify that everything works. Then login in Admin http://127.0.0.1:8000/admin/ and go to http://127.0.0.1:8000/rosetta/files/project/ to translate nedded languages.

> You can remove some languages in *settings.py* file.

### Change static files: favicon.ico, apple-touch-icon.png, Template, etc<a name="Change-Static-Files"></a>

Change site name and short_name in site.webmanifest file 
```
/homepage/static/site.webmanifest
```

Change Favicon:
```
/homepage/static/favicon.ico
/homepage/static/favicon-16x16.png  
/homepage/static/favicon-32x32.png
/homepage/static/apple-touch-icon.png
/homepage/static/android-chrome-192x192.png
/homepage/static/android-chrome-512x512.png
```
And check these files:
```
/homepage/static/img/homapage.png - social sharing image
/homepage/static/xml/sitemap.xml
/homepage/static/robots.txt
/homepage/static/ads.txt - if you plan to use Google Adsense
```

### Commit changes
```
git add .
git commit -m "initial changes"
git push
```

## Deploy to CapRover
```
caprover deploy
```

### Create Superuser
On the server run a code below, replacing *mydomain* with your app name:

```
docker exec -it $(docker ps --filter name=srv-captain--mydomain -q) python manage.py createsuperuser
```

### Login to Django Admin and change SITE name and link<a name="Login-to-Django-Admin"></a>
...

That's all.
Now you can instantly deploy after pushing new changes to git by:
```
caprover deploy --default
```


## Other improvements (TBD)

### Inline CSS and JS
https://gist.github.com/PaulKinlan/6284142
Add bookmark with js code instead of url:
```
javascript:void function () { (function () { if (typeof window.getMatchedCSSRules !== 'function') { window.getMatchedCSSRules = function (element) { var i, len, matching = [], sheets = document.styleSheets; function loopRules(rules) { var i, len, rule; for (i = 0, len = rules.length; i < len; i++) { rule = rules[i]; if (rule instanceof CSSMediaRule) { if (window.matchMedia(rule.conditionText).matches) { if(typeof rule.cssRules == 'object' && rule.cssRules.length > 0) { loopRules(rule.cssRules); } } } else if (rule instanceof CSSStyleRule) { if (element.matches(rule.selectorText)) { matching.push(rule); } } } }; for (i = 0, len = sheets.length; i < len; i++) { try { if(typeof sheets[i].cssRules == 'object' && sheets[i].cssRules.length > 0) { loopRules(sheets[i].cssRules); } } catch (err){ } } return matching; } } var e = function (e, t, n) { var r = n || {}, o = {}, i = function (e) { try { if(typeof o[e.selectorText] == 'undefined') { o[e.selectorText] = {}; } for (var t = e.style.cssText.split(/;(%3F![A-Za-z0-9])/), n = 0; n < t.length; n++) if (!!t[n] != !1) { var r = t[n].split(": "); r[0] = r[0].trim(), r[1] = r[1].trim(), o[e.selectorText][r[0]] = r[1] } } catch(err) { console.error('ERROR: in generating!! plz contact Dirk Persky'); } finally { console.warn('Scan Next Node'); } }, a = function () { for (var n = e.innerHeight, o = t.createTreeWalker(t, NodeFilter.SHOW_ELEMENT, function (e) { return NodeFilter.FILTER_ACCEPT }, !0); o.nextNode();) { var a = o.currentNode, c = a.getBoundingClientRect(); if (c.top < n || r.scanFullPage) { var l = e.getMatchedCSSRules(a); if (l) for (var f = 0; f < l.length; f++) i(l[f]) } } }; this.generateCSS = function () { var e = ""; for (var t in o) { e += t + " { "; for (var n in o[t]) e += n + ": " + o[t][n] + "; "; e += "}\n" } return e }, a() }, t = new e(window, document), n = t.generateCSS(); console.log(n) })() } ();
```
Open your website > inspector > Console, then open added bookmark, and critical css will be generated in Console.
