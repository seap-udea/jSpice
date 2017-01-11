# jSpice
SPICE-enabled javascript library for high precision astronomical calculations in the Web

Presentation
------------

**jSpice** is a ``javascript+Pyhton`` library intended to provide an
efficient set of tools to calculate high precision astronomical
ephemeris for interactive websites.

Although many interactive astronomical websites include their own code
to calculate ephemeris or use third-party libraries, most of them rely
on algorithms with limited precision and functionality.



Getting a copy
--------------

There are two type of **tQuakes** repositories: ``master`` and
``station``. 

``master`` is the repository containing all the files required to
install a database server. A ``master`` repository should be installed
in the apache root directory:

```
$ cd /var/www/html
$ git clone --branch master http://github.com/seap-udea/tQuakes.git
```

The ``station`` repository is that containing the required files for a
calculation station.  It could be installed on any directory on the machine:

```
$ git clone --branch station --single-branch http://github.com/seap-udea/tQuakes.git
```
