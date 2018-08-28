# EDITH VERSION ROADMAP
## Version 0.x (Alpha)
### v0.0.5 : 
@ 5/2018

* Basic functions are almost all in place. 
* Missing:
  * Add lto id to rs record for ingested object
easy
  * Logging steps throughout `ingestSip` microservice
Easy but time consuming
  * Database reporting during same
    * Hard
    * Need to plan db writes carefully
    * Is each sql record insertion an object? Or is each query run directly?

### v0.1:
* Add missing steps listed above
* Debugging



### v0.2:
Release 8/20/2018
* Add audio ingests to pymm
* Treat image sequences as a single unit
* Add DPX ingest to pymm

### v0.3
* Read LTO index file on tape unmount 
  * And add entries to the pymm database
* Reading from LTO
  * Offer to list either A tape or B tape
  * List contents of selected tape
* Write files out to a directory on the server
* users can then FTP the files to a local machine (?)

### Version 0.4 
~~ ~~

## Version 1.x 
### v1.0:
* Versions 0.x are debugged
* UI improvements?

## Version 2.x:
### v2.0
* Add metadata form to ingest form per-object
  * This creates a csv that is kept with pymm object
  * To be used for non-pfa collection objects
  * Pull code from piction metadoodler
