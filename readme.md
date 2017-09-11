# Ingest AIP 2 LTO & Send Proxy 2 ResourceSpace
This is a Python script that takes a folder of video files (in our case, digitized analog video and films scanned on a LaserGraphics Scan Station), creates an Archival Information Package using [mediamicroservices](https://github.com/BAM-PFA/mm) forked from CUNY Television, and sends a derivative H.264 proxy to ResourceSpace along with a smattering of metadata from the BAMPFA film collection management database. Next up will be writing part of this to write the AIP to Linear Tape Open (LTO7) drives for storage.

## Usage

The Python script is run from the command line currently, and the user is expected to drag a directory of video files to the terminal and enter some identifying credentials. If the files are named correctly there shouldn't need to be any other user input.

This is tested on Mac systems with Python 3 and FileMaker 12.

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

These options should probably be further constrained depending on whether the input is Standard Def or HD. This makes a *really* big file for a choppy video transfer.

## LTO (in progress)

This will use [`ltopers`](https://github.com/amiaopensource/ltopers) to write the AIP created by `ingestfile` to LTO tape. We use a Quantum 2-drive unit that we will use to create a redundant backup, with tapes stored in separate locations.

This script requires a tapeID to be entered, which I may set globally at the start of running the python script... ideally the tapeID will be part of the metadata JSON that gets sent to ResourceSpace so that you can search by tape or by resource metadata.



## Some unknowns
* At what point will the AIPs be written to tape? As a batch at the end of the ingest process? Per file? nightly via `cron` job?
* Searching LTO tapes. `ltopers` includes a mechanism to search the LTO tape indexes which are also written to the same MySQL database used by mediamicroservices (I think that's how it works?). I want to have the tape ID available in RS as well so that you can use that existing interface for a simple search or to see what tape(s) holds the master file.
* Searching the database created by mediamicroservices. Maybe make a separate front end? I have looked at [Xataface](http://xataface.com/) as an option.
* I haven't been able (allowed) to access or test our LTO drive. :(