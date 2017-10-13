cd /Users/exhibits/src/earth-latest-data/

# Download and format yesterday's data...
# Get yestday's date as string
PREVDAY=`date -v-1d +%F`
# Remove dashes
PREVDAYFORMATTED=${PREVDAY//[-._]/}

./wind.py --date $PREVDAYFORMATTED

# Download and format today's data...
# (Passing no date default's to today)
./wind.py

cd /Users/exhibits/src/wind
nohup node dev-server.js 8090 &
cd ~/bin/stele
./browser.py
