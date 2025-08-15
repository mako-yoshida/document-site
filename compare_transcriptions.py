#!/usr/bin/env python3
"""
Transcription Comparison Tool
異なる音声認識エンジンの文字起こし結果を比較するツール
"""

import json
import os
from pathlib import Path
from difflib import SequenceMatcher
import re
from datetime import datetime

class TranscriptionComparator:
    def __init__(self):
        self.results = {}
        
    def load_google_transcription(self, file_path):
        """
        Google Speech Recognition の結果を読み込み
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read().strip()
            
            self.results['google'] = {
                'source': 'Google Speech Recognition',
                'text': content,
                'length': len(content),
                'file_path': file_path
            }
            return True
        except Exception as e:
            print(f"❌ Google結果の読み込みエラー: {e}")
            return False
    
    def load_whisperx_transcription(self, file_path):
        """
        WhisperX の結果を読み込み
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            self.results['whisperx'] = {
                'source': 'WhisperX',
                'text': data['full_text'],
                'length': len(data['full_text']),
                'segments': len(data.get('segments', [])),
                'file_path': file_path,
                'model_info': data.get('model_info', {})
            }
            return True
        except Exception as e:
            print(f"❌ WhisperX結果の読み込みエラー: {e}")
            return False
    
    def normalize_text(self, text):
        """
        テキストを正規化して比較しやすくする
        """
        # 空白文字を統一
        text = re.sub(r'\s+', ' ', text)
        # 句読点周りの空白を除去
        text = re.sub(r'\s*([。、！？])\s*', r'\1', text)
        # 括弧の中身を除去（エラーメッセージなど）
        text = re.sub(r'\[.*?\]', '', text)
        return text.strip()
    
    def calculate_similarity(self, text1, text2):
        """
        2つのテキストの類似度を計算
        """
        normalized1 = self.normalize_text(text1)
        normalized2 = self.normalize_text(text2)
        
        return SequenceMatcher(None, normalized1, normalized2).ratio()
    
    def extract_differences(self, text1, text2, context_length=50):
        """
        テキスト間の差異を抽出
        """
        normalized1 = self.normalize_text(text1)
        normalized2 = self.normalize_text(text2)
        
        matcher = SequenceMatcher(None, normalized1, normalized2)
        differences = []
        
        for tag, i1, i2, j1, j2 in matcher.get_opcodes():
            if tag != 'equal':
                # 前後のコンテキストを含める
                start1 = max(0, i1 - context_length)
                end1 = min(len(normalized1), i2 + context_length)
                start2 = max(0, j1 - context_length)
                end2 = min(len(normalized2), j2 + context_length)
                
                differences.append({
                    'type': tag,
                    'google': normalized1[start1:end1],
                    'whisperx': normalized2[start2:end2],
                    'position': {'google': (i1, i2), 'whisperx': (j1, j2)}
                })
        
        return differences
    
    def analyze_character_accuracy(self):
        """
        文字レベルでの精度分析
        """
        if 'google' not in self.results or 'whisperx' not in self.results:
            return None
        
        google_text = self.normalize_text(self.results['google']['text'])
        whisperx_text = self.normalize_text(self.results['whisperx']['text'])
        
        matcher = SequenceMatcher(None, google_text, whisperx_text)
        matches = sum(triple.size for triple in matcher.get_matching_blocks())
        
        accuracy = matches / max(len(google_text), len(whisperx_text)) if google_text or whisperx_text else 0
        
        return {
            'character_match_ratio': accuracy,
            'google_length': len(google_text),
            'whisperx_length': len(whisperx_text),
            'length_difference': len(whisperx_text) - len(google_text)
        }
    
    def generate_report(self, output_file="transcription_comparison_report.md"):
        """
        比較レポートを生成
        """
        if len(self.results) < 2:
            print("❌ 比較には少なくとも2つの結果が必要です")
            return False
        
        google_text = self.results['google']['text']
        whisperx_text = self.results['whisperx']['text']
        
        # 類似度計算
        similarity = self.calculate_similarity(google_text, whisperx_text)
        
        # 文字レベル分析
        char_analysis = self.analyze_character_accuracy()
        
        # 差異抽出
        differences = self.extract_differences(google_text, whisperx_text)
        
        # レポート生成
        report = f"""# 音声文字起こし比較レポート

## 概要
- 生成日時: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
- 比較対象: Google Speech Recognition vs WhisperX

## 基本統計

### Google Speech Recognition
- 文字数: {self.results['google']['length']:,}文字
- ファイル: {self.results['google']['file_path']}

### WhisperX
- 文字数: {self.results['whisperx']['length']:,}文字
- セグメント数: {self.results['whisperx'].get('segments', 'N/A')}個
- ファイル: {self.results['whisperx']['file_path']}
- モデル情報: {self.results['whisperx'].get('model_info', {})}

## 比較分析

### 全体類似度
- **類似度スコア: {similarity:.3f} ({similarity*100:.1f}%)**

### 文字レベル分析
- 文字一致率: {char_analysis['character_match_ratio']:.3f} ({char_analysis['character_match_ratio']*100:.1f}%)
- 文字数差: {char_analysis['length_difference']:+,}文字 (WhisperX - Google)

## テキスト比較

### Google Speech Recognition
```
{google_text[:500]}{'...' if len(google_text) > 500 else ''}
```

### WhisperX
```
{whisperx_text[:500]}{'...' if len(whisperx_text) > 500 else ''}
```

## 主な差異 (最初の5件)

"""
        
        for i, diff in enumerate(differences[:5], 1):
            report += f"""
### 差異 {i}: {diff['type']}
**Google:**
```
{diff['google']}
```

**WhisperX:**
```
{diff['whisperx']}
```

---
"""
        
        report += f"""
## 総評

- **文字起こし精度**: {'高' if similarity > 0.8 else '中' if similarity > 0.6 else '低'}
- **文字数差**: {abs(char_analysis['length_difference'])}文字の差異
- **検出された差異**: {len(differences)}箇所

### 推奨事項
"""
        
        if similarity > 0.8:
            report += "- ✅ 両システムの結果は高い一致率を示しています\n"
        elif similarity > 0.6:
            report += "- ⚠️ 中程度の一致率です。重要な部分は手動確認を推奨\n"
        else:
            report += "- ❌ 低い一致率です。両方の結果を詳細に検証することを強く推奨\n"
        
        if char_analysis['length_difference'] > 100:
            report += "- 📏 WhisperXの方が詳細な文字起こしを提供している可能性があります\n"
        elif char_analysis['length_difference'] < -100:
            report += "- 📏 Googleの方が詳細な文字起こしを提供している可能性があります\n"
        
        # レポートをファイルに保存
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(report)
            
            print(f"📊 比較レポートを生成しました: {output_file}")
            return True
            
        except Exception as e:
            print(f"❌ レポート生成エラー: {e}")
            return False

