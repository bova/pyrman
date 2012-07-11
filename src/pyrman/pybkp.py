from __future__ import division
from datetime import datetime
from datetime import timedelta
import sys
import logging
import fido_common.loggingtool as loggingtool
import os.path

import re
import fido_common.mailtool as mailtool

import rman
from conf import AppConf
from stat import Explorer, RMANLog
import monitoring



def gen_sh_scpt(tpl_data, repl_dict):
    for var, value in repl_dict.iteritems():
        tpl_data = re.sub(var, value, tpl_data)
    return tpl_data


def main():
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

    
    monitor_system = monitoring.Monitoring(conf)

    mailer = mailtool.Mailer(conf.smtp.host, 
                             conf.smtp.port, 
                             conf.smtp.user, 
                             conf.smtp.pwd, 
                             conf.smtp.rcpt)
    mailer.setOrgName(conf.app.org_name)
    # Erroneous case
    if rman_log.has_error():
        monitor_system.send('0')
        logger.debug('Message send to monitoring system (%s)' % \
                    conf.monitoring.system)
        mailer.setSubject('[%s] pybackup: ERRORs(%d) during backup execution' %
                           (conf.ora.sid, rman_log.err_cnt))
        mailer.setBody('%s \n %s' %
                       (rmaner.output_buff.getvalue(), rman_files_frmt_info))
        # Send mail
        isSent = mailer.sendMail()
    else:
        monitor_system.send('1')
        logger.debug('Message sent to monitoring system (%s)' % \
                    conf.monitoring.system)
    



if __name__ == "__main__":
    main()
    
