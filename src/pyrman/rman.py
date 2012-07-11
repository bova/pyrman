'''
Created on 15.03.2012

@author: bova
'''
import logging
import fido_common.loggingtool as loggingtool
from datetime import date
import os
import sys
import re
import StringIO
import time

try:                           # work only with python version > 2.4
    import subprocess
    IS_SUBPROCESS = True
except ImportError:
    IS_SUBPROCESS = False
    
# template constatant
TPL_BACKUP_PATH = "%BACKUP_PATH%"
BACKUP_DURATION = "%BACKUP_DURATION%"

def get_curr_day_name():
    '''Return name of day (Monday,..., Sunday)
    '''
    return date.today().strftime("%A")


class RmanEnv(object):
    '''Holds RMAN environment variables    
    '''
    tpl_file = ''
    db_scpt = ''
    log_file = ''
    log_h = ''   
    

class Rman(object):
    '''Oracle RMAN utility     
    '''
    def __init__(self, conf):
        '''Initialize Rman instance
        
        @param conf: type of AppConf
        '''
        self.conf = conf
        self.env = RmanEnv()
        self.output_buff = StringIO.StringIO() 
        self.init_env()
                
        self.logger = logging.getLogger(conf.app_name)
        self.backup_duration = 0
        
    def init_env(self):
        '''Initialize environment which relate with RMAN'''
        self.env.log_file = os.path.join(self.conf.app.log_path, 
                                     'rman_%s.log' % self.conf.ora.sid) 
        self.env.log_h = open(self.env.log_file, 'w')
         

        
    def is_full_bkp_day(self):
        '''Decide which backup type will be used
        
        @param conf: appConf instance
        '''
        if self.conf.bkp.is_allways_full:
            return True
        day_name = self.conf.rman.full_bkp_day
        return day_name.lower() == get_curr_day_name().lower()
    
    def choose_bkp_type(self):
        '''Choose, which backup will be used        
        '''
        if self.is_full_bkp_day():
            self.env.tpl_file = self.conf.rman.tpl_full
            self.env.db_scpt = self.conf.rman.scpt_full
        else:
            self.env.tpl_file = self.conf.rman.tpl_incr
            self.env.db_scpt = self.conf.rman.scpt_incr

    def gen_bkp_scpt(self, tpl_data, script_type='db'):
        '''Generate script text
        
        @param tpl_data:
        @param script_type: 'db' or 'arch'
        '''
        #return Template(tpl_data).substitute(backup_path=backup_path)  
        #Not suitable for old python versions
        res = re.sub(TPL_BACKUP_PATH, self.conf.bkp.path, tpl_data)
        if script_type == 'arch':
            res = re.sub(BACKUP_DURATION, str(self.backup_duration), res)
        return res

    
    def write_scpt_data(self, data, output_file):
        '''Write some data to file
                
        @param data:
        '''
        try:
            scpt_file_hdlr = open(output_file, 'w+')
            scpt_file_hdlr.write(data)
        except IOError, err:
            print "I/O error: %s" % (err)
        else:
            scpt_file_hdlr.close()

    def build_scritps(self, script_type='db'):
        '''Generate backup scripts        
        
        @param script_type: 'db' or 'arch'
        '''
        if script_type == 'db':
            tpl = os.path.join(self.conf.app.tpl_path, self.env.tpl_file)
            tpl_file_hdlr = open(tpl, 'r+')
            tpl_data = tpl_file_hdlr.read()
            scpt_data = self.gen_bkp_scpt(tpl_data)
            self.write_scpt_data(scpt_data, self.env.db_scpt)
        elif script_type == 'arch':
            tpl = os.path.join(self.conf.app.tpl_path, self.conf.rman.tpl_arch)
            tpl_file_hdlr = open(tpl, 'r+')
            tpl_data = tpl_file_hdlr.read()
            scpt_data = self.gen_bkp_scpt(tpl_data, 'arch')
            self.write_scpt_data(scpt_data, self.conf.rman.scpt_arch)        

    def run_script(self, cmd_line):
        ''' Run system process 
        
        @param cmd_line: shell command line string
        '''
        ts = time.time()
        env = {"ORACLE_HOME": self.conf.ora.home, 
               "ORACLE_SID": self.conf.ora.sid, 
               "PATH": self.conf.ora.home +'/bin:'+ os.environ["PATH"]}
        
        try:
            proc = subprocess.Popen(cmd_line, 
                                    shell=True, 
                                    stdout=subprocess.PIPE, 
                                    universal_newlines=True, env=env)
            self.logger.debug('Run Subprocess ' + str(proc))                
            self.output_buff.write(proc.communicate()[0])
        except NameError:  # prior python v2.4 workaround
            os.putenv("ORACLE_HOME", self.conf.ora.home)
            os.putenv("ORACLE_SID", self.conf.ora.sid)
            os.putenv("PATH", self.conf.ora.home + 
                      "/bin:" + os.environ["PATH"])
            pipe = os.popen(cmd_line)
            self.logger.debug("Run Commands %s" % str(pipe))
            self.output_buff.write(pipe.read())
            self.logger.debug("Execution completed")            
            pipe.close()
            print "exception occured"
        except:
            self.logger.error('error while execute script %s' % 
                              sys.exc_info()[0])
        te = time.time() + 3600 # 60min plus to backup window        
        self.backup_duration = round(float(te - ts)/86400, 2) # backup duration in days
        
    def write_log(self):
        '''Write rman output to log        
        '''
        self.output_buff.seek(0)
        self.env.log_h.write(self.output_buff.getvalue())
        self.logger.info('See RMAN logs in file %s ' % self.env.log_file)
    
    def finalize(self):
        self.env.log_h.close()
    
    def run_db_backup(self):
        '''Execute database backup        
        '''
        self.build_scritps()
        cmd_line = "%s/bin/rman target / @%s" %  (self.conf.ora.home, 
                                                  self.env.db_scpt)
        self.run_script(cmd_line)        
        self.logger.debug('Run cmd line %s' % cmd_line)
    
    def run_archlog_backup(self):
        '''Execute archlog backup        
        '''
        if self.conf.rman.backup_type == 'ONLINE':
            self.build_scritps('arch')
            cmd_line = "%s/bin/rman target / @%s" % (self.conf.ora.home,
                                                     self.conf.rman.scpt_arch)
            self.run_script(cmd_line)  
            self.logger.debug('Run cmd line %s' % cmd_line)
                
    def run(self):
        '''Run all backup tasks            
        '''
        self.choose_bkp_type()
        
        self.run_db_backup()     
        self.run_archlog_backup()
    
        self.write_log()        
        self.finalize()
        
    
