#!/usr/bin/env python3
"""
既存の文字起こしテキストにEnhanced修正を適用
"""

import re
import sys
import os

def apply_enhanced_corrections():
    # Enhanced修正辞書
    corrections = {
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
        "九州採検体": "貸倒引当金", "売り上げだか": "売上高", "営業利液": "営業利益",
        "廃棟金": "配当金", "投稿": "動向", "やちんさいむ": "家賃債務", 
        "人供者": "入居者", "新容": "信用", "新用": "信用", "提言": "低減",
        "確率": "確立", "機関": "規範", "新党": "浸透", "自属的": "持続的",
        "構成": "公正", "中覚": "中核", "成功": "性向", "密閉市UFJ2コス": "三菱UFJニコス",
        "当産検数": "倒産件数", "三美市UFJ": "三菱UFJ", "勝ち想像": "価値創造",
        "効率が": "効率化", "深価値": "新価値", "三部CUFJ": "三菱UFJ",
        "圧倒的な新容力": "圧倒的な信用力"
    }
    
    # 元ファイル読み込み
    input_file = "whisperx-project/whisperx_output/第24回定時株主総会(事業報告・対処すべき課題)_whisperx_text.txt"
    
    with open(input_file, 'r', encoding='utf-8') as f:
        original_text = f.read()
    
    print("🔧 Enhanced修正機能を適用中...")
    
    # 修正適用
    corrected_text = original_text
    corrections_applied = []
    
    for wrong, correct in corrections.items():
        if wrong in corrected_text:
            corrected_text = corrected_text.replace(wrong, correct)
            corrections_applied.append(f"{wrong} → {correct}")
    
    # 数字表記統一
    original_before_num = corrected_text
    corrected_text = re.sub(r'(\d+)人株', r'\1株', corrected_text)
    corrected_text = re.sub(r'(\d+)学', r'\1額', corrected_text)
    
    if original_before_num != corrected_text:
        corrections_applied.append("数字表記の統一")
    
    # 結果保存
    output_file = "第24回定時株主総会(事業報告・対処すべき課題)_Enhanced版.txt"
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(corrected_text)
    
    print(f"✅ Enhanced修正版を作成: {output_file}")
    print(f"🎯 適用された修正: {len(corrections_applied)}個")
    
    for correction in corrections_applied[:10]:  # 最初の10個を表示
        print(f"  • {correction}")
    
    if len(corrections_applied) > 10:
        print(f"  ... 他{len(corrections_applied)-10}個の修正")
    
    print(f"\n📊 改善結果:")
    print(f"  • 元の文字数: {len(original_text)}")
    print(f"  • 修正後文字数: {len(corrected_text)}")
    print(f"  • 精度向上: Enhanced修正により企業・金融用語が正確に")
    
    return output_file

if __name__ == "__main__":
    apply_enhanced_corrections()