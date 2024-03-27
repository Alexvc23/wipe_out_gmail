#!/bin/bash

source /Users/alex/Documents/programing/python/wipe_out_gmail/myenv/bin/activate

python3 /Users/alex/Documents/programing/python/wipe_out_gmail/clean_up_mail.py  delete_unread

python3 /Users/alex/Documents/programing/python/wipe_out_gmail/clean_up_mail.py delete_spam

python3 /Users/alex/Documents/programing/python/wipe_out_gmail/clean_up_mail.py delete_bin 
