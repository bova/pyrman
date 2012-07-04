run
{
allocate channel ch1 device type disk format '%BACKUP_PATH%/full_%d_%s_%T.bkp';
allocate channel ch2 device type disk format '%BACKUP_PATH%/full_%d_%s_%T.bkp';

# Backup archivelogs
backup archivelog
 from time 'sysdate-%BACKUP_DURATION%'
 format '%BACKUP_PATH%/arch_%d_%s_%T.bkp';

# Backup controlfile
backup
current controlfile
format '%BACKUP_PATH%/ctl_%d_%s_%T.bkp';

}