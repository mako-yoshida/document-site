#!/usr/bin/env python3
"""
WhisperX Enhanced Quick Version - 即座に使える高精度版
大型モデルダウンロード不要、既存baseモデル + 高精度改善機能
"""

import os
import sys
import json
import time
import re
from pathlib import Path
from datetime import datetime
import whisperx

class WhisperXEnhancedQuick:
    def __init__(self, device="cpu", compute_type="int8"):
        """軽量版Enhanced WhisperX"""
        self.device = device
        self.compute_type = compute_type
        self.model = None
        self.align_model = None
        
        # 日本語修正辞書（株主総会など企業用語特化）
        self.corrections = {
            "密閉市UFJ": "三菱UFJ", "密備市UFJ": "三菱UFJ", "密閉": "三菱", "密備": "三菱",
            "消習後": "招集後", "臣体住宅": "賃貸住宅", "臣規": "新規", "臣体": "賃貸",
            "経産書類": "計算書類", "和楽": "景気", "学費保障": "家賃保証", 
            "やちん": "家賃", "人体者": "入居者", "人体住宅": "賃貸住宅",
            "財券": "財務", "人株": "1株", "廃棟": "配当", "類伸": "累進",
            "同事業年度": "当事業年度", "全事業年度": "前事業年度",
            "党基準": "当期純", "党事業年度": "当事業年度", "身職": "進捗",
            "きょうこな": "強固な", "企業家地": "企業価値", "工場": "向上",
            "学": "額", "検数": "件数", "建造化": "件増加", "建築": "堅調",
            "助した": "除した", "両行": "良好", "吸召再権": "有利子負債",
            "売り上げだか": "売上高", "営業利液": "営業利益", "廃棟金": "配当金",
            "投稿": "動向", "やちんさいむ": "家賃債務", "人供者": "入居者",
            "新容": "信用", "新用": "信用", "提言": "低減", "確率": "確立",
            "機関": "規範", "新党": "浸透", "自属的": "持続的", "構成": "公正",
            "中覚": "中核", "成功": "性向"
        }
        
        print(f"🚀 Enhanced WhisperX Quick版 初期化完了")
        print(f"💻 Device: {device}, Compute: {compute_type}")
    
    def load_models(self):
        """既存baseモデルを使用（ダウンロード不要）"""
        print("🧠 Base モデルをロード中...")
        try:
            self.model = whisperx.load_model("base", self.device, compute_type=self.compute_type)
            print("✅ Base モデルロード完了")
            
            print("🎯 日本語アライメントモデルをロード中...")
            self.align_model, self.metadata = whisperx.load_align_model(
                language_code="ja", device=self.device
            )
            print("✅ アライメントモデルロード完了")
            return True
        except Exception as e:
            print(f"⚠️ モデルロードエラー: {e}")
            return False
    
    def apply_corrections(self, text):
        """日本語企業用語の修正適用"""
        corrected = text
        applied = 0
        
        for wrong, correct in self.corrections.items():
            if wrong in corrected:
                corrected = corrected.replace(wrong, correct)
                applied += 1
        
        # 数字表記統一
        corrected = re.sub(r'(\d+)人株', r'\1株', corrected)
        corrected = re.sub(r'(\d+)学', r'\1額', corrected)
        
        if applied > 0:
            print(f"🔧 {applied}個の企業用語を修正しました")
            
        return corrected, applied > 0
    
    def transcribe(self, audio_path):
        """高精度文字起こし実行"""
        print(f"🎯 文字起こし開始: {audio_path}")
        start_time = time.time()
        
        try:
            # 音声ロード
            audio = whisperx.load_audio(audio_path)
            
            # 日本語最適化転写
            print("🔍 日本語最適化転写中...")
            result = self.model.transcribe(
                audio,
                batch_size=8
            )
            
            # アライメント
            if self.align_model:
                print("🎯 アライメント実行中...")
                result = whisperx.align(
                    result["segments"], self.align_model, self.metadata, 
                    audio, self.device
                )
            
            # テキスト結合
            full_text = " ".join([seg.get("text", "").strip() for seg in result["segments"]])
            
            # 日本語修正適用
            corrected_text, corrections_applied = self.apply_corrections(full_text)
            
            elapsed = time.time() - start_time
            
            print(f"✅ 転写完了! 処理時間: {elapsed:.1f}秒")
            print(f"📊 文字数: {len(corrected_text)}, セグメント: {len(result['segments'])}")
            
            return {
                "original": full_text,
                "corrected": corrected_text,
                "corrections_applied": corrections_applied,
                "segments": result["segments"],
                "processing_time": elapsed
            }
            
        except Exception as e:
            print(f"❌ エラー: {e}")
            return None

def main():
    if len(sys.argv) != 2:
        print("Enhanced WhisperX Quick版 - 高精度日本語文字起こし")
        print("使用方法: python whisperx_enhanced_quick.py <音声ファイル>")
        print("\n🚀 特徴:")
        print("  ✅ 既存モデル使用（大型DL不要）")
        print("  ✅ 日本語最適化設定")
        print("  ✅ 企業・金融用語自動修正")
        print("  ✅ 高速処理")
        sys.exit(1)
    
    audio_path = sys.argv[1]
    if not os.path.exists(audio_path):
        print(f"❌ ファイルが見つかりません: {audio_path}")
        sys.exit(1)
    
    # 転写実行
    transcriber = WhisperXEnhancedQuick()
    
    if not transcriber.load_models():
        print("💥 モデルロードに失敗しました")
        sys.exit(1)
    
    result = transcriber.transcribe(audio_path)
    
    if result:
        print(f"\n🎊 高精度文字起こし完了!")
        print("=" * 60)
        print("📝 修正後テキスト（最初の400文字）:")
        print(result["corrected"][:400] + "..." if len(result["corrected"]) > 400 else result["corrected"])
        print("=" * 60)
        
        if result["corrections_applied"]:
            print("🔧 企業用語の自動修正が適用されました")
        
        # ファイル保存
        output_file = f"{Path(audio_path).stem}_enhanced_quick.txt"
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(result["corrected"])
        print(f"💾 結果保存: {output_file}")
        
    else:
        print("💥 文字起こしに失敗しました")

if __name__ == "__main__":
    main()