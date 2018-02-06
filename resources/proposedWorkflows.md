# PROPOSED RESOURCESPACE WORKFLOWS

## Hi-level outline
All ingests will work basically the same, except that depending on the type of file ingested and the required output, different derivatives will be created.

1) Someone creates a source video file or a directory of files (video xfer or film scan)
2) The file(s) is transferred over the local network to our NAS (QNAP).
2) Through the RS interface someone chooses the files to ingest that are sitting on the QNAP
3) Each ingest/SIP that is created gets a UUID (128-bit unique ID like `52cc5488-0ad8-11e8-ba89-0ed5f89f718b`)
3) [`mediamicroservices`](https://github.com/mediamicroservices/mm) or [`pymm`](https://github.com/BAM-PFA/pymm) does this stuff:
 i) transcodes derivatives
 ii) gets technical metadata & fixity data (checksums) on the source and derivs
 iii) packages all of this into a folder structure like so (a "SUBMISSION INFORMATION PACKAGE"/SIP):
 > UUID/
 > ____objects/
 > _________files.mov
 > ____metadata/ 
 > ________metadata-example.xml
 > ____logs/ 
 > ________log.txt

4) If required, `mm` can send a ProRes copy back to the QNAP for Dave to pick up and do post-processing on.
4) [`ltopers`](https://github.com/amiaopensource/ltopers) writes SIPs to LTO on a regular basis. Think this is where you call a SIP an AIP
6) All these steps are recorded as they happen to a MySQL database set up through `mm`.

## (1) Film scan (prores master)

### one reel
* Gibbs scans a single reel and outputs a single ProRes file 
* It is an accessioned film so the filename includes a 5-digit sequence corresponding to the last section of the accession number (e.g. 1612-01-**12345**).
  * Or maybe it only has a barcode, so it includes the PF###### number 
* Gibbs transfers the correctly named file to the QNAP drive.
* Jon goes to the ResourceSpace home screen and chooses the Ingest Files tab. He chooses the file from the selection pane (THIS DOES NOT EXIST YET!!) and chooses the options that apply to this ingest:
  * Do/Do not send a ProRes mezzanine to Dave's pick-up folder on the QNAP
  * 
* then he hits *__INGEST__*.

* `ingestfiles.py` does the following:
  * call `mm`: 
    * create UUID for ingest process (THIS DOES NOT EXIST YET!!)
    * create UUID-named parent folder for SIP creation, with subfolders for file objects, metadata, and logs 
    * `rsync` the source file to the Linux jalopy machine for transcoding.
    * [on jalopy] create low res proxy H264, create ProRes proxy if needed
    * `rsync` the proxy/proxies back to the host machine in the right folder
    * create technical metadata for all the file objects
    * create manifest for package
    * `rsync` to AIP staging area
  * call to FileMaker based on accession number/barcode, if a match is found, post the low res proxy and descriptive metadata JSON to ResourceSpace
  * send ingest UUID along w descriptive metadata (THIS DOES NOT EXIST YET!!)
* later that week `writeLTO.py` uses `ltopers` to write to LTO and sends the LTO tape ID to the relevant RS record 

### multiple reels
* Gibbs outputs one ProRes file per reel, named as described above
* They go into a folder with the same naming convention, minus the reel-specific information such as barcode
* He transfers the folder to the QNAP
* Jon goes through RS interface to select folder that Gibbs created and selects options:
  * losslessly concatenate reels into a single Matroska container using something like [this](https://github.com/kieranjol/IFIscripts#concatpy) (THIS DOES NOT EXIST YET!!)
  * Do/Don't send concatenated file to Dave for post-processing
  * 
* hit _**INGEST**_
* `ingestfile.py` does this:
  * call `mm`:
    * concatenate reels, verify losslessness
    * other steps as above
    * a single _lrp is created per directory, so there's just one RS record for the group of reels.
  * grab metadata from Filemaker
    * if the accession number portion of the filename is `00000` then grab the barcode off the first file in the folder
* write to LTO on schedule

## (2) Film scan (DPX master)

Basically the same as above except that DPX can be transcoded to lossless FFV1 for space savings.... 
[read this blog post](https://kieranjol.wordpress.com/2016/10/07/introduction-to-ffv1-and-matroska-for-film-scans/) for some add'l info about FFV1 for film scans
Or we could keep the DPX as-is and output a ProRes for Dave 

## (3) Video Transfer (ProRes master)

Same as one-reel film scan. 
Questions: 
* Jon is currently capturing ProRes 4:2:2 with the AJA card. 
* Is this output what Dave would take in for processing or would he want a smaller file?
* If we set up Dave's unused Mac Pro to replace the old MP tower Jon is using we could capture using [`vrecord`](https://github.com/amiaopensource/vrecord) to FFV1 and still create a ProRes file for processing
* Archivally we 'ought' to be doing this but there is no immediate need. 

## (4) Event/Lecture recording (H264 master (¿?))
* Someone (Dave?) transfers the file to the QNAP
* File is named with basic metadata (date/name of significant person/band/etc) similar to Event images sent to Piction
* Ingest process is the same as above but choices selected are:
  * Don't send a ProRes copy to Dave
  * 
* There won't be a Filemaker record so either don't query FM or just send blank JSON to RS for record creation (currently the latter happens).

## (5) New audio recording (WAV source file)
* Jason transfers the correctly-named WAV to the QNAP
* He selects the file and hits INGEST
* `pymm` (I don't think `mm` is set up to this) does the same ingest process described as above except:
  * uses `bwfmetaedit` to embed  BAMPFA `<BEXT>` info and MD5 checksum for audio data
  * produces an mp3 derivative
* [HAVE TO FIGURE OUT HOW TO REDUCE DATA ENTRY LOAD FOR JASON TO ENTER MD FOR PICTION]
* mp3 gets sent to RS and to Piction (THIS DOES NOT EXIST YET!!)
* 

## (6) Digitized audio recording (WAV source file)
* Student captures audio (using `audiorecorder2` at some point soon? We are changing our capture procedure as of 2/2018)
* Student transfers file to QNAP
* BAMPFA `<BEXT>` info and MD5 checksum are already present in the file
* Staff ingests the file 
* Still have to figure out how to reduce data entry load for descriptive metadata  
  * idea: have a form similar to [piction-metadoodler](https://github.com/BAM-PFA/piction-metadoodler) that produces JSON for RS and a csv for Piction use.
* mp3 to RS and to Piction.