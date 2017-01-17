#!/bin/bash

kernels=(
    # Leap seconds
    "http://naif.jpl.nasa.gov/pub/naif/generic_kernels/lsk/naif0012.tls"

    # Earth reference frame

    # High precission orientation to present
    "http://naif.jpl.nasa.gov/pub/naif/generic_kernels/pck/earth_latest_high_prec.bpc"
    # High precission orientation past
    "http://naif.jpl.nasa.gov/pub/naif/generic_kernels/pck/earth_720101_070426.bpc"
    # Extrapolated low precission in future
    "http://naif.jpl.nasa.gov/pub/naif/generic_kernels/pck/earth_070425_370426_predict.bpc"
    # Earth reference frame
    "http://naif.jpl.nasa.gov/pub/naif/generic_kernels/fk/planets/earth_assoc_itrf93.tf"
    # Earth fixed
    "http://naif.jpl.nasa.gov/pub/naif/generic_kernels/pck/earth_fixed.tf"

    # Lunar orientation
    "http://naif.jpl.nasa.gov/pub/naif/generic_kernels/pck/moon_pa_de403_1950-2198.bpc"
    # Reference frame
    "http://naif.jpl.nasa.gov/pub/naif/generic_kernels/fk/satellites/moon_080317.tf"

    # GM data
    "http://naif.jpl.nasa.gov/pub/naif/generic_kernels/pck/gm_de431.tpc"

    # Asteroid reference frame
    "http://naif.jpl.nasa.gov/pub/naif/generic_kernels/spk/asteroids/codes_300ast_20100725.tf"

    # Orientation data for planets
    "http://naif.jpl.nasa.gov/pub/naif/generic_kernels/pck/pck00010.tpc"

    # Accurate planetary ephemeris
    "http://naif.jpl.nasa.gov/pub/naif/generic_kernels/spk/planets/de431_part-1.bsp"
    "http://naif.jpl.nasa.gov/pub/naif/generic_kernels/spk/planets/de431_part-2.bsp"

    # Accurate lunar ephemeris
    "http://naif.jpl.nasa.gov/pub/naif/generic_kernels/spk/planets/de430.bsp"

    # Planetary satellites
    "http://naif.jpl.nasa.gov/pub/naif/generic_kernels/spk/satellites/jup310.bsp"

    "http://naif.jpl.nasa.gov/pub/naif/generic_kernels/spk/satellites/sat368.bsp"
    "http://naif.jpl.nasa.gov/pub/naif/generic_kernels/spk/satellites/sat375.bsp"
    "http://naif.jpl.nasa.gov/pub/naif/generic_kernels/spk/satellites/sat393.bsp"

    # Asteroids
    "http://naif.jpl.nasa.gov/pub/naif/generic_kernels/spk/asteroids/codes_300ast_20100725.bsp"
)

for kernel in "${kernels[@]}"
do 
    wget $kernel
done
