from math import pi, atanh, sin, cos, exp

def convert_gps_into_lambert(latitude, longitude):
    c =	11754255.426096
    e = 0.0818191910428158
    n = 0.725607765053267
    xs = 700000
    ys = 12655612.049876

    radian_latitude = latitude/180*pi
    iso_latitude = atanh(sin(radian_latitude)) - e * atanh(e * sin(radian_latitude))

    lambert_x = c * exp(-n*iso_latitude) * sin(n * (longitude - 3)/ 180 * pi) + xs
    lambert_y = ys -  c * exp(-n*iso_latitude) * cos(n * (longitude - 3)/ 180 * pi)
    return lambert_x, lambert_y