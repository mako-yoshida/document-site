# YouTube Audio Extractor

YouTubeビデオから音声ファイル（MP3）を抽出するPythonスクリプトです。

## 必要な環境

- Python 3.6+
- yt-dlp
- ffmpeg（音声変換用）

## インストール

```bash
# yt-dlpのインストール（まだの場合）
pip install yt-dlp

# ffmpegのインストール（Ubuntu/Debian）
sudo apt update
sudo apt install ffmpeg
```

## 使用方法

```bash
# 基本的な使用方法
python youtube_audio_extractor.py "https://youtu.be/VIDEO_ID"

# 例：株主総会のビデオから音声抽出
python youtube_audio_extractor.py "https://youtu.be/e9z373SjwkM?si=tSAftbmYZFB9oFqr"
```

## 出力

- 音声ファイルは `./audio_output/` フォルダに保存されます
- ファイル名はビデオのタイトルに基づいて自動生成されます
- フォーマット：MP3（最高品質）

## 機能

1. **音声抽出**: YouTubeビデオからMP3音声ファイルを抽出
2. **ビデオ情報取得**: タイトル、長さ、説明文を表示
3. **品質設定**: 最高品質での音声抽出
4. **エラーハンドリング**: 詳細なエラーメッセージ

## 注意事項

- 著作権法を遵守してご利用ください
- 個人的な用途に限定してお使いください
- 大きなファイルの場合、抽出に時間がかかる場合があります

## トラブルシューティング

### エラー: "yt-dlp not found"
```bash
pip install yt-dlp
```

### エラー: "ffmpeg not found"
```bash
sudo apt install ffmpeg
```

### エラー: "Permission denied"
```bash
chmod +x youtube_audio_extractor.py
```