import re


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


def convert_to_metres(a_value, a_uom):
    conversion_dict = {
        'KM': 1000,
        'MI': 1609.344,
        'NM': 1852,
        'M': 1,
        'FT': 0.3048
    }

    regex = '^' + a_uom
    modifier = None
    for key, value in conversion_dict.items():
        if re.match(regex, key, flags=re.IGNORECASE):
            modifier = value

    if modifier is None:
        raise TypeError(f'{a_uom} is not an accepted unit of measure. Accepted units of measure are M, MI, KM, FT'
                        f' and NM')
    else:
        return round((a_value * modifier), 3)


def get_earth_radius(**kwargs) -> float:
    uom_dict = {'km': 6378.14, 'mi': 3963.19, 'nm': 3443.92, 'm': 6378140.00}
    return uom_dict[kwargs.pop('uom', 'km')]


def contains_z_value(coordinate_string: str):
    coordinate_string.split(' ')
    if len(coordinate_string) == 3:
        return True
    elif len(coordinate_string) == 2:
        return False
    else:
        raise ValueError('Coordinate string must contain at least two valid coordinates of the same type and an,'
                         ' optional height z value, separated by a comma separator')


def detect_coordinate_type(coordinate_string):
    split_list = coordinate_string.split(' ')

    def match_regex(string_to_match):
        regex_dict = {'dms': '^\d{6,7}[.]\d{1,}\D{1}$|^\d{6,7}\D{1}$',
                      'dd': '^[-?|+?]?\d{1,3}[.]\d+|[-?|+?]?\d{1,3}$'}

        if re.match(regex_dict['dms'], string_to_match):
            return 'dms'
        elif re.match(regex_dict['dd'], string_to_match):
            return 'dd'
        else:
            raise ValueError('Only valid DMS or decimal degree coordinate pairs are accepted.')

    def equal_type(type_1: str, type_2: str):
        if type_1 == type_2:
            return type_1
        else:
            raise ValueError('Both latitude and longitude must be the same type.  Both DMS or both DD.')

    lat_type = match_regex(split_list[0].strip())
    lon_type = match_regex(split_list[1].strip())

    if equal_type(lat_type, lon_type):
        return lat_type
    else:
        raise ValueError('Latitude and longitude must both be the same type.  ie - both decimal degrees; dms'
                         'or UTM')


def point_or_segment(coordinate_string: str):
    if '=' in coordinate_string:
        return 'curvedsegment'
    else:
        return 'point'


def split_segment_string(string):
    split_list = string.split(', ')
    segment_dict = {item.split('=')[0]: item.split('=')[1] for item in split_list}
    return segment_dict
