__author__ = "Nii Mante"
__license__ = "MIT"
__version__ = "1.0.0"
__email__ = "nmante@usc.edu"
__status__ = "Development"
""" This program takes a set of N image, finds duplicate images in the set,
    and returns a set of deduplicated images"""

from nearDuplicate import NearDuplicate
from exactDuplicate import ExactDuplicate
import argparse
import os, sys, errno
from multiprocessing import Pool
import json
import shutil
import imghdr

def main():
    args = create_parser().parse_args()
    generate_output(args)
    
def create_parser():
    parser = argparse.ArgumentParser(description='This program takes a set of N images, finds duplicate images in the set, and returns a set of deduplicated images.')
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-e', '--exact_duplicates', action="store_true", default=True,
            help='Use this flag to deduplicate images via an "exact" deduplication methodology. Default behavior is to use exact duplicates.')
    group.add_argument('-n', '--near_duplicates', action="store_true", default=False,
            help='Use this flag to deduplicate images via a "near" deduplication methodology')
    parser.add_argument('dump_dir', help="The absolute path to your dump directory")
    parser.add_argument('-o', '--output_json', help="Write the locations and hashes of each deduplicated image to a JSON file. Defaults to 'image_locations.json'") 
    parser.add_argument('-d', '--output_dir', help="Output deduplicated images to directory. ")
    parser.add_argument('-s', '--show_duplicates', default=False, action="store_true", help="Use this flag to generate a directory which contains duplicates. Defaults behavior doesn't show duplicates." ) 
    parser.add_argument('-j', '--num_jobs', help="Number of worker threads to divide the deduplication. Defaults to 2. The more images the more jobs you should create", default=2, type=int)

    return parser

def is_image(filename):

    # First do a simple check for file extensions
    extensions = [".jpg", ".png", ".svg", ".tiff", ".jpeg"]
    for ext in extensions:
        
        if filename.endswith(ext):
            # Compare the file extension
            return True
        """
        elif imghdr.what(filename) != None:
            # If there's no extension, determine it by opening the file
            return True
        """

    # If necessary try opening the file with an image module
    # If there's an error opening it, then it's not an image so return false
    """
    try: 
        Image.open(filename)
    except: IOError:
        return False 
    """
    
    return False 

def find_all_images(dump_directory):
    """Find a list of images provided a root dump directory"""

    filenames = []
    for root, dirs, files in os.walk(dump_directory):
        for f in files:
            if is_image(f):
                 filenames.append(os.path.join(root,f))
    
    print >> sys.stderr, "Found %d images in directory: %s" % (len(filenames), dump_directory)
    return filenames

def exact_deduplicate_images(workerId, file_array):
    """Given a list of file names, return a dictionary of "exactly" deduplicated images"""
    
    # Use our custom class "ExactDuplicate"
    # It deduplicates a list of images, and stores the deduplicated images in an image_dictionary
    ed = ExactDuplicate(file_array)
    ed.deduplicate_images()
    return ed.image_dictionary

def near_deduplicate_images(file_array):
    """Given a list of file names, return a dictionary of "nearly" deduplicated images"""
    nd = NearDuplicate(file_array)
    nd.deduplicate_images()
    return nd.image_dictionary 

def partition_filenames(file_array, num_chunks=2):
    """ Given an array of file names, return "num_chunks" partitions"""

    for i in xrange(0, len(file_array), num_chunks):
        yield file_array[i:i+num_chunks]

def merge_dictionaries(dictionaries):
    """ Given an array of dictionaries, merge the dictionaries into 1 final result"""
    final_dict = {}
    for d in dictionaries:
        duplicate_keys = set(d).union(final_dict)
        for key in duplicate_keys:
            arr = final_dict.get(key, []) + d.get(key, [])
            final_dict[key] = arr
    return final_dict

def mkdir_p(directory):
    try:
        os.makedirs(directory)
    except OSError as exc:
        if exc.errno == errno.EEXIST and os.path.isdir(directory):
            pass
        else: raise

def create_output_image_directory(args, final_dictionary):
    """ Given a deduplicated set of images, as well as an initial dump dir,
        output the deduplicated images to an output directory"""

    if args.output_dir == None:
        return
    duplicate_dir = os.path.join( args.output_dir, '_duplicates')
    mkdir_p(args.output_dir)
    mkdir_p(duplicate_dir)
    
    for image_hash in final_dictionary:
        
        # Grab the file names from our image dictionary
        duplicate_image_array = final_dictionary[image_hash]
        src_path = duplicate_image_array[0]["filename"] 
        _, src_filename = os.path.split(src_path)
        dst_path = os.path.join(args.output_dir, src_filename) 

        # Copy image to new directory 
        shutil.copy2(src_path, dst_path) 
        

        # If we're interested in looking at duplicates
        # We examine the rest of the images in the duplicate array for this 
        # Image hash
        if len(duplicate_image_array) > 1 and args.show_duplicates:
            curr_duplicate_image_dir = os.path.join(duplicate_dir, image_hash)
            mkdir_p(curr_duplicate_image_dir)
            for index, dup_obj in enumerate(duplicate_image_array):
                _, dst_filename = os.path.split(dup_obj["filename"]) 
                dst_path = os.path.join(curr_duplicate_image_dir, str(index) + "-" + dst_filename)
                shutil.copy2(src_path, dst_path) 
            

    print >> sys.stderr, "Copied unique images from:\n --- %s --- to\n --- %s ---" % (args.dump_dir, args.output_dir)

    if args.show_duplicates:
        print >> sys.stderr, "Duplicates stored in: \n --- %s ---" % duplicate_dir

def generate_output(args):
    """ Main application Driver
        
        1. Partition filenames into smaller chunks/arrays of image filenames
        2. Generate worker processes
        3. Pass the chunks to the workers
        4. Each worker deduplicates it's set of image files 
        5. Merge the results from each worker to one python dictionary
        6. OPTIONAL -- Output the deduplicated image files to a directory 
    """
    # Find all image files in dump directory
    filenames = find_all_images(args.dump_dir)

    # Partition the list of filenames
    num_chunks = args.num_jobs 
    file_chunks = partition_filenames(filenames, num_chunks)

    # Create a pool of worker threads
    # Each worker will deduplicate a set of images
    pool = Pool(processes=num_chunks)

    # Pass the partitions to each thread
    results = []
    if not args.near_duplicates:
        results = [pool.apply_async(exact_deduplicate_images, args=(index,chunk,)) for index, chunk in enumerate(file_chunks)]
    else:
        results = [pool.apply_async(near_deduplicate_images, args=(chunk,)) for chunk in file_chunks]
    # Get the results from each worker
    dictionaries = [p.get() for p in results]

    # Merge the results into one dictionary
    final_dictionary = merge_dictionaries(dictionaries)

    print >> sys.stderr, "Number of images prior to deduplication: %d" % len(filenames)
    print >> sys.stderr, "Number of images after deduplication: %d" %  len(final_dictionary)
    
    # Write the image locations to an output file
    outfile_name = ""
    if args.output_json == None:
        outfile_name = "image_locations.json"
   
    print >> sys.stderr, "Writing to image dictionary to file: %s" % outfile_name
    with open(outfile_name, 'w') as outfile:
        json.dump(final_dictionary, outfile, indent=4)

    # Copy the images to an output directory
    create_output_image_directory(args, final_dictionary)

if __name__ == "__main__":
    main()
