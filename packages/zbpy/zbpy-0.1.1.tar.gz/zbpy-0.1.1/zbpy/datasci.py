from .zbprotocol_pb2 import QueryOrdering
from .indexedfieldentity import IndexedField
import uuid
import pandas as pd 
import numpy as np
from ast import literal_eval
import json 
try:
    import _pickle as pickle
except:
    import pickle 


def df_to_kvp(dataframe, df_key, start_entry):
    """
    Returns keys (list of strings), values (list of bytes), done (boolean). df_to_kvp = dataframe to key-value pairs

    Parameters:
        dataframe: pandas.DataFrame
        df_key: string 
        start_entry: integer 
    """
    input_bytes = []
    keys = []

    i = start_entry
    stop = start_entry + 1000 #NEED TO CHANGE THIS AND NUM IN put_dataframe IN ORDER TO CHANGE HOW MANY ENTRIES ARE SENT AT A TIME
    len_dataframe = len(dataframe)
    done = False 

    if stop > len_dataframe:
        stop = len_dataframe
        done = True 

    while(i < stop):
                    #Have to remove first/last char because '[]' and have to turn from string to dict 
        as_dict = dataframe.iloc[i:i+1,:].to_json(orient="records")[1:-1]
        entry_dict = literal_eval(as_dict.replace('null', 'None')) 
        entry_bytes = json.dumps(entry_dict).encode('utf-8')
        
        entry_uuid = uuid.uuid4()
        keys.append(f'{df_key}/{entry_uuid.int}')
        input_bytes.append(entry_bytes)

        i += 1

    return keys, input_bytes, done

def parse_df_columns(dataframe, specify_fields):
    """
    Returns a list of IndexedField objects.

    Parameters:
        dataframe: pd.DataFrame 
        specify_fields: list of strings 
    """
    indexed_fields = []

    col_names = dataframe.columns 
    col_types = dataframe.dtypes 

    if specify_fields is None:
        specify_fields = list(col_names)

    for i in range(len(col_types)):
        if str(col_names[i]) in specify_fields:
            
            indexed_field = parse_df_column(col_names[i], col_types[i].type)
            indexed_fields.append(indexed_field)

    return indexed_fields 

def parse_df_column(col_name, col_type):
    """
    Returns an IndexedField object. 

    Parameters:
        col_name: string 
        col_type: pd.dtype
    """
    field_name = str(col_name) 
    field_type = None 

    if col_type is np.float64:
        field_type = QueryOrdering.REAL_NUMBERS 
    elif col_type is np.int64 or col_type is np.bool:
        field_type = QueryOrdering.INTEGRAL_NUMBERS 
    else:
        field_type = QueryOrdering.LEXICOGRAPHIC 
    
    indexed_field = IndexedField(field_name, field_type)
    return indexed_field 

def parse_np_array(matrix, np_key, start_entry):
    """
    Returns bytes of an encoded 

    Parameters:
        array: np.array
    """
    input_bytes = []
    keys = []

    i = start_entry
    stop = start_entry + 1024 #NEED TO CHANGE THIS AND NUM IN put_np_array IN ORDER TO CHANGE HOW MANY ENTRIES ARE SENT AT A TIME
    len_matrix = len(matrix)
    done = False 

    if stop > len_matrix:
        stop = len_matrix
        done = True 

    while(i < stop):
        input_matrix, i = get_np_rows(matrix, i)    
        input_bytes.append(pickle.dumps(input_matrix))
        entry_uuid = uuid.uuid4()
        keys.append(f'{np_key}/{entry_uuid.int}')

    return keys, input_bytes, done


def get_np_rows(matrix, start_entry, x=512):
    """
    Returns the next x rows of a numpy array. 
    """
    arrays = []

    matrix_len = len(matrix)
    end_entry = start_entry + x

    if matrix_len < start_entry + x:
        end_entry = matrix_len 

    for i in range(start_entry, end_entry):
        arrays.append(matrix[i])
        
    return arrays, end_entry