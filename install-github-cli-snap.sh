#!/bin/bash

# GitHub CLI インストールスクリプト (Snap版)
# 作成日: $(date)

echo "🚀 GitHub CLI (Snap版) インストールを開始します..."

# エラー時に停止
set -e

# snapでGitHub CLIをインストール
echo "⬇️ Snapパッケージでインストール中..."
sudo snap install gh

# インストール確認
echo "✅ インストール確認中..."
if command -v gh &> /dev/null; then
    echo "🎉 GitHub CLI インストール完了！"
    echo "バージョン: $(gh --version)"
    echo ""
    echo "次のステップ:"
    echo "1. 認証: gh auth login"
    echo "2. プルリクエスト作成: gh pr create"
else
    echo "❌ インストールに失敗しました"
    exit 1
fi

echo ""
echo "🔐 GitHub認証を今すぐ実行しますか？ (y/n)"
read -r answer
if [[ "$answer" == "y" || "$answer" == "Y" ]]; then
    echo "🔑 GitHub認証を開始..."
    gh auth login
fi

echo "✨ 完了！"