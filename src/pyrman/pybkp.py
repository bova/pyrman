from __future__ import division
from datetime import datetime
from datetime import timedelta
import sys
import logging
import loggingTool
import os.path

import re
import mailTool

import rman
from conf import AppConf
from stat import Explorer, RMANLog




def gen_sh_scpt(tpl_data, repl_dict):
    for var, value in repl_dict.iteritems():
        tpl_data = re.sub(var, value, tpl_data)
    return tpl_data





if __name__ == "__main__":
    
    # Processing script's arguments
    try:
        conf_file = sys.argv[1]
    except:
        print "Usage:", sys.argv[0], "conf_file_path"
        sys.exit(1)   

    # Parse configuration file
    conf = AppConf(conf_file)
    
    logging.basicConfig(filename=conf.log_file, level=logging.DEBUG)
    logger = logging.getLogger(conf.app_name)
    
    
    rmaner = rman.Rman(conf)
    rmaner.run()
    
    expl = Explorer(rmaner.env.log_file)
    rman_files_frmt_info = expl.get_info()
    
    rman_log= RMANLog(rmaner.output_buff)

    
    mailer = mailTool.mailer(conf.smtp.host, 
                             conf.smtp.port, 
                             conf.smtp.user, 
                             conf.smtp.pwd, 
                             conf.smtp.rcpt)
    mailer.setOrgName(conf.app.org_name)
    # Erroneous case
    if rman_log.has_error():
        mailer.setSubject('[%s] pybackup: ERRORs(%d) during backup execution' %
                           (conf.ora.sid, rman_log.err_cnt))
        mailer.setBody('%s \n %s' %
                       (rmaner.output_buff.getvalue(), rman_files_frmt_info))
        # Send mail
        isSent = mailer.sendMail()
    

