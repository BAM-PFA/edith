# ingestfiles
This is a work in progress web interface bringing together several disparate elements as a suite of audiovisual digital preservation tools. 

First, on ingesting an audiovisual file, we create an Archival Information Package [\(following the OAIS conceptual model\)](https://en.wikipedia.org/wiki/Open_Archival_Information_System) for audiovisual files using [mediamicroservices](https://github.com/BAM-PFA/mm). The mediamicroservices AIP consists of a predefined folder structure containing the master file, its derivatives, and technical metadata about each file, including checksums. We have it create a derivative access copy that is appropriate for use in ResourceSpace. It also records each digital preservation step in a MySQL database. 

Along the way, we query the BAMPFA film collection's FileMaker database (our collection management system for the film collection) for metadata in cases where the original analog material has been accessioned into the BAMPFA collection. This is returned as JSON that is also sent to ResourceSpace along with the access mp4 file. 

The AIPs are then written to [Linear Tape Open (LTO)](https://en.wikipedia.org/wiki/Linear_Tape-Open), which is also indexed in the mediamicroservices MySQL database. This portion uses [`ltopers`](https://github.com/amiaopensource/ltopers), a package maintained by members of the Association of Moving Image Archivists (AMIA).

## Usage overview

* Select files to ingest. Enter a user ID to record as 'OPERATOR.' 
* Analyzing the filename, the FMP database is queried and metadata returned, or not, as the case may be.
* Access file is created and sent to RS along with metadata JSON. 
* AIP (including master, derivatives, checksums, and metadata) is prepared and stored on a local drive, awaiting LTO-ness. 
* Currently LTO write is done manually. Sounds like we want this run as a (weekly?)  `cron` job
### setup

mediamicroservices requires some configuration of input and output paths, database configuration (only need to do this once at setup). Installing via Homebrew gets all the dependencies installed too.

ResourceSpace has some setup requirements that are [documented](https://www.resourcespace.com/knowledge-base/systemadmin/install_macosx) on its website. Mostly just getting the Apache server settings correct and tweaking some of the PHP got it working.

Getting data from FileMaker requires ODBC to be correctly set up with the right driver and permissions.


## mediamicroservices

This suite of Bash scripts performs a variety of small tasks useful in archiving audiovisual files. The centerpiece is `ingestfile` which combines several of the microservices to create an AIP that contains XML and text files of metadata obtained using `ffprobe`, `mediainfo`, and some other similar scripts. There are also neat things like a .png file of a representation of the audio waveform. Who knew.

It also writes all the actions taken on the master file to a MySQL database (including user, original specs of the video, and file checksums) and creates logs of errors, `rsync` messages, etc.

I modified it somewhat to allow it to be run by a script instead of needing user input.


## FileMaker

Files that are digitized versions of works from the BAMPFA film collection include a portion of the original accession number in the filename. The script uses that number to query the film collection database and retrieve relevant descriptive metadata. 

## ResourceSpace

[ResourceSpace](https://www.resourcespace.com/) is an open-source digital asset management system that uses a PHP/MySQL web interface. It's very intuitive and responsive, and it allows for in-browser playback of videos using [VideoJS](http://videojs.com/). Metadata fields are totally customizable and accessible via the API.

The ResourceSpace API call post assets and metadata metadata at the same time. This required some modification of the API bindings in the RS code so that the file could be read from a local directory instead of a remote URL, as written. The ingest process SFTP's the proxy file to the server where the RS instance is hosted and RS has its own filestore that it uses. I have the filestore currently set to point to an attached RAID array.

## Proxies

mediamicroservices uses `ffmpeg` to transcode the derivative files, and I modified the `MIDDLEOPTIONS` in `makeresourcespace` to reflect our needed specs:

> `MIDDLEOPTIONS+=(-b:v 8000k -maxrate 10000k -bufsize 9000k)`

These options should probably be further constrained depending on whether the input is Standard Def or HD. This makes a *really* big file for a potentially poor, standard-def video transfer.

## LTO

This uses [`ltopers`](https://github.com/amiaopensource/ltopers) to write the AIP created by `ingestfile` to LTO tape. We use an HP 2-drive unit that we use to create a redundant backup, with tapes stored in separate locations.

The interface asks for a tapeID to be entered, but it also shows you the last one used so you can just confirm that there isn't a new one in.

When an AIP is written to LTO, there is an API call to ResourceSpace to grap the resource ID and push the LTO tape ID to that resource for searching in RS.

The contents of the LTO tapes are also updated and indexed in the mediamicroservices database.


## Some major unknowns/ to-dos

* Searching the database created by mediamicroservices. Maybe make a separate front end? I have looked at [Xataface](http://xataface.com/) as an option. **UPDATE** Xataface is ok, but ugly.
* Alert for an LTO tape that is getting full
* Recognizing formats/files that won't be in FileMaker and acting accordingly, e.g. audio files, videos made for event documentation
* Metadata Schemas for non-film-collection resources.
	* do we want to investigate PBCore as a blanket schema that can/could absorb everything?
* Explore a plugin to re-query Filemaker if the database record has changed


## Flask UI notes:

Tested on Ubuntu 16.04 and Mac (El Capitan and Sierra)

* Dependencies: 
  * Flask (pip3 install Flask)
  * flask_wff (pip3 install flask_wtf)
  * SQLAlchemy (pip3 install flask-sqlalchemy)
  * flask-login
  * paramiko (on Ubuntu `pip3 install -U paramiko` for correct Cryptography build)