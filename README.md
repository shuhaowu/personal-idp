Personal IDP
============

Whoa. Your personal, private [Mozilla Persona IDP](https://developer.mozilla.org/en-US/Persona/Identity_Provider_Overview)

I know. It's pretty {profanity} awesome.

Screenshot: ![YAY](https://raw.github.com/shuhaowu/personal-idp/master/screenshot.png) 

Wat
===

This is a persona IDP you can pretty easily deploy on your server. It provides two factor authentication compatible with GAuthenticator.

The plan is eventually to have an app on the phone so it requests for access or something like that. Also logs are planned.

Setup
=====

The checked out source code is not really ready to be deployed/developed on. Right now everything is really chaotic and what not so the instruction maybe outdated.

This repo provides scripts to generate the keys and support documents. Those will be useful.

 1. Clone the repo
 2. `vagrant up`
 3. `vagrant ssh`
 4. `cd /vagrant/certs`
 5. `openssl genrsa -out private-key.pem 2048`
 6. `openssl rsa -in private-key.pem -pubout > public-key.pem`
 7. `/vagrant/scripts/gen_support_doc`
 8. At this point you have a `support_document` inside the root directory of this project and a keys.json file.
 9. `cd /vagrant; touch users.json`

Now you should have a reasonably working setup for production. The dev setup is really messy right now and will be cleaned up... eventually. so I won't include the instructions here yet.

To add users: 

    $ cd /vagrant
    $ DOMAIN=yourdomain.com DEBUG=1 python idp.py add
    Username: yourusername (this is without the @yourdomain.com part) so if you type in test this will automatically transform it to test@yourdomain.com for the Persona email
    Password:
    Repeat:

At this point, after filling in the username and password, you will see a QR code printed to your terminal. Scan that into Google Authenticator.

To delete users:

    $ cd /vagrant
    $ DOMAIN=yourdomain.com DEBUG=1 python idp.py del
    Username: yourusername

Your can also examine `/vagrant/users.json` manually. The password is kept via bcrypt.

Deploy Considerations
=====================

Deploying could be relatively difficult. This is an python app and can be deployed like any other python apps. However, a few notes must taken for security:

 1. A file named key.json will be generated and this is the key that the idp uses to sign users' certs. Please make sure that only the appropriate user has read access to this file. This file should be generated off the server and transfered onto the server and set to ro.
 2. A file named users.json is used to store the user information, including their OTP (2 factor) secrets. Please make sure that this is also read only and only the appropriate user has access to that file (usually the user used running the flask app).
 3. You will need SSL certificates. Keep them safe.
 4. It might not be a good idea to deploy on a VPS or something like that as the host could get your keys. Just be advised if you want to do that.

I personally use an nginx reverse proxy for the task of running everything.

Dev howto
=========

Ogod. There is a lot of issues with running this. Just don't mind it until I can get a chance to fix everything.

