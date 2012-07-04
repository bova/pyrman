run
{
allocate channel ch1 device type disk format '%BACKUP_PATH%/full_%d_%s_%T.bkp';
allocate channel ch2 device type disk format '%BACKUP_PATH%/full_%d_%s_%T.bkp';
#allocate channel ch2 device type disk format '/disk1/backup/psb1/psb1_%U.bkp';

# Hot backup
backup
 filesperset 10
 as compressed backupset
 full
 database;

# Switch redo log
sql'alter system switch logfile';

# Backup archivelogs
#backup archivelog
# from time 'sysdate-1/6'
# format '%BACKUP_PATH%/arch_%d_%s_%T.bkp';

# Backup controlfile
backup
current controlfile
format '%BACKUP_PATH%/ctl_%d_%s_%T.bkp';


# CrossCheck
crosscheck backup device type disk;
crosscheck archivelog all device type disk;

# Remove old backup
delete noprompt obsolete device type disk;
delete noprompt archivelog until time 'sysdate-14';
#DELETE NOPROMPT OBSOLETE RECOVERY WINDOW OF 7 DAYS device type disk;
}