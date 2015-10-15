
# Getting started with Apache Nutch

This guide walks through setup process of Apache Nutch powered image crawler which we used for fetching nearly a million
images for CSCI-572 Course assignment 1 of USC.
This guide uses Nutch 1.x (version 1.11 at the time of writing) and edits configurations to 
meet the requirements stated in http://sunset.usc.edu/classes/cs572_2015b/CS572_HW_NUTCH_WEAPONS.pdf

**Assumptions :**
 
   1. Operating Environment : Latest version of ubuntu operating system and Oracle JDK 8
   2. Tools which are required are assumed to be present or installed on the fly with `sudo apt-get install X` 
        when needed. Some of these include : Git, Ant, Maven.. 

## 1. Building Nutch from source code
 
 1.1) Clone a git repo :
 
    git clone git@github.com:apache/nutch.git
    cd nutch

 1.2 Build :
 
    ant runtime
   ant produces builds for local and distributed environments. This exercise uses local build present at `runtime/local`.
 
 1.3) Tweaking Config Files to prepare for first crawl:
    
   As per Nutch's conventions, the default configurations are found at `conf/nutch-default.xml`.
   Any tweaks made to configuration is to be placed in `conf/nutch-site.xml`. The following edits are to be made:  
    a) Set user agent :
      
      ```
       <property>
          <name>http.agent.name</name>
          <value>Apache Nutch/1.11 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) USC CSCI-572 Fall-15 Group-36 Member-1</value>
        </property>
      ```