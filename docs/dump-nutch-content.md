# How to dump Nutch Content

## Merge All Segments

This step merge all segments in `crawl/segments` to a single segment under `mergedsegs`
`nutch mergesegs mergedsegs -dir crawl/segments`

## Dump the merged segment

`nutch dump -outputDir dump -segment mergedsegs`

run `find dump` to list all files
