-- Dependencies
1. confParsing
2. loggingTool
3. mailTool

-- NFS MOUNT
10.50.50.27:/backup/s253_iabs        /backup/iabs          nfs     defaults,user     0 0

-- For enable incremental backup
Alter Database Enable Block Change Tracking Using File '/oradata/fbs/data/bct.dbf';

-- Check status of change tracking
Select * from v$block_change_tracking

-- Setup controlfile autobackup to right path
CONFIGURE CONTROLFILE AUTOBACKUP FORMAT FOR DEVICE TYPE DISK TO '/backup/ctl_auto/%F.rman';

# PYBKP crontab entry
05 05 * * * sh /home/oracle/pybkp/pybkp.sh /home/oracle/pybkp/conf/pybkp_psb.conf >/tmp/pybkp_psb.log 2>&1

# RMAN Settings
CONFIGURE RETENTION POLICY TO REDUNDANCY 5;


# Problem during backup
# Possible solutions:
crosscheck archivelog all;
crosscheck backup;
delete expired;
delete force obsolete;