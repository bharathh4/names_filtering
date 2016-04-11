Motivation:
Not all names need lexicons. This is a process which determines what names are not popular and lumenvox will use a bad rule. This process helps us avoid adding a lexicon for popular names like john or smith. The interface will need some API aesthetics cleanup. Feel free to get offended for blatant disregard for discriminating gets and posts!

Download the DB file from https://drive.google.com/open?id=0B4Wi34IOXmGhOWNBTXp2YjVFMWs and place it in freqest/db/

#################################################################
Run python flaskapp.py to start the server
Consume it as either

curl -F "file"=@names2.txt 
     -F "first_name_start"="0" 
     -F "first_name_end"="10000" 
     -F "first_name_threshold"="0.04" 
     -F "last_name_start"="0" 
     -F "last_name_end"="88000" 
     -F "last_name_threshold"="0.1" 
     'http://127.0.0.1:5000/extract/difficult_names'

where names2.txt has list of names in the following format.

bharath
john
smith
jesse
hagos
meselech

####################################################################

curl -F "first_name_start"="0" 
     -F "first_name_end"="10000" 
     -F "first_name_threshold"="0.04" 
     -F "last_name_start"="0" 
     -F "last_name_end"="88000" 
     -F "last_name_threshold"="0.1" 
     'http://127.0.0.1:5000/extract/difficult_name/meselch'

Returns a True indicating that this name (meselch) is not popular

curl -F "first_name_start"="0" 
     -F "first_name_end"="10000" 
     -F "first_name_threshold"="0.04" 
     -F "last_name_start"="0" 
     -F "last_name_end"="88000" 
     -F "last_name_threshold"="0.1" 
     'http://127.0.0.1:5000/extract/difficult_name/smith'

Returns a False indicating that this name (smith) is popular

#######################################################################


The params

-F "first_name_start"="0" 
-F "first_name_end"="10000" 
-F "first_name_threshold"="0.04" 

are essentially telling you to deem names with counts of less than 400 as not popular when passing thru firstname db

-F "last_name_start"="0" 
-F "last_name_end"="88000" 
-F "last_name_threshold"="0.1" 

are essentially telling you to deem names with rank more than 79200 as not popular when passing thru last name db

