import sys

def get_error_message(error, error_detail:sys, missing_columns=None):
    _, _, exc = error_detail.exc_info()
    lineno = exc.tb_lineno
    filename = exc.tb_frame.f_code.co_filename

    error_message = f"Error occurred in python script {filename} line number {lineno} error message {str(error)}"

    if missing_columns:
        error_message += f"\nThe following required columns are missing from the data: {missing_columns}"
        
    return error_message

class CustomException(Exception):
    def __init__(self, error_message, error_detail:sys, missing_columns=None):
        self.error_message = get_error_message(error_message, error_detail, missing_columns)
        super().__init__(self.error_message)

    def __str__(self):
        return self.error_message
