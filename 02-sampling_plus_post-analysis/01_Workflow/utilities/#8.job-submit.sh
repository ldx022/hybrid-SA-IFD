#!/bin/bash

# 获取基本目录
read -p "请输入aacg-prep.py创建的文件夹所在的基目录: " base_directory

# 遍历基本目录中的目标文件夹
for folder in "$base_directory"/*; do
    if [[ -d "$folder" && "$folder" != *"_0-aacg-"* && "$folder" == *"-aacg-"* ]]; then
        anneal_dir="$folder/anneal"
        gro_bsub_file="$anneal_dir/gro.bsub"

        # 检查 gro.bsub 文件是否存在
        if [[ -f "$gro_bsub_file" ]]; then
            # 进入目标文件夹
            cd "$anneal_dir" || continue

            # 提交作业
            bsub < "$gro_bsub_file"
            echo "作业 $gro_bsub_file 已提交"

            # 返回到原始目录（可选）
            cd - > /dev/null

            # 每提交一个作业休息 60 秒
            sleep 60
        fi
    fi
done

# 输出完成消息
echo "作业已提交完毕，退出该提交作业脚本"
