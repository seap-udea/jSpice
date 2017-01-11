# jSpice
SPICE-enabled javascript library for high precision astronomical calculations in the Web

Presentation
------------

**jSpice** is a ``javascript+Pyhton`` library intended to provide an
efficient set of tools to calculate high precision astronomical
ephemeris over interactive websites.

Although many astronomical websites include their own code to
calculate ephemeris or use third-party libraries for the same purpose,
most of them rely on algorithms with limited precision and
functionality.

But recreative and educational astronomy is getting closer to the
techniques and methods that in the past was mostly reserved to
professional astronomers.  As a result precise and sophisticated
calculations are becoming more common.

Computing lunar ephemeris, occultation times, eclipse conditions or
simply solar system's bodies positions to a precission of milliseconds
and arcseconds is very hard using classical algorithms.  For that
purpose professional astronomers and aerospace engineers use offline
tools such as NASA NAIF's **SPICE toolkit** or USNO's Nova software.

**jSpice** is an effort to bring the power and precission of those
tools, to the realm of interactive JS+AJAX+CSS+HTML5 powered websites.

With **jSpice** you will be able to:

- Invoke any SPICE routine from a JS powered website. 

- Create JS+HTML5 animations using real time calculations powered by
  SPICE.

- Calculate complex ephemeris for simple interactive websites without
  the burden of complex CGI scripts.

Quickstart
----------

Before you start you have to decide if you will use an already
existing **jSpice** public server or if you want to install a new
server in your own website.

The following instructions assume that you will use the public test
server running at http://urania.udea.edu.co/jSpice.  If you want to
install a new server jump to next section and then come back.

Once you have decided which server you will use, you just need to
download the package **jSpice** from github:

```
$ git clone --branch master http://github.com/seap-udea/jSpice.git
```

The package come along with the server source files and data.  If you
will not install a server by yourself remove the ``server`
directory.

```
$ rm -r jSpice/server
```

We recommend to place ``jSqpice`` in the ``js`` directory of your
website.

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
