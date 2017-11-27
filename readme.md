# ingestfiles
This is the start of a web interface to create Archival Information Packages for audiovisual files using [mediamicroservices](https://github.com/BAM-PFA/mm) and send a derivative access file to ResourceSpace along with a smattering of metadata from the BAMPFA FilemakerPro film collection management database. The AIPs are then written to LTO, which is indexed using the MySQL database built into the `mm` suite. 

I have been working on integrating this into ResourceSpace as a DAMS solution for BAMPFA's a/v assets, we'll see how it goes.

## Usage

* Select files to ingest. Analyzing the filename, the FMP database is queried and metadata returned, or not, as the case may be.
* Access file is created and sent to RS along with metadata JSON. 
* AIP (including master, derivatives, checksums, and metadata) is prepared and stored on a local drive, awaiting LTO-ness. 
* Currently LTO write is done manually. Sounds like we want this as a `cron` job
### setup

mediamicroservices requires some configuration of input and output paths, database configuration (only need to do this once at setup). Installing via Homebrew gets all the dependencies installed too.

ResourceSpace has some setup requirements that are [\(poorly\)](https://www.resourcespace.com/knowledge-base/systemadmin/install_macosx) documented. Mostly just getting the Apache server settings correct and tweaking some of the PHP got it working.

Getting data from FileMaker requires ODBC to be correctly set up with the right driver and permissions.


## mediamicroservices

This suite of Bash scripts performs a variety of small tasks useful in archiving audiovisual files. The centerpiece is `ingestfile` which combines several of the microservices to create an AIP that contains XML and text files of metadata obtained using `ffprobe`, `mediainfo`, and some other similar scripts. There are also neat things like a .png file of a representation of the audio waveform. Who knew.

It also writes all the actions taken on the master file to a MySQL database (including user, original specs of the video, frame and entire file checksums [I think?]) and creates logs of errors, `rsync` messages, etc.

I modified it somewhat to allow it to be run by a script instead of needing user input.


## FileMaker

Files that are digitized versions of works from the BAMPFA film collection include a portion of the original accession number in the filename. The script uses that number to query the film collection database and retrieve relevant descriptive metadata (I only have it running against a mock db now, which works well). 

This requires setting up ODBC for FileMaker (kind of a pain) and ideally a read-only account to be used just by this script.

## ResourceSpace

[ResourceSpace](https://www.resourcespace.com/) is an open-source digital asset management system that uses a PHP/MySQL web interface. It's very intuitive and responsive, and it allows for in-browser playback of videos using VideoJS. Metadata fields are totally customizable and accessible via the API... 

ResourceSpace has a (poorly documented) API that I used to post assets and metadata in the same call. This required some modification of the API bindings in the RS code so that the file could be read from a local directory instead of a remote URL, as written. The ingest process SFTP's the proxy file to the server where the RS instance is hosted and RS has its own filestore that it uses. I have the filestore currently set to point to an attached RAID array.

## Proxies

mediamicroservices uses `ffmpeg` to transcode the derivative files, and I modified the `MIDDLEOPTIONS` in `makeresourcespace` to reflect our needed specs:

> `MIDDLEOPTIONS+=(-b:v 8000k -maxrate 10000k -bufsize 9000k)`

These options should probably be further constrained depending on whether the input is Standard Def or HD. This makes a *really* big file for a potentially poor, standard-def video transfer.

## LTO

This uses [`ltopers`](https://github.com/amiaopensource/ltopers) to write the AIP created by `ingestfile` to LTO tape. We use an HP 2-drive unit that we use to create a redundant backup, with tapes stored in separate locations.

The interface asks for a tapeID to be entered, but it also shows you the last one used so you can just confirm that there isn't a new one in.


## Some unknowns/Major to-dos

* Searching the database created by mediamicroservices. Maybe make a separate front end? I have looked at [Xataface](http://xataface.com/) as an option. **UPDATE** Xataface is ok, but ugly.
* Alert for an LTO tape that is getting full
* Recognizing formats/files that won't be in FileMaker and acting accordingly
* Metadata Schemas for non-film-collection resources.
