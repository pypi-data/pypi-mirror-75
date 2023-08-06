# -*- coding: utf-8

"""
@File       :   test.py
@Author     :   Zitong Lu
@Contact    :   zitonglu1996@gmail.com
@License    :   MIT License
"""

import os
import numpy as np
from six.moves import urllib
from pyctrsa.util.progressbar import show_progressbar
from pyctrsa.util.download_data import schedule
from pyctrsa.util.unzip_data import unzipfile
from pyctrsa.util.preprocess_data import pre_data

url = 'https://attachment.zhaokuangshi.cn/BaeLuck_2018jn_data.zip'
filename = 'BaeLuck_2018jn_data.zip'
data_dir = '../data/'
filepath = data_dir + filename

"""  Section 1: Download Data  """

"""exist = os.path.exists(filepath)
if exist == False:
    urllib.request.urlretrieve(url, filepath, schedule)
    print('Download completes!')
elif exist == True:
    print('Data already exists!')

unzipfile(filepath, data_dir)"""


"""  Section 2: Data preprocessing for further calculation  """

"""subs = ["201", "202", "203", "204", "205", "206", "207", "208", "209",
        "210", "212", "213", "215", "216", "217", "218"]

pre_data(subs, data_dir)"""


"""  Section 3: Normal Cross-Temporal Similarities based on Neural Data  """

# take the data under 0° orientation and data under 180° orientation for example
