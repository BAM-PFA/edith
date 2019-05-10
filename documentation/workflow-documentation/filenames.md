# Filenames for EDITH

While we try to adhere to filename [standards](https://github.com/BAM-PFA/bampfa-workflows/tree/master/filenames) at BAMPFA, in the context of EDITH, some filenames are more critical than others. These are primarily instances where you expect to derive metadata about the object being ingested from one of the databases that we maintain.

Please also refer to the [documentation](complex_object_folder_structure.md) for the folder structure required for complex objects like multi-reel films or videos with multiple versions.


## DATABASE IDENTIFIERS
There are three main identifiers that could be present in a  filename:

### Database identifier
This is the 5-digit item identifier that is the last part of the PFA accession number (1604-01-**12345**). EDITH looks for this number to exist after an underscore, followed either by:
*  the end of the object's name (in the case of a folder being used to identify the object)
* a period followed by a file extension (in the case of a single file being ingested)
* another underscore with more text after it

Some examples are:
* A film scan folder being ingested with the item number included:
  * `schwechater_13186/`
* A single ProRes file being ingested:
  * `schwechater_13186_PM0027491_R01of01.mov`
* An audio recording with a record in the PFA Events (recordings) database:
  * `bampfa-audio_03107_agnes-varda.wav`

### PFA barcode
This is a barcode applied to a single reel or tape. It should follow the pattern **PM1234567**. It's used to identify an input object

* A film with no accession number, but with a barcode:
  * `schwechater_00000_PM0027491_R01of01.mov`
  * *Note that EDITH will still find the record even if the zeroed-out item number is not there. It's convenient to include the 5-zero placeholder for the item number, but it isn't a technical requirement.*
* A film scan folder with just the barcode:
  * `schwechater_PM0027491/`
    * `dpx/`
    * `schwechater_PM0027491.wav`

### FileMaker database record ID
In cases where a PFA collection work has no accession number and for whatever reason will not/does not now have a barcode, you can use the FileMaker internal record ID to search on. It is created automatically by FileMaker and should follow the pattern **ITM1234567**

* A film with no accession number or barcode:
  * `le-bonheur_00000_000000000_ITM0006097_R01of05/`
* Another one:
  * `la-pointe-courte_ITM0006098_R02of06.mov`

### Reel Number
This indicates the reel number in a sequence and should be present for all film transfers, even if there is only one reel. It should be formatted as `R01of01`, `R03of08`, etc. and comes as the last portion of the staff-entered file name (DPX files get an additional sequence number added by the scanner).

* A one-reel film scan:
  * `bop-scotch_17501_R01of01_0058016.dpx`
* A two-reel film scan:
  * `bright-college-years_06852_R01of02.mov`
  * `bright-college-years_06852_R02of02.mov`


## Versioning
We may (? 4/2019) also indicate versioning of in-house a/v in the filename.

### Platform
* ProRes master and h264 Instagram version:
  * `Exhibition_Art_Wall_Karabo_Poppy_Molesane_2018-02-05.mov`
  *  `Exhibition_Art_Wall_Karabo_Poppy_Molesane_2018-02-05_Instagram.mp4`

### Exhibition version
* `la-pointe-courte_ITM0006098_exhibition.mov`
