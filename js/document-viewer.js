// ドキュメントビューワー機能
class DocumentViewer {
    constructor() {
        this.welcomeMessage = document.querySelector('.welcome-message');
        this.documentViewer = document.getElementById('documentViewer');
        this.documentContent = document.getElementById('documentContent');
        this.breadcrumb = document.getElementById('breadcrumb');
        this.backButton = document.getElementById('backButton');
        
        this.currentFile = null;
        this.init();
    }

    init() {
        // ファイル選択イベントをリッスン
        document.addEventListener('fileSelected', (e) => {
            this.openDocument(e.detail.file);
        });

        // 戻るボタンのイベント
        this.backButton.addEventListener('click', () => {
            this.showWelcomeMessage();
        });
    }

    // ドキュメントを開く
    async openDocument(file) {
        try {
            this.showLoading();
            
            const fileData = await window.fileLoader.loadFile(file.path);
            this.currentFile = { ...file, ...fileData };
            
            this.updateBreadcrumb(file);
            this.renderDocument(fileData);
            this.showDocumentViewer();
            
        } catch (error) {
            this.showError(`ファイルの読み込みに失敗しました: ${error.message}`);
        }
    }

    // パンくずリストを更新
    updateBreadcrumb(file) {
        const pathParts = file.path.split('/');
        pathParts.shift(); // 'documents' を除去
        
        this.breadcrumb.innerHTML = `📁 ${pathParts.join(' / ')}`;
    }

    // ドキュメントをレンダリング
    renderDocument(fileData) {
        this.documentContent.innerHTML = '';

        switch (fileData.type) {
            case 'text':
                this.renderTextDocument(fileData);
                break;
            case 'pdf':
                this.renderPdfDocument(fileData);
                break;
            default:
                this.showError('サポートされていないファイル形式です');
        }
    }

    // テキストドキュメントをレンダリング
    renderTextDocument(fileData) {
        const container = document.createElement('div');
        
        if (fileData.format === 'markdown') {
            container.className = 'markdown-content';
            container.innerHTML = this.parseMarkdown(fileData.content);
        } else {
            container.className = 'text-content';
            container.textContent = fileData.content;
        }
        
        this.documentContent.appendChild(container);
    }

    // 簡単なMarkdownパーサー
    parseMarkdown(content) {
        return content
            .replace(/^# (.*$)/gim, '<h1>$1</h1>')
            .replace(/^## (.*$)/gim, '<h2>$1</h2>')
            .replace(/^### (.*$)/gim, '<h3>$1</h3>')
            .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
            .replace(/\*(.*?)\*/g, '<em>$1</em>')
            .replace(/`(.*?)`/g, '<code>$1</code>')
            .replace(/```([\s\S]*?)```/g, '<pre><code>$1</code></pre>')
            .replace(/^\- (.*$)/gim, '<li>$1</li>')
            .replace(/(<li>.*<\/li>)/s, '<ul>$1</ul>')
            .replace(/\n\n/g, '</p><p>')
            .replace(/^(?!<[h|u|p])(.+)/gm, '<p>$1</p>')
            .replace(/<p><\/p>/g, '');
    }

    // PDFドキュメントをレンダリング
    renderPdfDocument(fileData) {
        const container = document.createElement('div');
        container.className = 'pdf-container';
        
        const iframe = document.createElement('iframe');
        iframe.src = fileData.path;
        iframe.style.width = '100%';
        iframe.style.height = '600px';
        
        container.appendChild(iframe);
        this.documentContent.appendChild(container);

        // PDF.jsを使った高度な表示（オプション）
        this.enhancePdfViewer(container, fileData.path);
    }

    // PDF.jsを使った拡張表示
    enhancePdfViewer(container, pdfPath) {
        // PDF.jsが利用可能な場合の処理
        if (typeof pdfjsLib !== 'undefined') {
            const canvas = document.createElement('canvas');
            const context = canvas.getContext('2d');
            
            pdfjsLib.getDocument(pdfPath).promise.then(pdf => {
                pdf.getPage(1).then(page => {
                    const viewport = page.getViewport({ scale: 1.5 });
                    canvas.height = viewport.height;
                    canvas.width = viewport.width;

                    const renderContext = {
                        canvasContext: context,
                        viewport: viewport
                    };
                    
                    page.render(renderContext);
                });
            });
            
            container.appendChild(canvas);
        }
    }

    // 読み込み中表示
    showLoading() {
        this.documentContent.innerHTML = '<div class="loading">読み込み中...</div>';
        this.showDocumentViewer();
    }

    // エラー表示
    showError(message) {
        this.documentContent.innerHTML = 
            `<div class="error-message">❌ ${message}</div>`;
        this.showDocumentViewer();
    }

    // ウェルカムメッセージを表示
    showWelcomeMessage() {
        this.documentViewer.style.display = 'none';
        this.welcomeMessage.style.display = 'block';
        this.currentFile = null;
    }

    // ドキュメントビューワーを表示
    showDocumentViewer() {
        this.welcomeMessage.style.display = 'none';
        this.documentViewer.style.display = 'block';
    }

    // 現在のファイル情報を取得
    getCurrentFile() {
        return this.currentFile;
    }

    // ファイルをダウンロード
    downloadCurrentFile() {
        if (!this.currentFile) return;
        
        const link = document.createElement('a');
        link.href = this.currentFile.path;
        link.download = this.currentFile.filename;
        link.click();
    }
}

// 初期化
document.addEventListener('DOMContentLoaded', () => {
    window.documentViewer = new DocumentViewer();
});