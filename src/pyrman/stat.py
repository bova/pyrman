'''
Created on 18.03.2012

@author: vladandr
'''
import os
from datetime import datetime
from datetime import timedelta
import re

def _file_date_time(file_name):
    '''Return file modification time
    
    @param file_name: path to file
    '''
    return datetime.fromtimestamp(os.path.getmtime(file_name))

def _is_define(list_element):
    '''Reject element that equal None
    '''
    if list_element:
        return True
    else:
        return False

def _is_new_file(file_name):
    '''Check whether it fresh file
    
    @param file_name: path to file
    '''
    now = datetime.now()
    if (now - _file_date_time(file_name)) < timedelta(hours=12):
        return file_name
    else:
        return False

def _readable_size(file_size):
    '''Return file_size in more intuitive manner
    
    @param file_size: number
    '''
    unit_list = ['K', 'M', 'G']
    k_byte = 1024
    quotient, reminder = divmod(file_size, k_byte)
    unit_idx = 0
    while quotient > k_byte:
        quotient, reminder = divmod(quotient, k_byte)
        unit_idx += 1
    quotient = quotient + round(reminder/k_byte, 1)
    return str(quotient) + '' + unit_list[unit_idx]

class Explorer(object):
    '''Class for:
        - working with path, files
        - Find newest files
        - Format output
    '''
    def __init__(self, file_path):
        self.file_list = []
        self.newest_files = []
        
        self.walk(file_path)
        self._filter_newest_files()

    def visit(self, arg, dirname, names):
        '''For each file concatanate file & path
        and put result into class variable
        '''
        for name in names:
            self.file_list.append(os.path.join(dirname, name))

    def walk(self, path):
        '''Walk on PATH and execute self.visit function
        '''
        os.path.walk(path, self.visit, 1)


    def _filter_newest_files(self):
        '''Filter only fresh files        
        '''
        self.newest_files = filter(_is_define, 
                                   map(_is_new_file, self.file_list))



    def get_info(self):
        '''Return tabular info about fresh files
        '''
        files_info = '\n'
        for fname in self.newest_files:
            file_size = os.path.getsize(fname)
            files_info += '%20s %9s \n'  % (fname, _readable_size(file_size))
        return files_info

class RMANLog(object):    
    '''Check RMAN log for errors'''
    def __init__(self, log_file):
        self.log_file = log_file
        self.is_error = False
        self.err_cnt = 0

    def has_error(self):
        '''Search for RMAN- pattern in log_file        
        '''
        pattern = re.compile("RMAN-")
        for log_line in self.log_file:            
            if pattern.match(log_line):
                self.is_error = True
                self.err_cnt += 1                
        return self.is_error
