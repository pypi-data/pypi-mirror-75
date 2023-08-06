import pandas as pd
import numpy as np
import json 
from .util import unwrap_zb_error
try:
    import _pickle as pickle
except:
    import pickle 
from ast import literal_eval

def parse_object(s):
    return json.loads(s)

class PutPages():

    def __init__(self, client, keys, data):
        self.client = client 
        self.keys = keys 
        self.data = data 
        self.max_bytes_per_page = 2000000 
        self.cur_idx = 0 
    
    def put_all(self, table_id, overwrite=False, table_owner_id=None):
        """
        Puts data into specified table. 

        Parameters: 
            table_id: string 
            overwrite: boolean (default=False)
            table_owner_id: string (default=self.client.id())
        """
        key_pages, value_pages = self.pagify()

        for i in range(len(key_pages)):
            keys = key_pages[i]
            values = value_pages[i]
            
            error = self.client.put_multi_helper(table_id, keys, values, overwrite, table_owner_id)
            
            if unwrap_zb_error(error) is not None:
                return unwrap_zb_error(error)

        return None


    def pagify(self):
        """
        Returns 2d array of strings, 2d array of bytes.
        """
        page_bytes = 0 
        cur_page = []
        cur_page_values = []
        pages = []
        page_values = []

        for i in range(len(self.keys)):
            d_len = len(self.data[i])
            if (page_bytes + d_len) > self.max_bytes_per_page:
                pages.append(cur_page)
                page_values.append(cur_page_values)
                cur_page = []
                cur_page_values = []
                page_bytes = 0 

            cur_page.append(self.keys[i])
            cur_page_values.append(self.data[i])
            page_bytes += d_len

        if len(cur_page) > 0:
            pages.append(cur_page)
            page_values.append(cur_page_values)

        return pages, page_values 

class PaginationHandler():

    def __init__(self, f):
        """
        Initializes instance of PaginationHandler class.

        Parameters:
            f: paginationRequester - func (int) -> (dict[string][byte], bool) 
        """
        self.requester = f #paginationRequester func (int) -> (dict[string][]byte, bool)
        self.cur_data = None #dict[string][]byte
        self.cur_page = -1 #int
        self.has_next_page = True #bool
        self.cur_i = 0
        self.cur_keys = []
        self.return_dict = False 

    def __iter__(self):
        return self 

    def __next__(self):
        if self.cur_keys == []:
            self.cur_keys = self.keys()

        if self.cur_i >= len(self.cur_keys):
            if self.has_next_page:
                self.next()
                self.cur_keys = self.keys()
                self.cur_i = 0
            else:
                raise StopIteration()

        if len(self.cur_keys) > self.cur_i:
            cur_key = self.cur_keys[self.cur_i]
            cur_item = self.cur_data[cur_key]
            self.cur_i += 1
        else:
            raise StopIteration()


        try:
            if self.return_dict:
                return json.loads(cur_item)

            elif cur_item is not None:
                return cur_item
                
            else:
                return cur_key
        except TypeError:
            #Comes to this if (return literal_eval(cur_item.decode())) fails because cur_item is None
            if cur_item is not None:
                return pickle.loads(cur_item)
            return cur_key
        

    def return_pretty(self):
        """
        Will make items return as Python dictionaries when PaginationHandler is iterated through. 
        """
        self.return_dict = True 

    def return_bytes(self):
        """
        Will make items return as bytes when PaginationHandler is iterated through. 
        """
        self.return_dict = False 
    
    def data(self):
        """
        Returns dict that maps strings to a list of bytes. 
        """
        return self.cur_data 

    def keys(self):
        """
        Returns a list of strings. 
        """
        keys = []
        for key in self.cur_data:
            keys.append(key)
        return keys 

    def data_all(self):
        """
        Returns a dict that maps strings to a list of bytes.
        """
        i = 1
        data = self.cur_data
        while(self.has_next_page):
            dat, nxt = self.requester(i)
            for key in dat:
                data[key] = dat[key]
            i += 1
            self.has_next_page = nxt 
            self.cur_page = i 
            if len(dat) == 0 or not nxt:
                break 
        
        self.has_next_page = False 
        self.cur_data = data  
        return self.cur_data

    def keys_all(self):
        """
        Returns a list of string.
        """
        ks = []
        for k in self.cur_data:
            ks.append(k)

        if not self.has_next_page:
            return ks 
        
        i = 1
        while(True):
            dat, nxt = self.requester(i)
            for k in dat:
                ks.append(k)
                self.cur_data[k] = None 
            i += 1 
            self.has_next_page = nxt 
            self.cur_page = i 
            if len(dat) == 0 or not nxt:
                break 
        
        self.has_next_page = False 
        return ks
    
    def next(self):
        """
        Changes the current data stored in the pagination handler to the next page if there is one. 
        """
        if not self.has_next_page:
            return 

        self.cur_page += 1 
        dat, nxt = self.requester(self.cur_page)
        
        self.cur_data = dat
        self.has_next_page = nxt  

    def to_dataframe(self):
        """
        Transforms all data in PaginationHandler into pandas.DataFrame.
        """
        indices = []
        df_data = {}

        all_data = self.data_all()
        for i in all_data:
            indices.append(i)

            #turn entry from bytes to python dictionary 
            #to_dict = all_data[i].decode()
            #entry = literal_eval(to_dict.replace('null', 'None'))
            entry = parse_object(all_data[i])
            for key in entry: 
                if key not in df_data:
                    df_data[key] = [entry[key]]
                else:
                    df_data[key].append(entry[key])

        return pd.DataFrame(df_data, index=indices)

    def to_numpy_arrays(self):
        """
        Transforms all data in PaginationHandler into a list of numpy arrays. 
        """
        tot = [pickle.loads(i) for i in self]
    
        return np.concatenate(tuple(tot), axis=0) 

