#Image Deduplication In Python

#####Nii Mante

	usage: python main.py [-h] [-e | -n] [-o OUTPUT_JSON] [-d OUTPUT_DIR] [-s] dump_dir
	
	This program takes a set of N images, finds duplicate images in the set, and
	returns a set of deduplicated images.
	
	positional arguments:
	  dump_dir              The absolute path to your dump directory
	
	optional arguments:
	  -h, --help            show this help message and exit
	  -e, --exact_duplicates
	                        Use this flag to deduplicate images via an "exact"
	                        deduplication methodology
	  -n, --near_duplicates
	                        Use this flag to deduplicate images via a "near"
	                        deduplication methodology
	  -o OUTPUT_JSON, --output_json OUTPUT_JSON
	                        Write the locations and hashes of each deduplicated
	                        image to a JSON file
	  -d OUTPUT_DIR, --output_dir OUTPUT_DIR
	                        Output deduplicated images to directory.
	  -s, --show_duplicates
	                        Use this flag to generate a directory which contains
	                        duplicates.
	                        

##Overview

The purpose of this program is to deduplicate images. The program gives the option of deduplicating in two styles:

- Near duplicates
- Exact duplicates

##Examples

The program **requires** a directory of images. You don't need to worry about the structure of the folder (i.e. subdirectories). If there are images in the directory, the program will find it.

###Using Nutch?

If you're using Apatche Nutch, generate a dump directory

	# Merge segments from crawl
	bin/nutch mergesegs <MERGED_SEG_DIR_TO_CREATE> -dir <CRAWL_SEGMENTS_DIR>
	
	# Create a dump directory from that merged segment
	bin/nutch dump -segment <PREVIOUSLY_CREATED_MERGED_SEG_DIR> -outputDir <OUTPUT_DUMP_DIR_TO_CREATE>
	
This dump directory would be what you pass to the deduplication script.

	# Use the -s flag to also show duplicate images
	python main.py <PREVIOUSLY_CREATED_OUTPUT_DUMP_DIR> -d <DEDUP_IMAGE_DIR_TO_CREATE> -s

##Program Output

The program outputs a few things:

- **JSON** - JSON file which shows the file locations of deduplicated images, as well as the locations of the duplicates
- **Initial_Image_Count** - The number of images before the algorithm runs
- **Final_Image_Count** - The final number of images after deduplication
- **Images (OPTIONAL)** - If you choose, the program can conveniently put the deduplicated (and duplicate) images into an output folder









