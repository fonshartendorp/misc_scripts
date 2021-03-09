#!/bin/bash

export PASSPHRASE='%1f0Ez0@h52'

# Daily incremental backup, weekly full backup
duplicity --full-if-older-than 1W --exclude /mnt/stack_fons/personal/Headspace --exclude /mnt/stack_fons/personal/videos /mnt/stack_fons file:///mnt/nas/tblisi/fons/backups/stack

if [ $? -eq 0 ]
then
  echo "Backup succesful"
  # Deleting all incremental backups older than 7 days
  duplicity remove-all-inc-of-but-n-full 7 --force file:///mnt/nas/tblisi/fons/backups/stack
  # Removing full backups older than 2 weeks
  duplicity remove-older-than 2W --force file:///mnt/nas/tblisi/fons/backups/stack
else
  echo "Backup not succesful"
  # TODO: send mail
fi

unset PASSPHRASE
