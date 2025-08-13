#!/usr/bin/env python3
"""
YouTube Audio Extractor
YouTubeビデオから音声ファイルを抽出するスクリプト
"""

import os
import sys
import subprocess
from pathlib import Path

def extract_audio(youtube_url, output_dir="./audio_output"):
    """
    YouTubeビデオから音声を抽出する
    
    Args:
        youtube_url (str): YouTubeビデオのURL
        output_dir (str): 出力ディレクトリ
    
    Returns:
        str: 抽出された音声ファイルのパス
    """
    # 出力ディレクトリを作成
    Path(output_dir).mkdir(exist_ok=True)
    
    # yt-dlpコマンドの構築
    cmd = [
        "yt-dlp",
        "--extract-audio",
        "--audio-format", "mp3",
        "--audio-quality", "0",  # best quality
        "--output", f"{output_dir}/%(title)s.%(ext)s",
        "--no-playlist",
        youtube_url
    ]
    
    try:
        print(f"音声抽出を開始します: {youtube_url}")
        print(f"出力先: {output_dir}")
        
        # yt-dlpを実行
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        
        print("音声抽出が完了しました!")
        print(f"出力: {result.stdout}")
        
        # 作成されたファイルを探す
        audio_files = list(Path(output_dir).glob("*.mp3"))
        if audio_files:
            latest_file = max(audio_files, key=os.path.getctime)
            print(f"抽出された音声ファイル: {latest_file}")
            return str(latest_file)
        else:
            print("音声ファイルが見つかりませんでした")
            return None
            
    except subprocess.CalledProcessError as e:
        print(f"エラーが発生しました: {e}")
        print(f"stderr: {e.stderr}")
        return None
    except Exception as e:
        print(f"予期しないエラー: {e}")
        return None

def get_video_info(youtube_url):
    """
    YouTubeビデオの情報を取得する
    
    Args:
        youtube_url (str): YouTubeビデオのURL
    
    Returns:
        dict: ビデオ情報
    """
    cmd = [
        "yt-dlp",
        "--print", "title",
        "--print", "duration",
        "--print", "description",
        "--no-playlist",
        youtube_url
    ]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        lines = result.stdout.strip().split('\n')
        
        return {
            'title': lines[0] if len(lines) > 0 else '',
            'duration': lines[1] if len(lines) > 1 else '',
            'description': lines[2] if len(lines) > 2 else ''
        }
    except Exception as e:
        print(f"ビデオ情報取得エラー: {e}")
        return {}

def main():
    """メイン関数"""
    if len(sys.argv) != 2:
        print("使用方法: python youtube_audio_extractor.py <YouTube_URL>")
        print("例: python youtube_audio_extractor.py 'https://youtu.be/e9z373SjwkM'")
        sys.exit(1)
    
    youtube_url = sys.argv[1]
    
    # ビデオ情報を取得
    print("ビデオ情報を取得中...")
    video_info = get_video_info(youtube_url)
    
    if video_info:
        print(f"タイトル: {video_info.get('title', 'N/A')}")
        print(f"長さ: {video_info.get('duration', 'N/A')}")
        print("-" * 50)
    
    # 音声抽出
    audio_file = extract_audio(youtube_url)
    
    if audio_file:
        print(f"\n✅ 成功: 音声ファイルが作成されました")
        print(f"📁 パス: {audio_file}")
        
        # ファイルサイズを表示
        file_size = Path(audio_file).stat().st_size
        print(f"📊 サイズ: {file_size / (1024*1024):.1f} MB")
    else:
        print("\n❌ 失敗: 音声抽出に失敗しました")
        sys.exit(1)

if __name__ == "__main__":
    main()