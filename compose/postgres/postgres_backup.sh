#!/bin/bash

TIMESTAMP=%d-%m-%Y-%T
DELDATE=`date --date="-7 day" +${TIMESTAMP}`
DateTimeStamp=$(date +${TIMESTAMP})
HHOME=/home/pycon
if [ "$2" != "" ]; then
	BackupFileName=$2
else
	BackupFileName=tuteria_backup.sql.gz
fi
DROPBOX_UPLOADER=${HHOME}/dropbox_uploader.sh
TIMESTAMPED_BACKUPFILE=${DateTimeStamp}_${BackupFileName}
BACKUP_DIR=${HHOME}/backups

# Backup database from docker container
PGPASSWORD=$1 pg_dump --host=localhost -p 5433 -U pyconnigeria pyconnigeria | gzip -c  > ${BACKUP_DIR}/${TIMESTAMPED_BACKUPFILE}

# Upload to dropbox
$DROPBOX_UPLOADER -f ${HHOME}/.dropbox_uploader upload ${BACKUP_DIR}/${TIMESTAMPED_BACKUPFILE} .
$DROPBOX_UPLOADER -f ${HHOME}/.dropbox_uploader delete ${DELDATE}_${BackupFileName}

rm -rf ${BACKUP_DIR}/${TIMESTAMPED_BACKUPFILE}

