This is your certificate folder. Inside here should lie two files:

 - certificate.pem - This is your public certificate
 - certificate.key - This is your private key. Be careful with it.

These should be the real certificates you use on the server, if possible.

You could in theory also use another certificate for a different domain, but
development needs to be against that domain.

Also this certificate must be accepted by your browser. A StartSSL certificate
is free and you should get it today.
