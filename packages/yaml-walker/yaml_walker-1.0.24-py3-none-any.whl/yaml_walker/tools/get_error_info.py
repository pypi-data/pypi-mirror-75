import os
import sys
from collections import namedtuple

ERROR_INFO = namedtuple('ERROR_INFO', ['File', 'Line'])


def get_error_info():
    exc_type, exc_obj, exc_tb = sys.exc_info()
    file_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
    return ERROR_INFO(File=file_name, Line=exc_tb.tb_lineno)
