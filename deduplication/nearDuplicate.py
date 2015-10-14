__author__ = "Nii Mante"
__license__ = "MIT"
__version__ = "1.0.0"
__email__ = "nmante@usc.edu"
__status__ = "Development"

"""
   This module contains methods to find near duplicate images.  
"""
import tika
#tika.initVM()
from tika import parser
import sys
import exifread
from PIL import Image
from simhash import Simhash, SimhashIndex

class NearDuplicate:
    def __init__(self, filenames, use_tika_meta=False, bit_distance=1):
        self.filenames = filenames
        self.use_tika_meta = use_tika_meta
        self.simhash_index = None 
        self.image_dictionary = {}
        self.k = bit_distance
        # Need to store the image hashes in some fashion
        # Possibly cluster the hashes (k-means) 
    
    def tika_metadata(self, filename):
        """Use the tika-py module to grab metadata for a file"""
        parsed = parser.from_file(filename)
        return parsed.get("metadata", {})

    def exifread_metadata(self, filename):
        """Use the exifread module to grab metadata for a file"""
        f = open(filename, 'rb')
        tags = exifread.process_file(f)
        return tags

    def generate_features(self, filename):
        """Given an image generate a feature vector"""

        # Grab the metadata for the image
        metadata = {} 
        
        features = []
        if self.use_tika_meta:
            # Use only metadata from tika
            metadata = self.tika_metadata(filename)
            feature_tags = ["Image Height", "Image Width", "File Size", "Content-Type"]
            features = [tag + ":" + metadata.get(tag,"NONE") for tag in feature_tags]
            return features

        """ 
            Let's create an additional feature which uses the image content
            For now, let's just hash the entire image
                We'll resize the image so it's normalized to a certain size

                Features to use
                    - color histogram
                    - image bytes of subregions

            We can take subregions of the image, and hash those
        """

        im = Image.open(filename)
        # Resize the image so all images are normalized
        width = im.size[0]
        height = im.size[1]
        resize_width = 40
        resize_height = resize_width*height/width
        im.resize((resize_width, resize_height), Image.ANTIALIAS)

        # Crop sub regions
        height_padding, width_padding = resize_height/5, resize_width/5
        box = (width_padding, height_padding, resize_width - width_padding, 
                resize_height - height_padding)
        sub_region = im.crop(box) 
        histogram_bytes = str(im.histogram()) 
        content_type = "image/" + str(im.format.lower())
        center_region_bytes = str(list(sub_region.getdata()))
        
        feature_weight_dict = {
                "Image Height" : 1, 
                "Image Width" : 1,
                "Image Histogram" : 3,
                "Content-Type" : 3,
                "Center Region Bytes" : 5 

        }
        metadata = {
                "Image Height" : str(width), 
                "Image Width" : str(height),
                "Image Histogram" : histogram_bytes,
                "Content-Type" : content_type,
                "Center Region Bytes" : center_region_bytes 
        }

        
        # Create a vector of metadata
        #features = [tag + ":" + metadata.get(tag,"NONE") for tag, weight in zip(feature_tags_weight_tuple,] 
        for (feature_tag, weight), (meta_tag, meta_value) in zip(feature_weight_dict.items(), metadata.items()):
            features.append((meta_tag + ":" + meta_value, weight))

        return features 


    def vector_similarity(self, vec1, vec2):
        # Generate similarity between two vectors

        # Jaccard similarity/ Cosine Similarity

        pass

    def merge_near_duplicate_dictionaries(self, nd):
        # Merge the current near duplicate instance with another instance
        smaller_nd = self if len(self.image_dictionary) <= len(nd.image_dictionary) else nd
        larger_nd = self if len(self.image_dictionary) > len(nd.image_dictionary) else nd
        final_dict = larger_nd.image_dictionary

        # Iterate over the smaller near duplicate instance
        for key in smaller_nd.image_dictionary.keys():
            

            # If an exact duplicate exists, just grab it and merge them 
            if larger_nd.image_dictionary.get(key, None) != None:
                print >> sys.stderr, "Exact dup found"
                arr = smaller_nd.image_dictionary.get(key, []) +\
                        larger_nd.image_dictionary.get(key, [])
                print >> sys.stderr, "Adding to dictionary"
                final_dict[key] = arr
                continue

            # Find the closest near duplicate in the larger dictionary by
            # using it's index
            print >> sys.stderr, "Getting simhash obj"
            simhash_obj = smaller_nd.image_dictionary[key][0]["hash_object"]

            print >> sys.stderr, "Getting near duplicate keys"
            near_duplicates_keys = larger_nd.simhash_index.get_near_dups(simhash_obj)
            
            # If a near duplicate exists 
            if len(near_duplicates_keys) > 0:
                # grab the array of images at that key in the larger dictionary
                # Merge it the array of images in the smaller dictionary 
                print >> sys.stderr, "Near duplicates exist"
                near_dup_key = near_duplicates_keys[0]
                arr = smaller_nd.image_dictionary.get(key, []) +\
                        larger_nd.image_dictionary.get(near_dup_key, [])

                # create an entry in the new dictionary
                final_dict[near_dup_key] = arr
                continue
                
            # Otherwise we should just add this key-object from the dictionary
            # to this array
            final_dict[key] = smaller_nd.image_dictionary[key] 

            # Add this simhash to the Index for efficient searching
            larger_nd.simhash_index.add(key, simhash_obj)

        self.image_dictionary = final_dict
        self.simhash_index = larger_nd.simhash_index

        nd.image_dicionary = final_dict
        nd.simhash_index = larger_nd.simhash_index

        # Now simply return this final dict 
        return final_dict


    def simhash_value_to_key(self, simhash):
        """Given a simhash object, convert it's value to a hexadecimal key 
            This key will be used in our image_file dictionary
        """
        return str(hex(simhash.value))


    def deduplicate_images(self):
        """
            Given a list of image files "self.filenames", deduplicate the images using
            near deduplication 
        """
        # Iterate through our files
        for image_file in self.filenames:
            # Create a list of features
            feature_array = self.generate_features(image_file)

            # Simhash this list of features
            sHash = Simhash(feature_array)
            if self.simhash_index == None:
                # First image, so we create the index add it to the dictionary
                # And move on to next iteration
                key = self.simhash_value_to_key(sHash)

                # We will use this index to speed up the process for finding
                # nearby simhashes
                self.simhash_index = SimhashIndex([(key, sHash)], k=self.k)
                self.image_dictionary[key] = [{
                    "filename" : image_file, 
                    "hash_key" : key, 
                    "hash_object": sHash
                }] 
                continue

            near_duplicates_keys = self.simhash_index.get_near_dups(sHash)

            if len(near_duplicates_keys) > 0:
                # There are duplicates, so we should add them to the corresponding entry
                # in the file dictionary

                # Get the key for the nearest duplicate image
                near_dup_simhash_key = near_duplicates_keys[0] 

                # Get the key for this current image 
                current_simhash_key = self.simhash_value_to_key(sHash) 

                # Create an object comprised of the image filename and key
                # We'll store this in a dictionary to be used in our merge step
                current_simhash_object = {
                    "filename" : image_file, 
                    "hash_key" : current_simhash_key,
                    "hash_object" : sHash
                }
                self.image_dictionary[near_dup_simhash_key].append(current_simhash_object)
            else:
                # No duplicates, so let's create an entry in our image filename dictionary
                key = self.simhash_value_to_key(sHash)

                # Add this simhash to the Index for efficient searching
                self.simhash_index.add(key, sHash)

                # Create an object in our image file dictionary
                self.image_dictionary[key] = [{
                    "filename" : image_file, 
                    "hash_key" : key,
                    "hash_object" : sHash
                }]

