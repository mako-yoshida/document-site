// ナビゲーション機能
class Navigation {
    constructor() {
        this.fileTree = document.getElementById('fileTree');
        this.searchInput = document.getElementById('searchInput');
        this.files = [];
        this.mobileMenuOpen = false;
        this.init();
    }

    async init() {
        await this.loadFileStructure();
        this.renderFileTree();
        this.setupSearch();
        this.setupMobileMenu();
    }

    // ファイル構造を読み込み
    async loadFileStructure() {
        try {
            // documentsフォルダの構造を取得（キャッシュバスティング）
            const timestamp = Date.now();
            const response = await fetch(`documents/config.json?v=${timestamp}`, {
                cache: 'no-cache',
                headers: {
                    'Cache-Control': 'no-cache'
                }
            });
            if (response.ok) {
                const config = await response.json();
                this.files = config.files;
            } else {
                // config.jsonが無い場合のデフォルト構造
                this.files = [
                    {
                        name: 'sample-folder',
                        type: 'folder',
                        children: [
                            { name: 'sample.txt', type: 'file', path: 'documents/sample-folder/sample.txt' },
                            { name: 'readme.md', type: 'file', path: 'documents/sample-folder/readme.md' }
                        ]
                    }
                ];
            }
        } catch (error) {
            console.error('ファイル構造の読み込みに失敗:', error);
            this.files = [];
        }
    }

    // ファイルツリーをレンダリング
    renderFileTree(filteredFiles = null) {
        const files = filteredFiles || this.files;
        this.fileTree.innerHTML = '';
        
        if (files.length === 0) {
            this.fileTree.innerHTML = '<div class="loading">ファイルがありません</div>';
            return;
        }

        files.forEach(item => {
            this.renderTreeItem(item, this.fileTree, 0);
        });
    }

    // ツリーアイテムを描画
    renderTreeItem(item, container, level) {
        const itemElement = document.createElement('div');
        itemElement.className = `tree-item ${item.type}`;
        itemElement.style.paddingLeft = `${level * 20 + 10}px`;

        if (item.type === 'folder') {
            itemElement.innerHTML = `📁 ${item.name}`;
            itemElement.addEventListener('click', () => {
                this.toggleFolder(itemElement, item);
            });
        } else {
            itemElement.innerHTML = `📄 ${item.name}`;
            itemElement.addEventListener('click', () => {
                this.openFile(item);
            });
        }

        container.appendChild(itemElement);

        // フォルダの子要素
        if (item.type === 'folder' && item.children) {
            const childrenContainer = document.createElement('div');
            childrenContainer.className = 'folder-children';
            childrenContainer.style.display = 'none';
            
            item.children.forEach(child => {
                this.renderTreeItem(child, childrenContainer, level + 1);
            });
            
            container.appendChild(childrenContainer);
        }
    }

    // フォルダの開閉
    toggleFolder(element, folder) {
        const children = element.nextElementSibling;
        if (children && children.classList.contains('folder-children')) {
            const isOpen = children.style.display !== 'none';
            children.style.display = isOpen ? 'none' : 'block';
            
            // アイコン変更
            const icon = isOpen ? '📁' : '📂';
            element.innerHTML = `${icon} ${folder.name}`;
        }
    }

    // ファイルを開く
    openFile(file) {
        const event = new CustomEvent('fileSelected', {
            detail: { file: file }
        });
        document.dispatchEvent(event);
    }

    // 検索機能
    setupSearch() {
        this.searchInput.addEventListener('input', (e) => {
            const query = e.target.value.toLowerCase().trim();
            
            if (query === '') {
                this.renderFileTree();
                return;
            }

            const filteredFiles = this.filterFiles(this.files, query);
            this.renderFileTree(filteredFiles);
        });
    }

    // ファイルをフィルタリング
    filterFiles(files, query) {
        const filtered = [];
        
        files.forEach(item => {
            if (item.type === 'file') {
                if (item.name.toLowerCase().includes(query)) {
                    filtered.push(item);
                }
            } else if (item.type === 'folder') {
                const childMatches = this.filterFiles(item.children || [], query);
                if (childMatches.length > 0) {
                    filtered.push({
                        ...item,
                        children: childMatches
                    });
                }
                // フォルダ名もマッチする場合
                if (item.name.toLowerCase().includes(query)) {
                    filtered.push(item);
                }
            }
        });

        return filtered;
    }

    // モバイルメニューのセットアップ
    setupMobileMenu() {
        const mobileMenuButton = document.querySelector('.md\\:hidden .fixed');
        const sidebar = document.querySelector('aside');
        
        if (!mobileMenuButton || !sidebar) {
            console.warn('Mobile menu elements not found');
            return;
        }

        // ハンバーガーメニューボタンのクリックイベント
        mobileMenuButton.addEventListener('click', (e) => {
            e.preventDefault();
            this.toggleMobileMenu();
        });

        // オーバーレイの作成
        this.createMobileOverlay();
        
        // 画面リサイズ時の処理
        window.addEventListener('resize', () => {
            if (window.innerWidth >= 768 && this.mobileMenuOpen) {
                this.closeMobileMenu();
            }
        });
    }

    // モバイルオーバーレイの作成
    createMobileOverlay() {
        const overlay = document.createElement('div');
        overlay.className = 'mobile-overlay';
        overlay.addEventListener('click', () => {
            this.closeMobileMenu();
        });
        document.body.appendChild(overlay);
    }

    // モバイルメニューの開閉切り替え
    toggleMobileMenu() {
        if (this.mobileMenuOpen) {
            this.closeMobileMenu();
        } else {
            this.openMobileMenu();
        }
    }

    // モバイルメニューを開く
    openMobileMenu() {
        const sidebar = document.querySelector('aside');
        const overlay = document.querySelector('.mobile-overlay');
        
        if (sidebar && overlay) {
            sidebar.classList.add('mobile-sidebar', 'open');
            overlay.classList.add('show');
            this.mobileMenuOpen = true;
            
            // スクロールを無効化
            document.body.style.overflow = 'hidden';
        }
    }

    // モバイルメニューを閉じる
    closeMobileMenu() {
        const sidebar = document.querySelector('aside');
        const overlay = document.querySelector('.mobile-overlay');
        
        if (sidebar && overlay) {
            sidebar.classList.remove('mobile-sidebar', 'open');
            overlay.classList.remove('show');
            this.mobileMenuOpen = false;
            
            // スクロールを有効化
            document.body.style.overflow = '';
        }
    }
}

// 初期化
document.addEventListener('DOMContentLoaded', () => {
    window.navigation = new Navigation();
});