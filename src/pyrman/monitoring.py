
import logging
import sys

KEY = 'ora.rman.success[%s]'

class Monitoring(object):
	def __init__(self, conf):
		self.conf = conf
		self.logger = logging.getLogger(self.conf.app_name)
		self.init_zabbix()

	def init_zabbix(self):
		try:
			import zabbix			
			self.system = zabbix.ZabbixSender(self.conf.monitoring.host,
											  self.conf.monitoring.port)
		except:
			self.logger.fatal('zabbix module not installed!: %s' % \
							  sys.exc_info()[0])
		else:
			self.logger.debug('zabbix module successfully imported!')

	def send(self, data):
		key = KEY % self.conf.ora.sid
		self.system.send(self.conf.monitoring.client_host,
						 key,
						 data)

if __name__ == '__main__':
	conf = ''
	mon = Monitoring(conf)
