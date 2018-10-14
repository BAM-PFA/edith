# EDITH VERSION ROADMAP
## Version 0.x (Alpha)
### v0.0.5 : 
@ 5/2018

* Basic functions are almost all in place. 
* Missing:
  * Add lto id to rs record for ingested object
* Logging steps throughout `ingestSip` microservice
* Database reporting during same

### v0.1:
*skipped over these as releases*
* Add missing steps listed above
* Debugging

### v0.2:
Release 8/20/2018
* Add audio ingests to pymm
* Treat image sequences as a single unit
* Add DPX ingest to pymm

### v0.3:
Release 10/11/2018
* Adds metadata form for each object on the ingest screen
  * This data is added to the master metadata JSON object
  * Complete .json file is saved with the AIP
  * metadata is mapped to fields defined in ResourceSpace for display
* LTFS `index.schema` parsing for `pymm` database is implemented
  * `pymm` now parses DPX sequences as a unit of DPX folder and optional WAV file.
  * Records the WAV file and DPX folders as objects
  * Calculates the size of the DPX folder by summing all the component frames' `<length>` tags in the `.schema` file.

### v0.4
Release 10/13/2018
* Read LTO index file on tape unmount 
  * And add entries to the pymm database
* Reading from LTO
  * Offer to list either A tape or B tape
  * List contents of selected tape
* Write files out to a directory on the server
* Users can then FTP the files to a local machine (?)

#### v0.4.1
* Separate fields for metadata entry per object into tabs or accordion display
  * This is now (10/2018) just a big list of fields.


### Version 0.5
* improve UI/ feedback from various processes

### Version 0.6
* implement rsync daemon to get files to the `SHARED_DIR`

### Version 0.7
~~ ~~ ~~


## Version 1.x 
### v1.0:
* Versions 0.x are debugged
* UI improvements?

## Version 2.x:
### v2.0
* meh
