# Enhanced Parsing with Tika and Tesseract-OCR

## Upgrading tika to newer version
Nutch 1.11 has pre-configured tika parser plugin which uses version 1.10 of tika-core. The current version of tika on
 its trunk at the time of writing (as of Oct. 11, 2015) is 1.11 (SNAPSHOT). Tika libraries are built from source
 to make use of latest improvements. The instructions for doing so is as follows:
 
### Build tika dependencies
  + Clone git repo `git clone git@github.com:apache/tika.git`
  + get inside the root of tika project: `cd tika`
  + Be sure to use trunk branch : `git checkout trunk`   # make sure on trunk branch
  + Be sure to confirm latest version : `git pull origin trunk`  # pull latest changes
  + Build and install to local repo : `mvn clean install`   # to skip tests, suffix `-skipTests` to the command

### Upgrading tika libraries in tika: 
  The previous step has created tika libraries with version `1.11-SNAPSHOT` and stored them in `$HOME/.m2/repository/`.
This step configures nutch build to use these new libraries. 

  + Edit `ivy/ivy.xml`, set tika version `1.11-SNAPSHOT`
  + Edit `src/plugin/parse-tika/ivy.xml` to upgrade tika version 
  + Edit `src/plugin/parse-tika/plugin.xml` to upgrade tika version
  + Previous tika build step installed the dependency in $HOME/.m2/repository. This step
configures ivy to use local maven directory (because 1.11-SNAPSHOT is not published to public repo)
  + Configure nutch build system to use SNAPSHOTS from `$HOME/.m2/repository/`. Edit `ivy/ivysettings.xml` with the
   following changes :
     * Set a property inside `<ivysettings>` tag by adding:
       `<property name="local-maven2-dir" value="file://${user.home}/.m2/repository/"/>`
     * Create a resolver inside `<resolvers>` tag by adding:
       `<ibiblio name="local-maven-2" root="${local-maven2-dir}" pattern="${maven2.pattern.ext}" m2compatible="true"/>`
     * update `internal` chain with following :
      `<chain name="internal" dual="true">
         <resolver ref="local-maven-2"/>
         <resolver ref="local"/>
       </chain>`
     * Inside `<modules>` tag  add: `<module organisation="org.apache.tika" name=".*" resolver="internal"/>`

  The file after edits is attached in submission zip.
  The above steps upgrades nutch to newer tika version. Rebuild nutch with the command:
    `ant runtime` 


## Install and test Tesseract-OCR
  For ubuntu :

  + Install : `sudo apt-get install tesseract-ocr`
  + Test : `tesseract  -psm 3 input/image.jpg output/text` # use an image which has text content to test

## Test tika integration with tesseract

+ Create a seed file having only urls to images which have text.
+ Perform a depth 1 crawl : `bin/crawl seed image_crawl 1`
+ Export crawl content to a text file (courtesy http://stackoverflow.com/a/10794335/1506477) : 
  `nutch readseg -dump image_crawl/segments/* dump-text \
      -nocontent -nofetch -nogenerate -noparse -noparsedata`
+ View text `cat dump-text/dump` 
   This should print “ParseText” extracted by parse-tika plugin with the help of tesseract.
   
