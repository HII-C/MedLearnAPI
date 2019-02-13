set -a
source $1
set +a

# python3 server.py -u "student" -p $password -h "db01.healthcreek.org" -d "derived"
python3 server.py --user "root" --password $password --host "localhost" --db "derived"