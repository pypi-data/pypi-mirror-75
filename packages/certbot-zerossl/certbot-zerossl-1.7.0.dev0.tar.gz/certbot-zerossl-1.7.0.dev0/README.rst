Certbot (ZeroSSL Edition)
=========================

Installation
------------

Install the client with::

    python -m pip install certbot-zerossl



How to run the client
---------------------

https://zerossl.com/features/acme/

Understanding the client in more depth
--------------------------------------

To understand what the client is doing in detail, it's important to
understand the way it uses plugins.  Please see the `explanation of
plugins <https://certbot.eff.org/docs/using.html#plugins>`_ in
the User Guide.

Links
=====

Documentation: https://certbot.eff.org/docs

Upstream project: https://github.com/certbot/certbot

Main Website: https://zerossl.com/features/acme/

ACME spec: http://ietf-wg-acme.github.io/acme/

ACME working area in github: https://github.com/ietf-wg-acme/acme



System Requirements
===================

See https://certbot.eff.org/docs/install.html#system-requirements.


Current Features
=====================

* Supports multiple web servers:

  - apache/2.x
  - nginx/0.8.48+
  - webroot (adds files to webroot directories in order to prove control of
    domains and obtain certs)
  - standalone (runs its own simple webserver to prove you control a domain)
  - other server software via `third party plugins <https://certbot.eff.org/docs/using.html#third-party-plugins>`_

* The private key is generated locally on your system.
* Can talk to the Let's Encrypt CA or optionally to other ACME
  compliant services.
* Can get domain-validated (DV) certificates.
* Can revoke certificates.
* Adjustable RSA key bit-length (2048 (default), 4096, ...).
* Can optionally install a http -> https redirect, so your site effectively
  runs https only (Apache only)
* Fully automated.
* Configuration changes are logged and can be reverted.
* Supports an interactive text UI, or can be driven entirely from the
  command line.
* Free and Open Source Software, made with Python.

For extensive documentation on using Certbot, go to https://certbot.eff.org/docs.
