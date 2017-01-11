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
tools, to the realm of interactive JS+AJAX+CSS powered websites.

With **jSpice** you will be able to:

- Invoke any SPICE routine from a JS powered website. 


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
