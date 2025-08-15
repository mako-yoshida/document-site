#!/bin/bash

# GitHub CLI インストールスクリプト
# 作成日: $(date)

echo "🚀 GitHub CLI インストールを開始します..."

# エラー時に停止
set -e

# 1. GitHub CLIの公式リポジトリを追加
echo "📦 GitHub CLIリポジトリを追加中..."
curl -fsSL https://cli.github.com/packages/githubcli-archive-keyring.gpg | sudo dd of=/usr/share/keyrings/githubcli-archive-keyring.gpg
sudo chmod go+r /usr/share/keyrings/githubcli-archive-keyring.gpg
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/githubcli-archive-keyring.gpg] https://cli.github.com/packages stable main" | sudo tee /etc/apt/sources.list.d/github-cli.list > /dev/null

# 2. パッケージリストを更新
echo "🔄 パッケージリストを更新中..."
sudo apt update

# 3. GitHub CLIをインストール
echo "⬇️ GitHub CLIをインストール中..."
sudo apt install -y gh

# 4. インストール確認
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