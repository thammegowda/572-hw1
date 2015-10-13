echo "Running exact deduplication algorithm on images in folder test_images"
python main.py test_images -d test_output_exact_deduplicated_images -s

echo "Running near deduplication algorithm on images in folder test_images"
python main.py test_images -n -d test_output_near_deduplicated_images -s