def break_keys(keys, items_per_page):
    key_groups = []

    len_keys = len(keys)
    for i in range(0, len_keys+items_per_page, items_per_page):
        kg = keys[i-items_per_page:i]
        key_groups.append(kg)
    return key_groups[1:]

class GetPages():

    def __init__(self, client, keys, max_item_size, table_id, table_owner_id=None):
        if table_owner_id is None: 
            table_owner_id = client.id()

        max_page_size = 2000000
        items_per_page = max_page_size // max_item_size 


        self.client = client 
        self.key_groups = break_keys(keys, items_per_page)
        self.items_per_page = items_per_page
        self.table_id = table_id 
        self.table_owner_id = table_owner_id
        self.key_index = 0 
        self.pretty = False 
        self.cur_pag = None 

    def __iter__(self):
        return self 

    def __next__(self):
        if self.cur_pag is None:
            self.cur_pag = self.get_cur_pag()

        try:
            if self.pretty:
                self.cur_pag.return_dict = True 
            else:
                self.cur_pag.return_dict = False 
            return self.cur_pag.__next__()

        except StopIteration:
            if self.key_index < len(self.key_groups) - 1:
                self.key_index += 1
                self.cur_pag = self.get_cur_pag()

                if self.pretty:
                    self.cur_pag.return_dict = True 
                else:
                    self.cur_pag.return_dict = False

                return self.cur_pag.__next__()
            
            raise StopIteration()

    def get_cur_pag(self):
        pag = self.client.get_helper(self.table_id, self.key_groups[self.key_index], self.table_owner_id)
        return pag

    def data_all(self):
        data = {}
        
        while self.key_index < len(self.key_groups):
            cur_pag = self.get_cur_pag()
            data.update(cur_pag.data_all())

            self.key_index += 1 

        return data 

    def get_first_n_pages(self, n):
        data = {}

        while self.key_index < n:
            cur_pag = self.get_cur_pag()
            data.update(cur_pag.data_all())

            self.key_index += 1 
        
        return data 

    def keys_all(self):
        keys = []
        while self.key_index < len(self.key_groups):
            cur_pag = self.get_cur_pag()
            keys += cur_pag.keys_all()
            self.key_index += 1 

        return keys 

    def return_pretty(self):
        self.pretty = True 

    def return_bytes(self):
        self.pretty = False 

    def data(self):
        if self.key_groups == []:
            return {}

        cur_pag = self.get_cur_pag()
        return cur_pag.data_all()

    def keys(self):
        if self.key_groups == []:
            return []

        cur_pag = self.get_cur_pag()
        return cur_pag.keys_all()
    
    def next(self):
        if self.key_index < len(self.key_groups) - 1:
            self.key_index += 1 

    def to_dataframe(self):
        dfs = []

        while self.key_index < len(self.key_groups):
            cur_pag = self.get_cur_pag()
            dfs.append(cur_pag.to_dataframe())
            self.key_index += 1 

        return pd.concat(dfs)

    def to_numpy_arrays(self):
        arrays = []

        while self.key_index < len(self.key_groups):
            cur_pag = self.get_cur_pag()
            arrays.append(cur_pag.to_numpy_arrays())
            self.key_index += 1 

        return np.concatenate(tuple(arrays), axis=0)


def standard_pagination_handler(f):
    """
    Returns an object of class PaginationHandler.
    
    Parameters: 
        f: paginationRequester - func (int) -> (dict[string][byte], bool) 
    """
    ph = PaginationHandler(f)
    ph.next()
    return ph