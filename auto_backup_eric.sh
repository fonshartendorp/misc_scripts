#!/bin/bash

export PASSPHRASE='%1f0Ez0@h52'

# Daily incremental backup, weekly full backup
duplicity --full-if-older-than 1W /mnt/stack_eric file:///mnt/nas/tblisi/eric/backups/stack

if [ $? -eq 0 ]
then
  echo "Backup succesful"
  # Deleting all incremental backups older than 7 days
  duplicity remove-all-inc-of-but-n-full 7 --force file:///mnt/nas/tblisi/eric/backups/stack
  # Removing full backups older than 2 weeks
  duplicity remove-older-than 2W --force file:///mnt/nas/tblisi/eric/backups/stack
else
  echo "Backup not succesful"
  # TODO: send mail
fi

unset PASSPHRASE
