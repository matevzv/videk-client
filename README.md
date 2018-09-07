# Videk client

Videk client and related boot scripts. This package provides Videk REST client
and a systemd service for registration of SNA-LGTC boards in the Videk management
system.

To build Debian package:

    $ dpkg-buildpackage -b -uc

When built, install the package with:

    $ sudo dpkg -i videk-client_1.1.0-1_all.deb

After installation, the Videk API key must be written to the
`/etc/videk/api.key` file. This key can be found at videk.ijs.si by selecting
*Users*, *admin*. The API key is displayed under *API Token* header under *User
info*.
