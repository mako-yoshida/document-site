# GitHub Actions 管理ガイド

## 概要
このドキュメントは、document-siteプロジェクトのGitHub Actionsワークフローの停止・復旧手順を記載しています。

## ワークフロー構成
- **ファイル場所**: `.github/workflows/deploy-test.yml`
- **トリガー**: mainブランチへのpush
- **機能**: デプロイ後のPlaywrightテスト実行と証跡保存

---

## 停止方法

### 方法1: ワークフローファイルの削除（推奨）
```bash
# ローカルでファイル削除
rm .github/workflows/deploy-test.yml

# 変更をコミット・プッシュ
git add .
git commit -m "Disable GitHub Actions workflow"
git push origin main
```

### 方法2: GitHub UI上での無効化
1. GitHubリポジトリページにアクセス
2. `Actions` タブをクリック
3. 左側のワークフロー一覧から対象ワークフローを選択
4. 右上の `...` メニューから `Disable workflow` を選択

### 方法3: ファイル名変更（一時無効化）
```bash
# ファイル名を変更して無効化
mv .github/workflows/deploy-test.yml .github/workflows/deploy-test.yml.disabled

# 変更をコミット・プッシュ
git add .
git commit -m "Temporarily disable GitHub Actions workflow"
git push origin main
```

---

## 復旧方法

### 方法1からの復旧: ワークフローファイルの再作成
```bash
# 削除したワークフローファイルを復元
git log --oneline | grep "Disable GitHub Actions workflow"
# 上記で表示されたコミットハッシュの前のコミットをチェック
git show <コミットハッシュ>:.github/workflows/deploy-test.yml > .github/workflows/deploy-test.yml

# または、バックアップから復元
# （事前にworkflowファイルをバックアップしておく場合）

# 変更をコミット・プッシュ
git add .
git commit -m "Re-enable GitHub Actions workflow"
git push origin main
```

### 方法2からの復旧: GitHub UI上での有効化
1. GitHubリポジトリページにアクセス
2. `Actions` タブをクリック
3. 左側のワークフロー一覧から対象ワークフロー（無効化されたもの）を選択
4. `Enable workflow` ボタンをクリック

### 方法3からの復旧: ファイル名変更の取り消し
```bash
# ファイル名を元に戻す
mv .github/workflows/deploy-test.yml.disabled .github/workflows/deploy-test.yml

# 変更をコミット・プッシュ
git add .
git commit -m "Re-enable GitHub Actions workflow"
git push origin main
```

---

## 確認方法

### 停止確認
1. GitHubリポジトリの `Actions` タブで実行履歴を確認
2. 新しいpushでワークフローが実行されないことを確認
3. 既存の手動デプロイが正常動作することを確認

### 復旧確認
1. ダミーファイルをコミット・プッシュしてワークフロー実行を確認
2. `Actions` タブで実行履歴とステータスを確認
3. 証跡（スクリーンショット等）が正常に保存されることを確認

---

## 注意事項

- **既存運用への影響**: GitHub Actionsの停止・復旧は既存の手動デプロイには影響しません
- **バックアップ**: ワークフローファイルを削除する前に、設定内容をバックアップしておくことを推奨
- **テスト実行**: 復旧後は必ずテスト実行で動作確認を行ってください

---

## トラブルシューティング

### ワークフローが実行されない場合
- ファイルパス（`.github/workflows/`）が正しいか確認
- YAMLファイルの構文エラーがないか確認
- GitHub Actionsの利用制限に達していないか確認

### 復旧に失敗する場合
- Gitの履歴からワークフローファイルの内容を確認
- 手動でワークフローファイルを再作成
- GitHub Supportに問い合わせ

---

**作成日**: 2025-08-14  
**対象プロジェクト**: document-site  
**最終更新**: 2025-08-14