BASE_DIRECTORY=$(dirname $(dirname $(pwd)))
for folder in "$BASE_DIRECTORY"/*; do
    if [[ -d $folder && $folder != *"_0-aacg-"* && $folder == *"-aacg-"* ]]; then
        echo "Processing folder: $folder"
        # 构造 sed 命令来插入 newfile.txt 的内容
        sed -i "/mask {/r newfile.txt" "$folder/first.inp"
        echo "in directory: $(pwd)"
        # 插入 template_id 内容
        sed -i "/template_id {/r ../../template_id_content.txt" "$folder/first.inp"
    fi
done
