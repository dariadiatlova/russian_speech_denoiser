source_txt_directory=$1
target_txt_directory=$2

# moves all files with a .txt extensions fromm multiple source sub-directories into target directory
find $source_txt_directory -name '*.txt' -exec mv {} $target_txt_directory \;
