#!/bin/bash
# Time in second get from server
FPS="$2"
DIRECTORY="$1"
SCALE=""
NOW=$(date '+%s')


if [ ! -z $3 ]
  then
    NOW="$3"
fi

if [ ! -z $4 ]
  then
    SCALE="scale="$4","
fi

mkdir ./$NOW

# Remove any JPGs from previous runs.
find "$DIRECTORY" -name '*.jpg' | xargs rm

# Find any MP4s even in sub dirs, and store results in array.
# This is important as ffmpeg refuses to excute more than once
# if using a regular loop using find.
unset a i
while IFS= read -r -d '' file; do
  a[i++]="$file"
done < <(find "$DIRECTORY" -name '*.mp4' -type f -print0)

for n in "${a[@]}"
do
   :
   echo $n
   # Replace .mp4 with blank to remove.
   FILEPREFIX=$(echo $n | sed 's/.mp4//g')
   # Generate frames
   ffmpeg -i "$FILEPREFIX".mp4 -y -an -q 0 -vf "$SCALE"fps="$FPS" ./"$NOW"/"$FILEPREFIX"_%06d.jpg
done

python3 ./ocr.py "$NOW"
python3 ocrresult_to_html.py "$NOW"
