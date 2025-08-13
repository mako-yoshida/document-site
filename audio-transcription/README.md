# Audio Transcriber

音声ファイルを日本語で文字起こしするPythonスクリプトです。

## 機能

- 複数の音声フォーマット対応（MP3, WAV, M4A等）
- 長時間音声の自動分割処理
- Google Speech Recognition APIを使用した高精度文字起こし
- JSON形式とテキスト形式での結果保存
- チャンク別の詳細情報保存

## 必要な環境

- Python 3.6+
- インターネット接続（Google Speech Recognition API使用のため）

## 必要なライブラリ

```bash
pip install SpeechRecognition pydub
```

### 追加の依存関係

```bash
# Ubuntu/Debian
sudo apt update
sudo apt install ffmpeg

# macOS (Homebrew)
brew install ffmpeg
```

## 使用方法

```bash
# 基本的な使用方法
python audio_transcriber.py <音声ファイルパス>

# 例：YouTube抽出音声の文字起こし
python audio_transcriber.py "../youtube-audio-extractor/audio_output/第24回定時株主総会(事業報告・対処すべき課題).mp3"
```

## 出力ファイル

### 1. テキストファイル（.txt）
- ファイル名: `{元ファイル名}_text.txt`
- 内容: 文字起こし結果のプレーンテキスト

### 2. JSON詳細ファイル（.json）
- ファイル名: `{元ファイル名}_transcription.json`
- 内容: 
  - 全体の文字起こしテキスト
  - チャンク別の詳細情報
  - タイムスタンプ
  - メタデータ

## 設定

### チャンク分割時間の変更
スクリプト内の `chunk_duration` を変更することで、音声分割の単位を調整できます：

```python
self.chunk_duration = 30  # 秒単位
```

### 音声認識言語の変更
デフォルトは日本語（ja-JP）ですが、他の言語に変更可能：

```python
text = self.recognizer.recognize_google(audio_data, language='en-US')  # 英語
```

## 処理フロー

1. **音声ファイル読み込み**: 各種フォーマットに対応
2. **WAV変換**: 音声認識用にWAV形式に変換
3. **音声分割**: 30秒単位で音声を分割
4. **文字起こし**: 各チャンクを順次処理
5. **結果保存**: テキストとJSONで保存

## エラーハンドリング

- **音声認識不可**: `[音声認識不可]` として記録
- **API エラー**: `[認識エラー: エラー内容]` として記録
- **処理エラー**: `[処理エラー: エラー内容]` として記録

## 注意事項

- Google Speech Recognition APIは無料ですが、使用量制限があります
- 長時間の音声ファイルは処理時間がかかります
- インターネット接続が必要です
- 音質が悪い場合、認識精度が下がる可能性があります

## 著作権とプライバシー

- 音声データはGoogle Speech Recognition APIに送信されます
- 著作権法を遵守してご利用ください
- 機密情報を含む音声の処理にはご注意ください

## トラブルシューティング

### エラー: "No module named 'speech_recognition'"
```bash
pip install SpeechRecognition
```

### エラー: "No module named 'pydub'"
```bash
pip install pydub
```

### エラー: "ffmpeg not found"
```bash
sudo apt install ffmpeg  # Ubuntu/Debian
brew install ffmpeg       # macOS
```

### 認識精度が低い場合
- 音質の良い音声ファイルを使用してください
- 背景ノイズが少ない音声が推奨です
- チャンク分割時間を調整してみてください