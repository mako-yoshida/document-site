# Document Site - Claude Code Configuration

## Repository Information
- **Repository**: https://github.com/mako-yoshida/document-site
- **GitHub Pages**: https://mako-yoshida.github.io/document-site
- **Main Branch**: main

## Project Structure
```
documents/
├── config.json              # Site configuration
├── business-strategy/       # Business strategy documents
│   ├── zenpo-strategy.md
│   └── proptech-market-strategy.md
├── sample-folder/
└── technical/
```

## Development Commands
```bash
# Authentication
git config --global credential.helper store

# Check status
git status
git log --oneline -5

# Deploy changes
git add .
git commit -m "Description"
git push origin main

# Local server (if needed)
python3 -m http.server 8000
```

## File Management
- All documents are managed through `documents/config.json`
- New files must be added to both the filesystem and config.json
- Changes require git commit and push to appear on GitHub Pages

## WhisperX Implementation Project (継続中)
**ブランチ**: `whisperx-transcription`
**開始日**: 2025-08-15

### プロジェクト概要
- YouTubeから抽出した音声ファイルでWhisperXを使用した文字起こし機能を実装
- 既存の文字起こし結果と精度比較を行う

### 対象ファイル
- 音声ファイル: `youtube-audio-extractor/audio_output/第24回定時株主総会(事業報告・対処すべき課題).mp3`
- 既存の文字起こし結果: `audio-transcription/transcription_output/`

### 進捗状況 (Todo List)
- [x] 新しいブランチを作成してチェックアウト
- [進行中] WhisperXライブラリのインストール
  - 状況: `pip install whisperx` 実行中（NVIDIA CUDAライブラリダウンロード中）
  - バックグラウンドプロセス: bash_2
- [保留] 音声ファイルでWhisperXを使った文字起こし実行
- [保留] 既存の文字起こし結果と比較検証

### 次のステップ（継続時の作業）
1. WhisperXインストール完了確認: `pip list | grep whisperx`
2. WhisperX用スクリプト作成: `whisperx_transcriber.py`
3. 音声ファイルで文字起こし実行
4. 既存結果（Google Speech Recognition）との比較分析

### 技術メモ
- WhisperXは話者分離、正確なタイムスタンプ、VAD機能を持つ
- 日本語対応、オープンソース（MIT License）
- 依存関係が多く、インストールに時間がかかる

## Last Updated
2025-08-15 - WhisperX project progress documentation