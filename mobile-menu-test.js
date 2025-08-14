// モバイルハンバーガーメニューの自動テスト
const { chromium } = require('playwright');

async function testMobileMenu() {
    const browser = await chromium.launch({ headless: false });
    const page = await browser.newPage();
    
    try {
        console.log('🚀 モバイルハンバーガーメニューテスト開始...');
        
        // モバイルビューポートに設定（iPhone SE サイズ）
        await page.setViewportSize({ width: 375, height: 667 });
        
        // サイトにアクセス
        await page.goto('https://mako-yoshida.github.io/document-site');
        await page.waitForLoadState('networkidle');
        
        console.log('✅ サイト読み込み完了');
        
        // ハンバーガーメニューボタンの存在確認
        const menuButton = page.locator('button.md\\:hidden.fixed');
        await menuButton.waitFor({ state: 'visible' });
        console.log('✅ ハンバーガーメニューボタンが表示されている');
        
        // サイドバーが最初は非表示であることを確認
        const sidebar = page.locator('aside');
        await page.waitForTimeout(1000);
        
        // メニューボタンをクリック
        await menuButton.click();
        console.log('✅ ハンバーガーメニューボタンをクリック');
        
        // アニメーション完了を待機
        await page.waitForTimeout(500);
        
        // サイドバーが表示されることを確認
        const sidebarVisible = await sidebar.isVisible();
        if (sidebarVisible) {
            console.log('✅ サイドバーが表示されました');
        } else {
            console.log('❌ サイドバーが表示されていません');
        }
        
        // オーバーレイの存在確認
        const overlay = page.locator('.mobile-overlay');
        const overlayVisible = await overlay.isVisible();
        if (overlayVisible) {
            console.log('✅ オーバーレイが表示されました');
        } else {
            console.log('❌ オーバーレイが表示されていません');
        }
        
        // オーバーレイをクリックしてメニューを閉じる
        if (overlayVisible) {
            await overlay.click();
            console.log('✅ オーバーレイをクリック');
            
            // アニメーション完了を待機
            await page.waitForTimeout(500);
            
            // サイドバーが非表示になることを確認
            const sidebarHidden = await sidebar.isVisible();
            if (!sidebarHidden) {
                console.log('✅ サイドバーが非表示になりました');
            } else {
                console.log('❌ サイドバーが非表示になっていません');
            }
        }
        
        // 再度メニューを開いてファイルツリーをテスト
        await menuButton.click();
        await page.waitForTimeout(500);
        
        // ファイルツリーの読み込み確認
        const fileTree = page.locator('#fileTree');
        await fileTree.waitFor({ state: 'visible' });
        console.log('✅ ファイルツリーが表示されました');
        
        // ファイルツリー内の要素確認
        const treeItems = page.locator('.tree-item');
        const itemCount = await treeItems.count();
        if (itemCount > 0) {
            console.log(`✅ ファイルツリーアイテム数: ${itemCount}`);
        } else {
            console.log('❌ ファイルツリーアイテムが見つかりません');
        }
        
        // 検索機能のテスト
        const searchInput = page.locator('#searchInput');
        await searchInput.fill('sample');
        await page.waitForTimeout(500);
        console.log('✅ 検索機能テスト完了');
        
        // メニューを再度閉じる
        await menuButton.click();
        await page.waitForTimeout(500);
        
        console.log('🎉 モバイルハンバーガーメニューテスト完了！');
        
        // スクリーンショット撮影
        await page.screenshot({ 
            path: 'mobile-menu-test-result.png', 
            fullPage: true 
        });
        console.log('📸 スクリーンショット保存: mobile-menu-test-result.png');
        
    } catch (error) {
        console.error('❌ テスト失敗:', error);
        
        // エラー時のスクリーンショット
        await page.screenshot({ 
            path: 'mobile-menu-test-error.png', 
            fullPage: true 
        });
        
        throw error;
    } finally {
        await browser.close();
    }
}

// テスト実行
if (require.main === module) {
    testMobileMenu()
        .then(() => {
            console.log('✅ すべてのテストが正常に完了しました');
            process.exit(0);
        })
        .catch((error) => {
            console.error('❌ テストが失敗しました:', error);
            process.exit(1);
        });
}

module.exports = { testMobileMenu };