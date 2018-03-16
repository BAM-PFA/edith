# ingestfiles
This is a work in progress webapp for use in BAMPFA a/v digital preservation. It uses the Flask framework in a pretty basic way to 
1) provide archive staff with a few simple choices...

   * What file(s) to ingest into our digital preservation system(s)
   * What options to apply to the ingest process(es)


2) ... then act on those choices using scripts that:
   * gather descriptive and technical metadata
   * generate fixity benchmarks (and perform checks during file movement)
   * transcode derivatives
   * package resulting a/v files and metadata into OAIS Submission Information Packages (that are then written to LTO)
   * and post access copies and metadata to ResourceSpace for internal a/v digital asset management. 

## some details
First, on ingesting an audiovisual file, we create a Submission Information Package [\(following the OAIS conceptual model\)](https://en.wikipedia.org/wiki/Open_Archival_Information_System) for audiovisual files using [pymediamicroservices](https://github.com/BAM-PFA/pymm) (`pymm`). 

`pymm` is a python 3 port (a distillation? a rip-off?) of some core functionality in [mediamicroservices](https://github.com/mediamicroservices/mm), namely the package structure, metadata extraction, etc. `mm` does a lot more as of 3/2018 for file fixity checks, perceptual fingerprinting, a/v quality/conformance checking, etc., plus a plethora of derivative options. We're starting with the basics and are gonna assess what else we can/should/want to add once we are off the ground. There's a lot inspired by/stolen from the [Irish Film Archive](https://github.com/kieranjol/IFIscripts) in there too.

The pymm/mediamicroservices SIP consists of a predefined folder structure containing the master file, its derivatives, and technical metadata about each file, including checksums. `pymm` creates a derivative access copy that is appropriate for use in ResourceSpace and for research access. `pymm` copies the MySQL database structure used in `mm` to record [PREMIS](https://en.wikipedia.org/wiki/Preservation_Metadata:_Implementation_Strategies) events and file characteristics.

Along the way, we query the BAMPFA film collection's FileMaker database (our collection management system for the film collection) for basic descriptive metadata and technical information about analog source material in cases where the original has been accessioned into the BAMPFA collection. This is returned as JSON that is also sent to ResourceSpace along with the access mp4 file. 

The SIPs are then written to [Linear Tape Open (LTO)](https://en.wikipedia.org/wiki/Linear_Tape-Open), which is also indexed in the `mm` MySQL database. This portion uses [`ltopers`](https://github.com/amiaopensource/ltopers).

## Usage overview

* Select files/folders to ingest.
* Enter an email address that matches a predefined list of ResourceSpace accounts, used both to record the staff member doing the ingest, and to post to RS using their private RS API key. 
* Searching the filename for either an accession number or a barcode, the FileMaker database is queried and metadata returned, or not, as the case may be.
* Access file is created and sent to RS along with descriptive metadata JSON. 
* SIP (including master, derivatives, checksums, and metadata) is prepared and moved to a staging location, awaiting LTO-ness. 
* Currently LTO write is done manually. Sounds like we want this run as a (weekly?)  `cron` job

### setup
`pymm` requires some configuration of input and output paths, database configuration (only need to do this once at setup). There are a couple of non standard Python 3 libraries used.

ResourceSpace has some setup requirements that are [documented](https://www.resourcespace.com/knowledge-base/systemadmin/install_macosx) on its website. Mostly just getting the Apache server settings correct and tweaking some of the PHP got it working.

Previous iterations of `ingestfiles` used ODBC to connect to our FileMaker 13 database, but due to some constraints (FM doesn't provide an ODBC driver for Linux) I am now using the FileMaker XML API. It's... ok. We set up the FM Server to provide the XML Web Publishing API and our DBA created a FM view specifically for this purpose. Presumably if you (aka future me) want to reuse the ODBC code to perform more standard SQL queries on a less proprietary database, you can dig through the history to plug it back in.

### FileMaker
Files that are digitized/born digital works from the BAMPFA film collection include a portion of the original accession number in the filename. The script uses that number to query the film collection database and retrieve relevant descriptive metadata. We use '00000' to denote items that are not (yet) accessioned, so we can also search for a 9-digit barcode in a filename to query FM. If that fails, there is no uniqe ID to search in FM and we just set the descriptive metadata to null values.

[Here](https://fmhelp.filemaker.com/docs/13/en/fms13_cwp_xml.pdf) is the FileMaker 13 XML API documentation.... :(

### ResourceSpace
[ResourceSpace](https://www.resourcespace.com/) is an open-source digital asset management system that uses a PHP/MySQL web interface. It's very intuitive and responsive, and it allows for in-browser playback of videos using [VideoJS](http://videojs.com/). Metadata fields are totally customizable and accessible via the API.

The ResourceSpace API call post assets and metadata metadata at the same time. I have previously used SFTP to move files from a processing computer to the RS server and used a direct attached RAID as the RS filestore, but (fingers crossed) we will be using a large capacity internal RAID on our server and won't need to do a bunch of file transfers. Here's a cool RAID setup [tutorial](https://www.digitalocean.com/community/tutorials/how-to-create-raid-arrays-with-mdadm-on-ubuntu-16-04) for Ubuntu...

### Proxies
`pymm` uses `ffmpeg` to transcode the derivative access files, currently set to:

> `MIDDLEOPTIONS+=(-b:v 8000k -maxrate 10000k -bufsize 9000k)`

These options should probably be conditionally constrained based on input. This makes a *really* big file for a potentially poor, standard-def video transfer.

### LTO (under revision)
This uses [`ltopers`](https://github.com/amiaopensource/ltopers) to write the SIP created by `ingestfile` to LTO tape. We use an HP 2-drive unit that we use to create a redundant backup, with tapes stored in separate locations.

The interface asks for a tapeID to be entered, but it also shows you the last one used so you can just confirm that there isn't a new one in.

When an AIP is written to LTO, there is an API call to ResourceSpace to grap the resource ID and push the LTO tape ID to that resource for searching in RS.

The contents of the LTO tapes are also updated and indexed in the mediamicroservices database.

### Some major unknowns/ to-dos
* Searching the database created by mediamicroservices. Maybe make a separate front end? I have looked at [Xataface](http://xataface.com/) as an option. **UPDATE** Xataface is ok, but ugly.
* Alert for an LTO tape that is getting full
* Metadata Schemas for non-film-collection resources.
	* do we want to investigate PBCore as a blanket schema that can/could absorb everything? ([maybe](https://docs.google.com/spreadsheets/d/1pF6giZVXvgoqoy0bLwTezoDW7Ylpib8RKMxvNXhVxLI/edit?usp=sharing)?)
* Explore a plugin to re-query Filemaker if the database record has changed

### Flask UI notes:
The structure of the app is pretty basic. I have a lot (all) of the 'secret stuff' and all the configurable paths set up in an 'instance-specific' `config.py` file. This stuff could be stored in a database, along with an actual authentication module for staff. For the moment though, we only have a handful of users and making a database would be overkill.

Still deployed as dev, will be run on Apache in production.

## Dependencies
Tested on Ubuntu 16.04 and Mac El Capitan and Sierra.
* Runs on Python 3
* paramiko (on Ubuntu `pip3 install -U paramiko` for correct Cryptography build)
* `pymm` dependencies:
   * mediainfo
   * ffmpeg
   * ffmpy
   * xmltodict
   * Levenshtein
   * mysql connector/python
* Flask-specific dependencies: 
  * Flask (pip3 install Flask; gets core Flask dependencies automatically: wtforms, werkzeug)
  * flask_wtf (pip3 install flask_wtf)


  