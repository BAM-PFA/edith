# BETA EDITH WORKFLOWS

## Hi-level outline
All ingests will work basically the same, except that depending on the type of file ingested and the required output, different derivatives will be created. The main computers involved are:

* EDITH server (hosts ResourceSpace, does transcoding/packaging/checksumming, interfaces with LTO decks)
* Lasergraphics station: film scans are done here
* Video digitization rig: not currently on our network, just has huge storage and taxi drives
* 16-bay QNAP: Network Attached Storage used as first delivery point for digitized stuff

Here's the basic workflow:

1) Someone creates a source video file or a directory of files (video transfer, film scan, digitized audio, born digital AV)
2) The file(s) is transferred over the local network to our Enterprise QNAP NAS device.
3) When filenames (and directory structures, for DPX output) are verified manually, the master asset is copied into a watched folder, also on the QNAP. An `rsync` process running as a daemon copies the asset(s) to the EDITH server, running `--chmod=+rwx` on them in the process. *[nb- this is under revision ~12/2018]*
3) Through the ResourceSpace interface a user chooses assets to ingest that are sitting on the server RAID
4) As applicable, additional descriptive metadata can be added in the ingest menu. Filenames are parsed and the film collection DB is queried when a matching accesison # is found.
5) Each ingest/SIP that is created gets a UUID (128-bit unique ID like `52cc5488-0ad8-11e8-ba89-0ed5f89f718b`)
6) [`pymm`](https://github.com/BAM-PFA/pymm) does this stuff:

 i) transcodes derivatives

 ii) gets technical metadata & fixity data (checksums) on the source and derivs
 
 iii) packages all of this into a folder structure like so (a "SUBMISSION INFORMATION PACKAGE"/SIP):<br>
 **UUID**/<br>
&nbsp;&nbsp;&nbsp;&nbsp;objects/<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;files.mov<br>
&nbsp;&nbsp;&nbsp;&nbsp;metadata/ <br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;metadata-example.xml<br>
&nbsp;&nbsp;&nbsp;&nbsp;logs/ <br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;log.txt<br>

7) If required, `pymm` can send a ProRes copy back to the RAID for Dave to pick up and do post-processing on.
8) Code taken from [`ltopers`](https://github.com/amiaopensource/ltopers) allows a user to write SIPs to LTO, as well as formatting or ejecting tapes, as well as retrieving data from tape.
9) All these steps are recorded as they happen to a MySQL database created by `pymm`.

## (1) Film scan (prores master)

### one reel
* Projectionist scans a single reel and outputs a single ProRes file 
* It is an accessioned film so the filename includes a 5-digit sequence corresponding to the last section of the accession number (e.g. 1612-01-**12345**).
  * Or maybe it only has a barcode, so the filename includes the PM###### number  (example-title_00000_**pm001234**_R01-of-01.mov)
* Projectionist transfers the correctly named file to the QNAP.
* Jon performs basic QC/file existence check and changes filenames as needed. Moves correct file to QNAP watched folder.
* EDITH syncs the folder contents to the server RAID and deletes the extra copy on the QNAP.
* Jon goes to the ResourceSpace home screen and chooses the Ingest Files tab. He checks 'Run Ingest' for the files he wants to ingest and chooses the options that apply to each ingest:
  * Send a ProRes mezzanine to Dave's pick-up folder on the ~~QNAP~~ EDITH RAID.
* then he hits *__INGEST__*.

* `EDITH` does the following:
  * call `pymm`: 
  * create Universally Unique Identifier (UUID) for ingest process 
  * create UUID-named parent folder for SIP creation, with subfolders for file objects, metadata, and logs 
  * create low res proxy H264 
  * create technical metadata for all the file objects
  * create manifest for package
  * `mv` to AIP staging area
  * call to FileMaker based on accession number/barcode, if a match is found, post the low res proxy and descriptive metadata JSON to ResourceSpace
  * send ingest UUID to RS
* later that week `writeLTO.py` uses `ltopers` to write to LTO and sends the LTO tape ID to the relevant RS record

### multiple reels
* Gibbs outputs one ProRes file per reel, named as described above
* They go into a folder with the same naming convention, minus the reel-specific information such as barcode
* He transfers the folder to the QNAP
* Jon goes through RS interface to select folder that the projectionist created and selects options:
  * Do/don't concatenate reels to produce a single access file using [concatFiles.py](https://github.com/BAM-PFA/pymm/blob/master/concatFiles.py)
  * Do/Don't create a ProRes mezzanine file
  * Do/Don't send a mezzanine file to Dave

