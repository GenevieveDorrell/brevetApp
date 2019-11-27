"""
Open and close time calculations
for ACP-sanctioned brevets
following rules described at https://rusa.org/octime_alg.html
and https://rusa.org/pages/rulesForRiders
"""
import arrow


#  Note for CIS 322 Fall 2016:
#  You MUST provide the following two functions
#  with these signatures, so that I can write
#  automated tests for grading.  You must keep
#  these signatures even if you don't use all the
#  same arguments.  Arguments are explained in the
#  javadoc comments.
#


def open_time(control_dist_km, brevet_dist_km, brevet_start_time):
    """
    Args:
       control_dist_km:  number, the control distance in kilometers
       brevet_dist_km: number, the nominal distance of the brevet
           in kilometers, which must be one of 200, 300, 400, 600,
           or 1000 (the only official ACP brevet distances)
       brevet_start_time:  An ISO 8601 format date-time string indicating
           the official start time of the brevet
    Returns:
       An ISO 8601 format date string indicating the control open time.
       This will be in the same time zone as the brevet start time.
    """
    hour_shift = 0
    dist = brevet_dist_km
    openTime = arrow.get(brevet_start_time)
    if control_dist_km < dist:
        dist = control_dist_km
    if dist == 0.0:
        return openTime.format('dddd MM/DD/YYYY HH:mm')
    if dist > 600.0:
        hour_shift += (dist - 600) / 28
        dist -= (dist - 600)
    if dist > 400.0:
        hour_shift += (dist - 400) / 30
        dist -= (dist - 400)
    if dist > 200.0:
        hour_shift += (dist -200) / 32
        dist -= (dist - 200)
    if dist <= 200.0:
        hour_shift += dist / 34

    openTime = openTime.shift(hours=+hour_shift)
    return openTime.format('dddd MM/DD/YYYY HH:mm')


def close_time(control_dist_km, brevet_dist_km, brevet_start_time):
    """
    Args:
       control_dist_km:  number, the control distance in kilometers
          brevet_dist_km: number, the nominal di stance of the brevet
          in kilometers, which must be one of 200, 300, 400, 600, or 1000
          (the only official ACP brevet distances)
       brevet_start_time:  An ISO 8601 format date-time string indicating
           the official start time of the brevet
    Returns:
       An ISO 8601 format date string indicating the control close time.
       This will be in the same time zone as the brevet start time.
    """

    dist = brevet_dist_km
    closeTime = arrow.get(brevet_start_time)
    if control_dist_km < dist:
        dist = control_dist_km
    if dist == control_dist_km and dist == 200.0:
        hour_shift = 13.5
    elif dist == 0.0:
        hour_shift = 1
    elif dist < 60.0:
        hour_shift = 1 + dist / 20
    elif dist > 600.0:
        hour_shift = 600 / 15 + (dist - 600) / 11.428
    else:
        hour_shift = dist / 15

    closeTime = closeTime.shift(hours=+hour_shift)
    return closeTime.format('dddd MM/DD/YYYY HH:mm')
