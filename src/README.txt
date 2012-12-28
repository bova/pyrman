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

h2. Error 1

* RMAN-06207
* RMAN-06214: Datafile Copy   /oracle/11.2.0.3/dbs/snapcf_cebs.f

* delete obsolete;
ORA-19606: Cannot copy or restore to snapshot control file

h3. Solution

[ID 1215493.1]
crosscheck  controlfilecopy '/oracle/11.2.0.3/dbs/snapcf_cebs.f';
CONFIGURE SNAPSHOT CONTROLFILE NAME TO '/oracle/11.2.0.3/dbs/snapcf_cebs.f1';
delete obsolete;
CONFIGURE SNAPSHOT CONTROLFILE NAME TO '/oracle/11.2.0.3/dbs/snapcf_cebs.f';