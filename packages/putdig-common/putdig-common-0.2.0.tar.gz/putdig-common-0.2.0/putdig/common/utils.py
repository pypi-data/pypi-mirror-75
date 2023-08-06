from pumpkin_supmcu.supmcu import DataType
from typing import Union, Any

_data_type_extremes = {
    DataType.UINT8: (0, 255),
    DataType.INT8: (-128, 127),
    DataType.UINT16: (0, 65535),
    DataType.INT16: (-32768, 32767),
    DataType.UINT32: (0, 4294967295),
    DataType.INT32: (-2147483648, 2147483647),
    DataType.UINT64: (0, 18446744073709551615),
    DataType.INT64: (-9223372036854775808, 9223372036854775807),
    DataType.Hex8: (0, 255),
    DataType.Hex16: (0, 65535)
}


def validate_value(val: str, data_type: DataType, idx: int = -1, max_size: int = -1) -> Union[bool, Any]:
    """
    Validates the given `val` against the `data_type`, ensuring that `val` is within the valid values for
    `data_type`.

    :param val: The value to validate against.
    :param data_type: The datatype of the telemetry item
    :param idx: The index of the telemetry item
    :param max_size: The max length of the telemetry item, is only used for `string` types.
    :return: True if the value is valid, the value otherwise
    """
    if 3 <= data_type <= 10:
        # Making sure that the value is an integer
        try:
            val = int(val)
        except ValueError:
            print(f"Value doesn't match data type {str(data_type).split('.')[-1]}")
            return False
        # Making sure the value is within the data type's min and max
        if not _data_type_extremes[data_type][0] <= val <= _data_type_extremes[data_type][1]:
            print(f"Value is too large for type {str(data_type).split('.')[-1]}")
            return False
    elif data_type == DataType.Str:
        if idx == -1 and max_size != -1:
            # Adding a null terminator and verifying that the val is the correct length
            val += "\x00"
            if len(val) > max_size:
                print(f"String is too long.  It neeeds to be {max_size - 1} characters or less")
                return False
            if len(val) < max_size:
                val = val[:-1] + " "*(max_size - val) + "\x00"
        else:
            pass  # TODO: figure out how to handle string size validation
            #             when the string is one of a few telemetry items
    elif data_type == DataType.Char:
        # Allowing the user to prepend a backslash to set values that are command characters
        if val.startswith("\\"):
            val = val[1:]
        if len(val) > 1:
            print("Chars can only be single characters")
            return False
    elif 10 < data_type < 13:
        # Verifying that the value is the right type
        try:
            val = float(val)
        except ValueError:
            print(f"Value doesn't match data type {str(data_type).split('.')[-1]}")
            return False

    elif data_type >= 13:
        # Making sure that the value is an integer and parsing it as a hex
        try:
            val = int(val, 16)
        except ValueError:
            print(f"Value doesn't match data type {str(data_type).split('.')[-1]}")
            return False
        # Making sure the value is within the data type's min and max
        if not _data_type_extremes[data_type][0] <= val <= _data_type_extremes[data_type][1]:
            print(f"Value is not within the size constraints for type {str(data_type).split('.')[-1]}")
            return False
    return val


def compare_versions(version1: str, version2: str) -> bool:
    v1 = version1.split('(')
    if len(v1) > 1:
        v1 = v1[0].rstrip() + v1[-1].split(')')[-1]
        version1 = ''.join(v1)
    v2 = version2.split('(')
    if len(v2) > 1:
        v2 = v2[0].rstrip() + v2[-1].split(')')[-1]
        version2 = ''.join(v2)
    return version1 == version2
