def dms_to_decimal(latitude_or_longitude):
    slice_dms = get_dms_slice_dict(latitude_or_longitude)
    calculated_dms_dict = calculate_dms_to_decimal(slice_dms)

    # Using formula - DD + MM / 60 + SS.ss / 3600
    decimal_coordinate = calculated_dms_dict['degrees'] + (calculated_dms_dict['minutes'] +
                                                           calculated_dms_dict['seconds'])

    if slice_dms['hemisphere'] == 'S' or slice_dms['hemisphere'] == 'W':
        decimal_coordinate = -abs(decimal_coordinate)

    return decimal_coordinate


def get_dms_slice_dict(latitude_or_longitude_string):
    hemisphere = latitude_or_longitude_string[-1]

    if hemisphere == 'W' or hemisphere == 'E':
        degrees = int(latitude_or_longitude_string[0:3])
        minutes = int(latitude_or_longitude_string[3:5])
        seconds = float(latitude_or_longitude_string[5:-1])

    elif hemisphere == 'N' or hemisphere == 'S':
        degrees = int(latitude_or_longitude_string[0:2])
        minutes = int(latitude_or_longitude_string[2:4])
        seconds = float(latitude_or_longitude_string[4:-1])

    else:
        raise ValueError('DMS coordinates must indicate which hemisphere they belong to by appending N, E, S or W' \
                         'to the end of the coordinate.  No other format currently accepted')

    slice_dict = {'degrees': degrees, 'minutes': minutes, 'seconds': seconds, 'hemisphere': hemisphere}

    return slice_dict


def calculate_dms_to_decimal(dms_sliced_dict):
    degrees = dms_sliced_dict['degrees']
    minutes = dms_sliced_dict['minutes'] / 60
    seconds = dms_sliced_dict['seconds'] / 3600

    calculated_dms_dict = {'degrees': degrees, 'minutes': minutes, 'seconds': seconds,
                           'hemisphere': dms_sliced_dict['hemisphere']}

    return calculated_dms_dict


def get_earth_radius(**kwargs) -> float:
    uom_dict = {'km': 6378.14, 'mi': 3963.19, 'nm': 3443.92, 'm': 6378140.00}
    # Radius of earth in Km
    radius = uom_dict[kwargs.pop('uom', 'km')]

    return radius