#!/usr/bin/env python3
"""
Quick test script for enhanced WhisperX with medium model
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from whisperx_transcriber import WhisperXTranscriber

def quick_test():
    audio_path = "/home/yoshida/githubio1/youtube-audio-extractor/audio_output/第24回定時株主総会(事業報告・対処すべき課題).mp3"
    
    if not os.path.exists(audio_path):
        print(f"❌ Audio file not found: {audio_path}")
        return
    
    print("🚀 Quick test with medium model...")
    transcriber = WhisperXTranscriber(device="cpu", compute_type="int8")
    
    # Use medium model for faster testing
    transcriber.load_models(model_size="medium")
    
    # Test transcription
    result = transcriber.transcribe_audio(audio_path, output_dir="./quick_test_output")
    
    if result:
        print("\n✅ Quick test successful!")
        print(f"📝 First 200 chars: {result['full_text'][:200]}...")
        
        if result['accuracy_improvements']['postprocessing_applied']:
            print("🔧 Postprocessing corrections were applied!")
        
    else:
        print("❌ Quick test failed")

if __name__ == "__main__":
    quick_test()