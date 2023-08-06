import pandas as pd

def pandas_explorer(data_frame):
    return_dict = dict()
    
    describe = data_frame.describe(include = "all")
    number_of_rows = data_frame.shape[0]
    number_of_column = data_frame.shape[1]
    corr = data_frame.corr()
    
    return_dict['describe'] = describe
    return_dict['number_of_rows'] = number_of_rows
    return_dict['number_of_column'] = number_of_column
    return_dict['corr'] = corr 
    
    return return_dict

