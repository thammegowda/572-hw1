#!/bin/sh

exact_out_dir=test_output_exact_deduplicated_images
near_out_dir=test_output_near_deduplicated_images
img_dir=test_images

rm -rf $exact_out_dir
rm -rf $near_out_dir

echo "EXACT DEDUPLICATION TEST"
echo "================================"
echo "Running exact deduplication algorithm on images in folder test_images"
python main.py $img_dir -d $exact_out_dir -s
echo "================================"

echo "NEAR DEDUPLICATION TEST"
echo "================================"
echo "Running near deduplication algorithm on images in folder test_images"
python main.py $img_dir -n -d $near_out_dir -s
echo "================================"

