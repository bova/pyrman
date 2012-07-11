'''
Created on 18.03.2012

@author: vladandr
'''

import fido_common.confparsing as confparsing
import os

TPL_DIR = "rman_tpl"
RUN_DIR = "run"
LOG_DIR = "log"

IS_TRUE = lambda val: val in ('True', 'true', 'Yes', 'yes')


class App(object):
    '''Holds app configuration
    '''
    home = ''
    tpl_path = ''
    run_path = ''
    log_path = ''
    org_name = ''


class Oracle(object):
    '''Holds oracle configuration
    '''
    home = ''
    sid = ''
    
    
class Backup(object):
    '''Holds backup configuration
    '''
    path = ''               
    retention = ''               
    is_allways_full = ''


class RMAN(object):
    '''Holds rman configuration
    '''
    backup_type = ''
    tpl_full = ''            
    tpl_incr = '' 
    tpl_arch = ''           
    full_bkp_day = ''
    scpt_full = ''
    scpt_incr = ''


class SMTP(object):
    '''Holds Mail configuration
    '''
    host = ''
    port = ''
    user = ''
    pwd = '' 
    rcpt = ''


class Monitoring(object):
    '''Holds configuration of monitoring system like Zabbix
    '''
    system = ''
    host = ''
    port = ''
    is_enabled = False



class AppConf(object):
    '''Configuration module    
    '''
    app_name = 'pybkp'    

    def __init__(self, conf_file):
        self.conf_file = conf_file
        self.log_file = ''
        self.log_level = ''
        
        confparsing.setRunConfFile(run_file=self.conf_file)
        self.run_conf = confparsing.RuntimeConfParser()
        
        self.app = App()
        self.ora = Oracle()
        self.bkp = Backup()
        self.rman = RMAN()
        self.smtp = SMTP()
        self.monitoring = Monitoring()
 
        self.parse()       
    
    def init_app(self):
        '''Init variables that define app configuration        
        '''
        self.app.home = self.run_conf.getRunOption('app', 'pybkp_home', '')
        self.app.tpl_path = os.path.join(self.app.home, TPL_DIR)
        self.app.run_path = os.path.join(self.app.home, RUN_DIR)
        self.app.log_path = os.path.join(self.app.home, LOG_DIR)
        self.app.org_name = self.run_conf.getRunOption('app', 'org_name', '')
        return True
        
    def init_oracle(self):
        '''Init Oracle config variables
        '''        
        self.ora.home = self.run_conf.getRunOption('ORA', 'oracle_home', '')
        self.ora.sid = self.run_conf.getRunOption('ORA', 'oracle_sid', '')

    def init_backup(self):
        '''Init varables that define backup configuration        
        '''
        # backup, RMAN config variables
        self.bkp.path = self.run_conf.getRunOption('backup', 
                                                   'backup_path', '/backup')
        self.bkp.retention = self.run_conf.getRunOption('backup', 
                                                        'backup_retention', 
                                                        3, 'int')
        self.bkp.is_allways_full = self.run_conf.getRunOption('backup', 
                                                          'is_allways_full', 
                                                          'True')
        self.bkp.is_allways_full = IS_TRUE(self.bkp.is_allways_full)
        
    def init_rman(self):
        '''Init variables that define configuration of RMAN        
        '''   
        self.rman.backup_type = self.run_conf.getRunOption('rman', 
                                                           'backup_type', 
                                                           'ONLINE')
        self.rman.backup_type = self.rman.backup_type.upper()
        
        if self.rman.backup_type == 'ONLINE':
            self.rman.tpl_full = 'full_db.tpl'
            self.rman.tpl_incr = 'incr_db.tpl'
        else:
            self.rman.tpl_full = 'full_db_offline.tpl'
            self.rman.tpl_incr = 'incr_db_offline.tpl'
        
        self.rman.tpl_arch = 'arch.tpl'
        self.rman.full_bkp_day = self.run_conf.getRunOption('rman', 
                                                            'full_bkp_day', 
                                                            'Friday')

        self.rman.scpt_full = os.path.join(self.app.run_path, 
                                           "full_db_%s.rman" % self.ora.sid)
        self.rman.scpt_incr = os.path.join(self.app.run_path, 
                                           "incr_db_%s.rman" % self.ora.sid)      
        self.rman.scpt_arch = os.path.join(self.app.run_path,
                                           "arch_%s.rman" % self.ora.sid)
    
    def init_smtp(self):
        '''Init variables that define SMTP configuration        
        '''
        self.smtp.host = self.run_conf.getRunOption('mailer', 'smtp_host', '')
        self.smtp.port = self.run_conf.getRunOption('mailer', 
                                                    'smtp_port', '25', 'int')
        self.smtp.user = self.run_conf.getRunOption('mailer', 'smtp_user', '')
        self.smtp.pwd = self.run_conf.getRunOption('mailer', 'smtp_pass', '')
        self.smtp.rcpt = self.run_conf.getRunOption('mailer', 'smtp_rcpt', '')

    def init_log(self):
        '''Init log configuration        
        '''
        self.log_file = os.path.join(self.app.log_path, '%s_%s.log' %
                                     (self.app_name, self.ora.sid))
        self.log_level = self.run_conf.getRunOption('logging', 
                                                    'log_level', 'DEBUG')

    def init_monitoring(self):
        self.monitoring.system = self.run_conf.getRunOption('monitoring',
                                                            'system',
                                                            'zabbix')
        self.monitoring.host = self.run_conf.getRunOption('monitoring',
                                                          'host', '')
        self.monitoring.port = self.run_conf.getRunOption('monitoring',
                                                          'port', 
                                                          10051,
                                                          'int')
        self.monitoring.is_enabled = self.run_conf.getRunOption('monitoring',
                                                                'is_enabled',
                                                                'True')
        self.monitoring.client_host = self.run_conf.getRunOption('monitoring',
                                                                 'client_host',
                                                                 '')

    def parse(self):        
        '''Parse configuration file and initialize all variables        
        '''
        self.run_conf.readConf()
        
        self.init_app()
        self.init_oracle()
        self.init_backup()
        self.init_rman()
        self.init_smtp()
        self.init_log()
        self.init_monitoring()


        

