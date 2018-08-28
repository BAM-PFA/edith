# EDITH VERSION ROADMAP
## Version 0.x (Development)
### Version 0.0.5 : current development as of 5/2018

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

### Version 0.1:
* Add missing steps listed above
* Debugging



### Version 0.2:
* Add audio ingests to pymm
* Read LTO index file on tape unmount 
  * And add entries to the pymm database
* Treat image sequences as a single unit

### Version 0.3
* Reading from LTO
  * Offer to list either A tape or B tape
  * List contents of selected tape
* Write files out to a directory on the server
* users can then FTP the files to a local machine (?)

### Version 0.4 
* Add DPX ingest tp pymm

***
## Version 1.x 
### Version 1.0:
* Versions 0.x are debugged
* UI improvements

### Version 1.1:
* Add metadata form to ingest form per-object
  * This creates a csv that is kept with pymm object
  * To be used for non-pfa collection objects
  * Pull code from piction metadoodler

