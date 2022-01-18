# Earth Map data download script

This is a script to download and process wind data for cambecc's fantastic D3
global map of environmental data. This is part of our effort to use this system
in a museum exhibit at the Conner Prairie Interactive History Park.

This is a work in progress and is [customized to our specific
needs](https://github.com/scimusmn/earth) right now, although I hope to abstract
it more in the future.

# Requirements
## grib2json
grib2json is a Java application that converts the GRIB data files from NOAA into the JSON files that we need for the wind app.

The install documentation for grib2json is a little sparse. Generally follow these steps to get this application to work on the exhibit systems.

- Install the [latest JAVA SDK](https://www.oracle.com/technetwork/java/javase/downloads/jdk12-downloads-5295953.html)
- Install Maven with homebrew `brew install maven`
- Clone the grib2json repo `git clone https://github.com/cambecc/grib2json.git`
- In that folder run the maven package command to build the software `mvn package`
- This will create a archive. Open that and move the contents to your `/Applications` folder

## Python 3
Older versions of this script ran on Python 3. Since we're installing Python 3 by default now we updated the script to work with that.

### Python > docopt
Install with:

    pip install docopt
