#!/bin/bash

set -e

# Resolve to the site root (parent of tools/) so the relative paths below work from any CWD.
cd "$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

# 定义需要处理的文件列表
FILES=(
  "assets/media/projects/scene-flow-deployment/autoflow_vis.mp4"
  "assets/media/projects/offline-4d-labeling/offline_visual_auto_labeling.mp4"
)

for FILE in "${FILES[@]}"; do
  # 检查原始文件是否存在
  if [ ! -f "$FILE" ]; then
    echo "❌ 文件不存在，跳过: $FILE"
    continue
  fi

  # 生成备份文件名（在扩展名前加 _bk）
  DIR=$(dirname "$FILE")
  BASENAME=$(basename "$FILE" .mp4)
  BACKUP="${DIR}/${BASENAME}_bk.mp4"
  OUTPUT="$FILE"

  echo "================================================"
  echo "📦 处理文件: $FILE"

  # 备份原始文件
  echo "🔒 备份: $FILE -> $BACKUP"
  cp "$FILE" "$BACKUP"

  # 执行 ffmpeg 转换
  echo "🎬 转换中..."
  ffmpeg -y -i "$BACKUP" \
    -map 0:v:0 -map 0:a? \
    -c:v copy -c:a copy \
    -sn -dn \
    -movflags +faststart \
    "$OUTPUT"

  echo "✅ 完成: $OUTPUT"
done

echo "================================================"
echo "🎉 所有文件处理完毕！"