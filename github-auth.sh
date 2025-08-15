#!/bin/bash

# GitHub CLI認証スクリプト
# Personal Access Tokenを使用

echo "GitHub Personal Access Tokenを入力してください:"
read -s TOKEN

echo "$TOKEN" | gh auth login --with-token

echo "認証完了を確認中..."
gh auth status

echo "認証が完了しました！"