def main():
    """メイン関数"""
    print("🔍 音声文字起こし比較ツール")
    print("=" * 50)
    
    comparator = TranscriptionComparator()
    
    # Google Speech Recognition結果を読み込み
    google_file = "audio-transcription/transcription_output/第24回定時株主総会(事業報告・対処すべき課題)_text.txt"
    if os.path.exists(google_file):
        print(f"📖 Google結果を読み込み中: {google_file}")
        if comparator.load_google_transcription(google_file):
            print("✅ Google結果の読み込み完了")
        else:
            print("❌ Google結果の読み込みに失敗")
            return
    else:
        print(f"❌ Googleファイルが見つかりません: {google_file}")
        return
    
    # WhisperX結果を読み込み
    whisperx_file = "whisperx_output/第24回定時株主総会(事業報告・対処すべき課題)_whisperx_transcription.json"
    if os.path.exists(whisperx_file):
        print(f"📖 WhisperX結果を読み込み中: {whisperx_file}")
        if comparator.load_whisperx_transcription(whisperx_file):
            print("✅ WhisperX結果の読み込み完了")
        else:
            print("❌ WhisperX結果の読み込みに失敗")
            return
    else:
        print(f"❌ WhisperXファイルが見つかりません: {whisperx_file}")
        return
    
    # 比較実行
    print("\n🔬 比較分析を実行中...")
    if comparator.generate_report():
        print("✅ 比較分析完了!")
        
        # 簡易サマリーを表示
        google_text = comparator.results['google']['text']
        whisperx_text = comparator.results['whisperx']['text']
        similarity = comparator.calculate_similarity(google_text, whisperx_text)
        
        print(f"\n📊 簡易サマリー:")
        print(f"   類似度: {similarity:.3f} ({similarity*100:.1f}%)")
        print(f"   Google文字数: {len(google_text):,}")
        print(f"   WhisperX文字数: {len(whisperx_text):,}")
        print(f"   文字数差: {len(whisperx_text) - len(google_text):+,}")
        
    else:
        print("❌ 比較分析に失敗しました")

if __name__ == "__main__":
    main()