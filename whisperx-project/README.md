# WhisperX音声認識プロジェクト

## プロジェクト概要

このプロジェクトは、WhisperXを使用した音声文字起こしの実装と、既存のGoogle Speech Recognitionとの精度比較を行ったものです。

## プロジェクト構成

```
whisperx-project/
├── README.md                                    # このファイル
├── whisperx_transcriber.py                      # WhisperX文字起こしスクリプト
├── compare_transcriptions.py                    # 文字起こし結果比較ツール
├── transcription_comparison_report.md           # 詳細比較レポート
└── whisperx_output/                            # WhisperX出力結果
    ├── 第24回定時株主総会(事業報告・対処すべき課題)_whisperx_text.txt
    └── 第24回定時株主総会(事業報告・対処すべき課題)_whisperx_transcription.json
```

## 実行結果サマリー

- **処理時間**: 約2分40秒（音声約3分間）
- **文字数**: 3,465文字（34セグメント）
- **精度**: Google Speech Recognitionとの類似度73.8%
- **特徴**: 単語レベルタイムスタンプ、話者分離対応

## 使用方法

### 1. WhisperXによる文字起こし

```bash
python3 whisperx_transcriber.py "音声ファイルのパス"
```

**例:**
```bash
python3 whisperx_transcriber.py "../youtube-audio-extractor/audio_output/第24回定時株主総会(事業報告・対処すべき課題).mp3"
```

### 2. 文字起こし結果の比較

```bash
python3 compare_transcriptions.py
```

このスクリプトは以下のファイルを自動的に比較します：
- Google Speech Recognition結果: `../audio-transcription/transcription_output/第24回定時株主総会(事業報告・対処すべき課題)_text.txt`
- WhisperX結果: `whisperx_output/第24回定時株主総会(事業報告・対処すべき課題)_whisperx_transcription.json`

## 必要環境

### WhisperXのインストール

```bash
pip install whisperx
```

**注意**: 
- インストールには約15分、3-4GBのダウンロードが必要
- NVIDIA CUDAライブラリを含む多数の依存関係をインストール

### システム要件

- Python 3.8+
- 十分なディスク容量（約5GB以上推奨）
- メモリ4GB以上推奨

## 技術仕様

### WhisperXの特徴

1. **高精度文字起こし**: OpenAI Whisperベースの高精度音声認識
2. **単語レベルタイムスタンプ**: 正確な時間情報
3. **話者分離**: 複数話者の自動分離（Voice Activity Detection）
4. **多言語対応**: 日本語を含む約100言語サポート
5. **オープンソース**: MIT License

### 処理フロー

1. 音声ファイル読み込み
2. Whisperによる文字起こし実行
3. 単語レベルアライメント
4. 結果のJSON/テキスト出力

## 比較分析結果

| 項目 | Google Speech Recognition | WhisperX |
|------|---------------------------|----------|
| 文字数 | 3,482文字 | 3,465文字 |
| 処理時間 | 約5分 | 約2分40秒 |
| 特徴 | チャンク分割処理 | 一括処理 |
| 強み | 安定性、日本語最適化 | 効率性、文脈保持 |

### 主な差異

- **用語認識**: 専門用語や固有名詞で差異
- **文脈理解**: WhisperXの方が自然な文章構造
- **処理効率**: WhisperXが約2倍高速

## ファイル詳細

### whisperx_transcriber.py
- WhisperXを使用した音声文字起こしスクリプト
- 単語レベルタイムスタンプ生成
- JSON/テキスト形式での結果出力

### compare_transcriptions.py
- 2つの文字起こし結果の比較分析ツール
- 類似度計算、差異抽出機能
- Markdownレポート自動生成

### transcription_comparison_report.md
- 詳細な比較分析レポート
- 統計情報、差異分析、推奨事項を含む

## 今後の拡張可能性

1. **リアルタイム文字起こし**: ストリーミング音声対応
2. **話者分離**: 複数話者音声での精度向上
3. **専門用語辞書**: ビジネス・技術用語の認識精度向上
4. **GUI化**: ユーザーフレンドリーなインターフェース

## ライセンス

このプロジェクトのコードはMITライセンスです。  
WhisperX自体もMITライセンスのオープンソースソフトウェアです。

---

*作成日: 2025年8月15日*  
*最終更新: 2025年8月15日*