# MetaDataDumper
 This java project has a Command line interface for dumping metadata of files into json line file. The metadata is 
 read from tika.
 
## Requirements
  + JDK 7+
  + Maven v3+
  + Java Dependencies Retrieved via maven : tika-core, tika-parsers, tika-serializations
  
## Build 
  `mvn clean package assembly:single`
An executable jar with all dependencies should be produced in `target/*-jar-with-dependencies.jar`


## Run or Use 

`java -jar target/metadata-dumper*-jar-with-dependencies.jar -inputDir /path/to/input/ -output path/metadata.jsonl`

where `/path/to/input/` is root directory of all the files whose metadata needs to be dumped
      `path/metadata.jsonl` is path to output file

## Format of Metata data
path/to/file  \t:\t  {...json meta data...}
