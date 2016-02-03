##Updating the service

This describes how to add new terms or, if other changes are necessary, how to deploy those changes to the EC2.

###Adding a new term

The term list is foung in badger.py in the `_badge_types` dictionary. To add a new term, just add a new dictionary element:

```
"drones": {"background": "#A1D3E4", "text": "Drones"},
```

where the first token (drones) is the URL-friendly short name, `background` is the right-side color, and `text` is the descriptive title appearing on the badge. Note that the membership badges are a different color.

The list of terms is also in the README so don't forget to update that list (see "Values for Collaboration Areas").

###Deploying the app

Make sure you have an AWS key (\*.pem file) and are able to `ssh` into the instance (generate a key pair associated with the instance, make sure the security group is updated to allow SSH from your IP). Make a note of the `Public DNS` value.

Commit the changes made to badger.py and the README.md and push the changes to the remote on Github. 

SSH into the EC2:

```
$ ssh -i "your_aws_key.pem" ubuntu@the_public_dns_string
```

Update the local code from git:

```
$ cd esip_badger
$ git pull
```

There's no build for this, but the server processes need to be reloaded.

```
$ sudo restart badger
$ sudo service nginx restart
```

And logout, you're good to go.


