GotchaTwitter
======

Example
------
    input = [<screen_name_1>, <screen_name_2>]
    access_token = <pushbullet_token>
    output_fp = <filepath you want to save>
    with GotchaTwitter('timeline', input, output_fp) as gt:
	    gt = gt.set_output(save_mode='w', has_header=True) \
		    .set_notifier('pushbullet', access_token=access_token)
	    gt.crawl()

Notifier Setting
------
### PushBullet
1. Register a [PushBullet](https://www.pushbullet.com/) account and create an access token in your account setting.
2. Download Pushbullet app on your device (iOS tested).

Install lxml on Amazon Linux AMI (2016.03.3)  
------
    sudo yum install libxml2-devel libxslt-devel python-devel gcc
    sudo pip install --upgrade setuptools
    sudo /usr/local/bin/easy_install lxml