* hit _**INGEST**_
* `EDITH` does this:
  * call `pymm`
  * other steps as above
   * if the accession number portion of the filename is `00000` then grab the barcode off the first file in the folder
   * the proxies for each reel, and any concatenated version, are sent to a single RS record (Reel 1 shows up first and the rest are 'alternative files')
* write to LTO

## (2) Film scan (DPX master)

Basically the same as above ~~except that DPX can be transcoded to lossless FFV1 for space savings.... 
[read this blog post](https://kieranjol.wordpress.com/2016/10/07/introduction-to-ffv1-and-matroska-for-film-scans/) for some add'l info about FFV1 for film scans
Or we could keep the DPX as-is and output a ProRes for Dave. Or don't make a mezzanine by default... ?~~

We're considering options to reduce the transfer of so many small files. Top choices are TAR wrapping or RAWcooked, if funding and post-production workflows make sense. 

## (3) Video Transfer (ProRes master)

Same steps as film scans.
Questions: 
* Jon is currently capturing ProRes 4:2:2 HQ with the AJA card. 
* Is this output what Dave would take in for processing or would he want a different file?
* If we set up Dave's unused Mac Pro to replace the old MP tower Jon is using we could capture using [`vrecord`](https://github.com/amiaopensource/vrecord) to FFV1 and still create a ProRes file for processing
* Archivally this seems like a good option but there is no immediate need to change our current setup

## (4) Event/Lecture recording (ProRes master)
* Someone (Dave? Stephanie Smith?) transfers the file to the QNAP RAID
* File is named with basic metadata (date/name of significant person/band/etc) similar to Event images sent to Piction
* Ingest process is the same as above but choices selected are:
  * Don't send a ProRes copy to Dave
  
* There won't be a Filemaker record so descriptive metadata must be entered in the ingest menu.

## (5) New audio recording (WAV source file)
* Jason transfers the [correctly-named](https://docs.google.com/document/d/1gvPV2pyvgX9XgkxrmfKdFI4W6wJ48Z9RK451e4hhUDM/edit) WAV to the QNAP
* He enters the appropriate descriptive metadata 
* He selects the file and hits INGEST
* `pymm` does the same ingest process described as above except:
  * uses `bwfmetaedit` to embed  BAMPFA `<BEXT>` info and MD5 checksum for audio data
  * produces an mp3 derivative *[not implemented yet]*
* mp3 gets sent to RS and to Piction *[not implemented - need to find a way to use API call to FTP the proxy, similar to [Drive2Piction](https://github.com/BAM-PFA/Drive2Piction)]* 

## (6) Digitized audio recording (WAV source file)
* Student captures audio with `audiorecorder` (or using `audiorecorder2` at some point soon? We are changing our capture procedure as of 2/2018)
* Student transfers file to QNAP
* BAMPFA `<BEXT>` info and MD5 checksum are already present in the file
* Staff ingests the file as above 
* mp3 to RS and to Piction. 

----
## File formats in use
Here are file formats in use as of 12/2018. Some of this will shift, particularly how we handle DPX output, and DCP & DCDM born-digital acquisitions. 

| Type                   | Owning department(s) | Master file format(s)  | Access format |Notes|
|------------------------|----------------------|------------------------|---------------|---------------|
| Film scan              | Film Collection      | ProRes 4:2:2/DPX + PCM | H.264 in .mp4 ||
| Video transfer         | Film Collection      | ProRes 4:2:2           | H.264 in .mp4 ||
| DCP/DCDM                  | Film Collection      |                        |               |Not able to take in this format yet|
| Digitized cassette     | Library              | BWF                    | mp3           ||
| Event videorecording   | Digital Media/Comms? | ProRes 422             | H.264 in .mp4 ||
| Lecture videorecording | Digital Media        | ?                      |               ||
| Artist interview       | Comms?               | ProRes 422             | H.264 in .mp4 ||
| Promo video            | Comms?               |                        | H.264 in .mp4 ||
| PFA speaker recording  | Library              | BWF                    | mp3           ||
| Event audio recording  | Comms                | mp3                    | mp3           ||