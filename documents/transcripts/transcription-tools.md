# 🎙️ 音声文字起こしツール

YouTube動画から音声を抽出し、自動文字起こしを行うツールセットの説明書です。

---

## 🛠️ ツール概要

### 1. YouTube Audio Extractor
YouTubeビデオから高品質な音声ファイル（MP3）を抽出するPythonスクリプト

**場所**: `youtube-audio-extractor/`

**主な機能**:
- YouTube動画のURL入力で音声抽出
- 最高品質MP3での保存
- ビデオ情報（タイトル、長さ）の取得
- エラーハンドリングと詳細ログ

### 2. Audio Transcriber
音声ファイルを日本語で文字起こしするPythonスクリプト

**場所**: `audio-transcription/`

**主な機能**:
- 複数音声形式対応（MP3, WAV, M4A等）
- 自動音声分割（30秒単位）
- Google Speech Recognition API使用
- テキスト・JSON形式での結果保存

---

## 📋 使用方法

### ステップ1: YouTube音声抽出

```bash
cd youtube-audio-extractor
python3 youtube_audio_extractor.py "YouTube_URL"
```

**例**:
```bash
python3 youtube_audio_extractor.py "https://youtu.be/e9z373SjwkM?si=tSAftbmYZFB9oFqr"
```

### ステップ2: 音声文字起こし

```bash
cd audio-transcription
python3 audio_transcriber.py "音声ファイルパス"
```

**例**:
```bash
python3 audio_transcriber.py "../youtube-audio-extractor/audio_output/動画タイトル.mp3"
```

---

## 📊 出力ファイル

### YouTube Audio Extractor
- **出力先**: `audio_output/`
- **ファイル形式**: MP3（高品質）
- **ファイル名**: 動画タイトルに基づく自動命名

### Audio Transcriber
- **出力先**: `transcription_output/`
- **テキストファイル**: `{ファイル名}_text.txt`
- **詳細結果**: `{ファイル名}_transcription.json`

#### JSON詳細構造
```json
{
  "source_file": "音声ファイルパス",
  "transcription_date": "2025-08-13T...",
  "total_chunks": 30,
  "total_duration": 900,
  "full_text": "全体の文字起こし結果...",
  "chunks": [
    {
      "chunk_index": 1,
      "start_time": 0,
      "end_time": 30,
      "text": "チャンク1の文字起こし..."
    }
  ]
}
```

---

## ⚙️ 設定・カスタマイズ

### 音声分割時間の調整
```python
# audio_transcriber.py 内
self.chunk_duration = 30  # 秒単位（デフォルト: 30秒）
```

### 音声品質設定
```python
# youtube_audio_extractor.py 内
"--audio-quality", "0"  # 0=最高品質, 9=最低品質
```

### 認識言語の変更
```python
# audio_transcriber.py 内
language='ja-JP'  # 日本語（デフォルト）
language='en-US'  # 英語
```

---

## 📋 必要な環境

### システム要件
- Python 3.6以上
- インターネット接続（Google Speech Recognition API）
- ffmpeg（音声変換用）

### Pythonライブラリ
```bash
pip install yt-dlp SpeechRecognition pydub
```

### システム依存関係
```bash
# Ubuntu/Debian
sudo apt update
sudo apt install ffmpeg

# macOS
brew install ffmpeg
```

---

## 🎯 実用例

### 会議録作成
1. オンライン会議の録画をYouTubeにアップロード
2. 本ツールで音声抽出・文字起こし
3. 会議録として整理・編集

### 講演・セミナー記録
1. 講演動画から音声抽出
2. 自動文字起こしで初稿作成
3. 手動校正で完成版作成

### インタビュー・取材
1. インタビュー音声の文字起こし
2. チャンク別での確認・編集
3. 記事作成の素材として活用

---

## ⚠️ 注意事項

### 精度について
- 音声品質によって認識精度が変動
- 背景ノイズが多いと精度低下
- 専門用語や固有名詞は誤認識の可能性

### プライバシー・セキュリティ
- 音声データはGoogle APIに送信される
- 機密情報を含む音声の処理は要注意
- 著作権法の遵守が必要

### パフォーマンス
- 長時間音声は処理時間が長くなる
- APIレート制限による待機時間あり
- 大容量ファイルはメモリ使用量注意

---

## 🚀 今後の改善予定

### 機能拡張
- [ ] ローカル音声認識エンジン対応
- [ ] 複数話者の識別機能
- [ ] 自動要約機能の追加
- [ ] Web UI の開発

### 精度向上
- [ ] 音声前処理の改善
- [ ] 専門用語辞書の追加
- [ ] 話者適応機能

---

## 📞 サポート・お問い合わせ

ツールに関する質問や改善提案は、プロジェクトのIssueにてお気軽にお知らせください。

---

*最終更新: 2025年8月13日*