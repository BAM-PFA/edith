how it will work:


*  jon inserts new tapes
* need a form to take in tape id A that will be applied to tape B, storing to tmp config file (??)
* this is in an interface to formatLTO, which should try to format both blank tapes or return error
* mounting LTO: given the current base LTO ID it should show mount status at /mnt/TAPEA and /mnt/TAPEB, and proceed with trying to mount at those points if tapes aren't mounted yet
* schema file should be written to local tmp/ dir
* Read the available space and store it to temp config file (??) ( look at `df` as used in writelto)
* write lto: 

* read contents of AIP dir, list aip uuid and size using folder_size function
* provide option to write each to lto
* compare total sizes avaiable with space left on tape
* if enough space is left run gcp to copy files
* run verify.py 
* display verified status, option to cleanup AIP folder
* unmount tapes from /mnt/TAPEID when all transfers are done
* schema file is updated at this point, so read in the .schema index file and for individual files in /objects dir select: 
  * file name
  * ltoID
  * path on tape
  * file size
  * modified time (?)
* for DPX select these attributes for the top folder only plus:
  * number of frames (# files in the folder)
  * probably some other stuff
* write each to the database... 

* use the ingest uuid to search resourcespace for the relevant object and add the A tape id to the record
* 

new config settings needed:
* AIP directory path, hostname, IP address
* lto tape id
* lto capacity