# EDITH VERSION ROADMAP
## Version 0.x (Alpha)
### Version 0.0.5 :
@ 5/2018

* Basic functions are almost all in place.
* Missing:
  * Add lto id to rs record for ingested object
* Logging steps throughout `ingestSip` microservice
* Database reporting during same

### Version 0.1:
*skipped over these as releases*
* Add missing steps listed above
* Debugging

### Version 0.2:
Release 8/20/2018
* Add audio ingests to pymm
* Treat image sequences as a single unit
* Add DPX ingest to pymm

### Version 0.3:
Release 10/11/2018
* Adds metadata form for each object on the ingest screen
  * This data is added to the master metadata JSON object
  * Complete .json file is saved with the AIP
  * metadata is mapped to fields defined in ResourceSpace for display
* LTFS `index.schema` parsing for `pymm` database is implemented
  * `pymm` now parses DPX sequences as a unit of DPX folder and optional WAV file.
  * Records the WAV file and DPX folders as objects
  * Calculates the size of the DPX folder by summing all the component frames' `<length>` tags in the `.schema` file.

### Version 0.4
Release 10/13/2018
* Read LTO index file on tape unmount
  * And add entries to the pymm database
* Reading from LTO
  * Offer to list either A tape or B tape
  * List contents of selected tape
* Write files out to a directory on the server
* Users can then FTP the files to a local machine (?)

#### Version 0.4.1
Release 11/19/2018
* Separate fields for metadata entry per object into tabs or accordion display

### Version 0.4.2
Release 2019/02/18
* Logic fixes
* Add license

## Version 1.x
### Version 1.0:
Released 2019/02/18
* Implements database-backed User, Admin, Authentication modules.
* User feedback is improved with message flashing

### Version 1.1:
Released 2019/04/17
* Refactor ingests using Object-Oriented approach.
  * Ingests are now an object, with each item being ingested represented by a separate object.
* Metadata fields are now defined in the database, with metadata processes controlled by a Metadata object per item.

### Version 1.2
* Refactor LTO functions

### Version 1.3
* implement rsync daemon to get files to the `SHARED_DIR`

## Version 2.x:
### Version 2.0
* Implement task queue to offload long running processes to background jobs
* Allow monitoring of job progress/status
* Schedule processes to follow first-in-first-out pattern
