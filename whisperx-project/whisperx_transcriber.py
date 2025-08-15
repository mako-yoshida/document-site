#!/usr/bin/env python3
"""
WhisperX Audio Transcriber
WhisperXを使用して音声ファイルを文字起こしするスクリプト
"""

import os
import sys
import json
import time
from pathlib import Path
from datetime import datetime
import whisperx

class WhisperXTranscriber:
    def __init__(self, device="cpu", compute_type="int8"):
        """
        WhisperXトランスクライバーを初期化
        
        Args:
            device (str): 実行デバイス ("cpu" または "cuda")
            compute_type (str): 計算タイプ ("int8", "float16", "float32")
        """
        self.device = device
        self.compute_type = compute_type
        self.model = None
        self.align_model = None
        self.diarize_model = None
        
    def load_models(self, model_size="base"):
        """
        必要なモデルをロード
        
        Args:
            model_size (str): Whisperモデルサイズ ("tiny", "base", "small", "medium", "large-v2")
        """
        print(f"Whisperモデル ({model_size}) をロード中...")
        self.model = whisperx.load_model(model_size, self.device, compute_type=self.compute_type)
        print("✅ Whisperモデルのロード完了")
        
        # アライメント用モデル（正確なタイムスタンプのため）
        print("アライメントモデルをロード中...")
        self.align_model, self.metadata = whisperx.load_align_model(language_code="ja", device=self.device)
        print("✅ アライメントモデルのロード完了")
        
    def transcribe_audio(self, audio_path, output_dir="./whisperx_output"):
        """
        音声ファイルを文字起こしする
        
        Args:
            audio_path (str): 音声ファイルのパス
            output_dir (str): 出力ディレクトリ
            
        Returns:
            dict: 文字起こし結果
        """
        try:
            # 出力ディレクトリを作成
            Path(output_dir).mkdir(exist_ok=True)
            
            print(f"🎯 WhisperXで文字起こしを開始します: {audio_path}")
            start_time = time.time()
            
            # 音声ファイルをロード
            print("音声ファイルをロード中...")
            audio = whisperx.load_audio(audio_path)
            print("✅ 音声ファイルのロード完了")
            
            # 1. 文字起こし実行
            print("🔍 文字起こしを実行中...")
            result = self.model.transcribe(audio, batch_size=16)
            print("✅ 文字起こし完了")
            
            # 2. 単語レベルの正確なタイムスタンプを追加
            if self.align_model:
                print("🎯 単語レベルアライメントを実行中...")
                result = whisperx.align(result["segments"], self.align_model, self.metadata, audio, self.device, return_char_alignments=False)
                print("✅ アライメント完了")
            
            # 結果の処理
            full_text = ""
            segments_with_timestamps = []
            
            for segment in result["segments"]:
                segment_info = {
                    "start": segment.get("start", 0),
                    "end": segment.get("end", 0),
                    "text": segment.get("text", "").strip(),
                    "words": segment.get("words", [])
                }
                segments_with_timestamps.append(segment_info)
                
                if segment_info["text"]:
                    full_text += segment_info["text"] + " "
            
            # 結果をまとめる
            transcription_result = {
                "source_file": audio_path,
                "transcription_date": datetime.now().isoformat(),
                "model_info": {
                    "model_type": "WhisperX",
                    "device": self.device,
                    "compute_type": self.compute_type
                },
                "full_text": full_text.strip(),
                "segments": segments_with_timestamps,
                "total_segments": len(segments_with_timestamps)
            }
            
            # 結果をファイルに保存
            audio_name = Path(audio_path).stem
            output_file = Path(output_dir) / f"{audio_name}_whisperx_transcription.json"
            text_file = Path(output_dir) / f"{audio_name}_whisperx_text.txt"
            
            # JSON結果を保存
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(transcription_result, f, ensure_ascii=False, indent=2)
            
            # テキストのみを保存
            with open(text_file, 'w', encoding='utf-8') as f:
                f.write(transcription_result['full_text'])
            
            elapsed_time = time.time() - start_time
            
            print(f"\n🎉 WhisperX文字起こし完了!")
            print(f"⏱️  処理時間: {elapsed_time:.1f}秒")
            print(f"📄 テキストファイル: {text_file}")
            print(f"📋 詳細結果: {output_file}")
            print(f"📊 総文字数: {len(transcription_result['full_text'])}文字")
            print(f"🎯 セグメント数: {len(segments_with_timestamps)}個")
            
            return transcription_result
            
        except Exception as e:
            print(f"❌ WhisperX文字起こしエラー: {e}")
            return None

def main():
    """メイン関数"""
    if len(sys.argv) != 2:
        print("使用方法: python whisperx_transcriber.py <音声ファイルパス>")
        print("例: python whisperx_transcriber.py 'youtube-audio-extractor/audio_output/第24回定時株主総会(事業報告・対処すべき課題).mp3'")
        sys.exit(1)
    
    audio_path = sys.argv[1]
    
    if not os.path.exists(audio_path):
        print(f"❌ エラー: ファイルが見つかりません: {audio_path}")
        sys.exit(1)
    
    # WhisperXトランスクライバーを初期化
    print("🚀 WhisperXトランスクライバーを初期化中...")
    transcriber = WhisperXTranscriber(device="cpu", compute_type="int8")
    
    # モデルをロード
    transcriber.load_models(model_size="base")
    
    # 文字起こし実行
    result = transcriber.transcribe_audio(audio_path)
    
    if result:
        print(f"\n🎊 WhisperXによる文字起こしが正常に完了しました!")
        print(f"📝 文字起こしテキスト（最初の200文字）:")
        print("-" * 50)
        print(result['full_text'][:200] + "..." if len(result['full_text']) > 200 else result['full_text'])
        print("-" * 50)
        print("🆚 既存の結果と比較するには、比較スクリプトを実行してください。")
    else:
        print("\n💥 文字起こしに失敗しました")
        sys.exit(1)

if __name__ == "__main__":
    main()