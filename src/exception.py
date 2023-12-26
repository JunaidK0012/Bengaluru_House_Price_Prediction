import os
import sys

def get_error_message(error,error_detail:sys):
    _,_,exc = error_detail.exc_info()
    lineno = exc.tb_lineno
    filename = exc.tb_frame.f_code.co_filename

    error_message = " Error occured in python script {} line number {} error message {} ".format(filename,lineno,str(error))
    return error_message

class CustomException():
    def __init__(self,error_message,error_detail:sys):
        super.__init__(error_message)
        self.error_message = get_error_message(error_message,error_detail=error_detail)

    def __str__(self):
        return self.error_message