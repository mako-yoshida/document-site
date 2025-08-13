#!/usr/bin/env python3
"""
Audio Transcriber
音声ファイルを文字起こしするスクリプト
"""

import os
import sys
import time
from pathlib import Path
import speech_recognition as sr
from pydub import AudioSegment
from pydub.silence import split_on_silence
import json
from datetime import datetime

class AudioTranscriber:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.chunk_duration = 30  # 30秒ずつに分割
        
    def convert_to_wav(self, audio_path):
        """
        音声ファイルをWAVフォーマットに変換
        
        Args:
            audio_path (str): 入力音声ファイルのパス
            
        Returns:
            str: 変換されたWAVファイルのパス
        """
        try:
            print(f"音声ファイルを読み込み中: {audio_path}")
            
            # ファイル拡張子に基づいて読み込み
            audio_path = Path(audio_path)
            if audio_path.suffix.lower() == '.mp3':
                audio = AudioSegment.from_mp3(str(audio_path))
            elif audio_path.suffix.lower() == '.wav':
                audio = AudioSegment.from_wav(str(audio_path))
            elif audio_path.suffix.lower() == '.m4a':
                audio = AudioSegment.from_file(str(audio_path), "m4a")
            else:
                audio = AudioSegment.from_file(str(audio_path))
            
            # WAVフォーマットで保存
            wav_path = audio_path.parent / f"{audio_path.stem}_converted.wav"
            audio.export(str(wav_path), format="wav")
            
            print(f"WAVファイルに変換完了: {wav_path}")
            return str(wav_path)
            
        except Exception as e:
            print(f"音声変換エラー: {e}")
            return None
    
    def split_audio(self, audio_path, chunk_length_ms=30000):
        """
        音声ファイルを指定された長さで分割
        
        Args:
            audio_path (str): 音声ファイルのパス
            chunk_length_ms (int): チャンクの長さ（ミリ秒）
            
        Returns:
            list: 分割された音声チャンクのリスト
        """
        try:
            print(f"音声ファイルを{chunk_length_ms/1000}秒ごとに分割中...")
            
            audio = AudioSegment.from_wav(audio_path)
            chunks = []
            
            for i in range(0, len(audio), chunk_length_ms):
                chunk = audio[i:i + chunk_length_ms]
                chunks.append(chunk)
            
            print(f"音声を{len(chunks)}個のチャンクに分割しました")
            return chunks
            
        except Exception as e:
            print(f"音声分割エラー: {e}")
            return []
    
    def transcribe_chunk(self, audio_chunk, chunk_index):
        """
        音声チャンクを文字起こしする
        
        Args:
            audio_chunk: 音声チャンク
            chunk_index (int): チャンクのインデックス
            
        Returns:
            str: 文字起こし結果
        """
        try:
            # 一時的なWAVファイルとして保存
            temp_path = f"temp_chunk_{chunk_index}.wav"
            audio_chunk.export(temp_path, format="wav")
            
            # 音声認識を実行
            with sr.AudioFile(temp_path) as source:
                audio_data = self.recognizer.record(source)
                
            # Google Speech Recognition を使用して文字起こし
            try:
                text = self.recognizer.recognize_google(audio_data, language='ja-JP')
                print(f"チャンク {chunk_index + 1}: 文字起こし完了")
                return text
            except sr.UnknownValueError:
                print(f"チャンク {chunk_index + 1}: 音声を認識できませんでした")
                return "[音声認識不可]"
            except sr.RequestError as e:
                print(f"チャンク {chunk_index + 1}: Google Speech Recognition エラー: {e}")
                return f"[認識エラー: {e}]"
            
        except Exception as e:
            print(f"チャンク {chunk_index + 1} 処理エラー: {e}")
            return f"[処理エラー: {e}]"
        finally:
            # 一時ファイルを削除
            if os.path.exists(temp_path):
                os.remove(temp_path)
    
    def transcribe_audio(self, audio_path, output_dir="./transcription_output"):
        """
        音声ファイル全体を文字起こしする
        
        Args:
            audio_path (str): 音声ファイルのパス
            output_dir (str): 出力ディレクトリ
            
        Returns:
            dict: 文字起こし結果とメタデータ
        """
        try:
            # 出力ディレクトリを作成
            Path(output_dir).mkdir(exist_ok=True)
            
            print(f"文字起こしを開始します: {audio_path}")
            start_time = time.time()
            
            # WAV形式に変換
            wav_path = self.convert_to_wav(audio_path)
            if not wav_path:
                return None
            
            # 音声を分割
            chunks = self.split_audio(wav_path, self.chunk_duration * 1000)
            if not chunks:
                return None
            
            # 各チャンクを文字起こし
            transcription_results = []
            full_text = ""
            
            for i, chunk in enumerate(chunks):
                print(f"\nチャンク {i + 1}/{len(chunks)} を処理中...")
                
                chunk_text = self.transcribe_chunk(chunk, i)
                
                chunk_result = {
                    'chunk_index': i + 1,
                    'start_time': i * self.chunk_duration,
                    'end_time': min((i + 1) * self.chunk_duration, len(chunks[0]) / 1000 * len(chunks)),
                    'text': chunk_text
                }
                
                transcription_results.append(chunk_result)
                
                if chunk_text and not chunk_text.startswith('['):
                    full_text += chunk_text + " "
                
                # APIレート制限を避けるため少し待機
                time.sleep(1)
            
            # 結果をまとめる
            result = {
                'source_file': audio_path,
                'transcription_date': datetime.now().isoformat(),
                'total_chunks': len(chunks),
                'total_duration': len(chunks) * self.chunk_duration,
                'full_text': full_text.strip(),
                'chunks': transcription_results
            }
            
            # 結果をファイルに保存
            audio_name = Path(audio_path).stem
            output_file = Path(output_dir) / f"{audio_name}_transcription.json"
            text_file = Path(output_dir) / f"{audio_name}_text.txt"
            
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(result, f, ensure_ascii=False, indent=2)
            
            with open(text_file, 'w', encoding='utf-8') as f:
                f.write(result['full_text'])
            
            # 一時WAVファイルを削除
            if wav_path != audio_path:
                os.remove(wav_path)
            
            elapsed_time = time.time() - start_time
            print(f"\n✅ 文字起こし完了!")
            print(f"⏱️  処理時間: {elapsed_time:.1f}秒")
            print(f"📄 テキストファイル: {text_file}")
            print(f"📋 詳細結果: {output_file}")
            print(f"📊 総文字数: {len(result['full_text'])}文字")
            
            return result
            
        except Exception as e:
            print(f"文字起こしエラー: {e}")
            return None

def main():
    """メイン関数"""
    if len(sys.argv) != 2:
        print("使用方法: python audio_transcriber.py <音声ファイルパス>")
        print("例: python audio_transcriber.py '../youtube-audio-extractor/audio_output/第24回定時株主総会(事業報告・対処すべき課題).mp3'")
        sys.exit(1)
    
    audio_path = sys.argv[1]
    
    if not os.path.exists(audio_path):
        print(f"エラー: ファイルが見つかりません: {audio_path}")
        sys.exit(1)
    
    # 文字起こし実行
    transcriber = AudioTranscriber()
    result = transcriber.transcribe_audio(audio_path)
    
    if result:
        print(f"\n🎉 文字起こしが正常に完了しました!")
        print(f"📝 文字起こしテキスト（最初の200文字）:")
        print("-" * 50)
        print(result['full_text'][:200] + "..." if len(result['full_text']) > 200 else result['full_text'])
    else:
        print("\n❌ 文字起こしに失敗しました")
        sys.exit(1)

if __name__ == "__main__":
    main()