"""

"""


# Built-in

# Libs
import numpy as np

# Own modules
from .misc_utils import load_file


def get_img_channel_num(file_name):
    """
    Get #channels of the image file
    :param file_name: absolute path to the image file
    :return: #channels or ValueError
    """
    img = load_file(file_name)
    if len(img.shape) == 2:
        channel_num = 1
    elif len(img.shape) == 3:
        channel_num = img.shape[-1]
    else:
        raise ValueError('Image can only have 2 or 3 dimensions')
    return channel_num


def change_channel_order(data, to_channel_last=True):
    """
    Switch the image type from channel first to channel last
    :param data: the data to switch the channels
    :param to_channel_last: if True, switch the first channel to the last
    :return: the channel switched data
    """
    if to_channel_last:
        if len(data.shape) == 3:
            return np.rollaxis(data, 0, 3)
        else:
            return np.rollaxis(data, 1, 4)
    else:
        if len(data.shape) == 3:
            return np.rollaxis(data, 2, 0)
        else:
            return np.rollaxis(data, 3, 1)


if __name__ == '__main__':
    pass
