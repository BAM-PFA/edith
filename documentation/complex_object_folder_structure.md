# Folder structures for complex objects

Complex objects are basically anything other than a single file that is ingested. This can be two or more discrete AV files, discrete files that also contain a folder of documentation files with supplementary documentation, or something more complex like a folder with multiple reels of DPX+WAV film scans. The processing scripts that package assets for archiving require a certain folder structure in order to work properly and output the correct archival package.

Mostly, these folders should follow the same kind of pattern. The important point is that **the folder containing any component parts should be named for whatever you determine is the 'canonical' name for the whole**.

For example, with film scans, the component parts will contain individual reel barcodes and "R01of02"/"R02of02" phrases, but the enclosing folder will just be named for the title and the accession number that matches a database record, which in turn describes all the reels of the film.

Also, enclosing folders should only ever be one "level" deep, so all the files (or DPX+WAV folders) making up the whole should all be next to each other under the top level folder. In the same way, any documentation that is submitted should be directly under the top-level folder and it **must** be in a folder called `documentation`.

Here are some examples (lines with a `/` at the end represent folders; `--` represents one level deep):

## Two files that make up reels or parts of a whole

```
title-of-work_database-id-as-applicable/
-- title-of-work_database-id_reel-barcode_R01of02.mov
-- title-of-work_database-id_reel-barcode_R02of02.mov
```

## Two files without database records
```
title-of-work/
-- title-of-work_master.mov
-- title-of-work_instagram.mp4
```

## One file with documentation
```
title-of-work_database-id-as-applicable/
-- title-of-work_database-id_reel-barcode_R01of01.mov
-- documentation/
-- -- photo-of-reel-can.jpg
-- -- inspection-report.pdf
```

## Basic structure of DPX film scan folders
Film scans with DPX frames and a WAV file should at the least have one folder with the pertinent reel-specific information in the name, then the WAV file below it and a DPX folder named `DPX` or `dpx` **only**. The naming of the WAV file should **exactly** match the individual dpx file names up to the sequence number. For example:
* WAV file: `odalisque_15145_PM0164691_R01of01.wav`
* one DPX frame: `odalisque_15145_PM0164691_R01of01_0086880.dpx`

The basic folder structure looks like this:
```
odalisque_15145/
-- odalisque_15145_R01of01_PM0164691.wav
-- dpx/
-- -- odalisque_15145_R01of01_PM0164691_0086880.dpx
-- -- odalisque_15145_R01of01_PM0164691_0086881.dpx
-- -- etc.
```


## Three-reel film scan with documentation
```
chieko-sho_03783/
-- chieko-sho_03783_PM0050657_R01of03/
-- -- chieko-sho_03783_PM0050657_R01of03.wav
-- -- dpx/
-- -- -- chieko-sho_03783_PM0050657_R01of03_0086880.dpx
-- -- -- chieko-sho_03783_PM0050657_R01of03_0086881.dpx
-- -- -- etc.
-- chieko-sho_03783_PM0050657_R02of03/
-- -- chieko-sho_03783_PM0050657_R02of03.wav
-- -- dpx/
-- -- -- chieko-sho_03783_PM0050657_R02of03_0086880.dpx
-- -- -- chieko-sho_03783_PM0050657_R02of03_0086881.dpx
-- -- -- etc.
-- chieko-sho_03783_PM0050657_R03of03/
-- -- chieko-sho_03783_PM0050657_R03of03.wav
-- -- dpx/
-- -- -- chieko-sho_03783_PM0050657_R03of03_0086880.dpx
-- -- -- chieko-sho_03783_PM0050657_R03of03_0086881.dpx
-- -- -- etc.
-- documentation/
-- -- photo-of-reel-1_can.jpg
-- -- photo-of-reel-2_can.jpg
-- -- photo-of-reel-3_can.jpg
-- -- inspection-report.pdf
```
