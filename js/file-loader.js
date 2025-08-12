// ファイル読み込み機能
class FileLoader {
    constructor() {
        this.supportedFormats = {
            text: ['.txt', '.md', '.markdown', '.log', '.json', '.js', '.html', '.css'],
            pdf: ['.pdf']
        };
    }

    // ファイル形式を判定
    getFileType(filename) {
        const ext = this.getFileExtension(filename);
        
        if (this.supportedFormats.text.includes(ext)) {
            return 'text';
        } else if (this.supportedFormats.pdf.includes(ext)) {
            return 'pdf';
        }
        return 'unsupported';
    }

    // ファイル拡張子を取得
    getFileExtension(filename) {
        return filename.toLowerCase().substring(filename.lastIndexOf('.'));
    }

    // ファイルを読み込み
    async loadFile(filePath) {
        try {
            const response = await fetch(filePath);
            
            if (!response.ok) {
                throw new Error(`ファイルが見つかりません: ${response.status}`);
            }

            const fileType = this.getFileType(filePath);
            
            switch (fileType) {
                case 'text':
                    return await this.loadTextFile(response, filePath);
                case 'pdf':
                    return this.loadPdfFile(filePath);
                default:
                    throw new Error('サポートされていないファイル形式です');
            }
        } catch (error) {
            console.error('ファイル読み込みエラー:', error);
            throw error;
        }
    }

    // テキストファイルを読み込み
    async loadTextFile(response, filePath) {
        const content = await response.text();
        const extension = this.getFileExtension(filePath);
        
        return {
            type: 'text',
            content: content,
            format: extension === '.md' || extension === '.markdown' ? 'markdown' : 'plain',
            filename: filePath.split('/').pop()
        };
    }

    // PDFファイルを読み込み
    loadPdfFile(filePath) {
        return {
            type: 'pdf',
            path: filePath,
            filename: filePath.split('/').pop()
        };
    }

    // ファイルサイズを取得（概算）
    async getFileSize(filePath) {
        try {
            const response = await fetch(filePath, { method: 'HEAD' });
            const contentLength = response.headers.get('content-length');
            return contentLength ? parseInt(contentLength) : null;
        } catch (error) {
            return null;
        }
    }

    // ファイル情報を取得
    async getFileInfo(filePath) {
        const filename = filePath.split('/').pop();
        const extension = this.getFileExtension(filename);
        const type = this.getFileType(filename);
        const size = await this.getFileSize(filePath);

        return {
            filename,
            extension,
            type,
            size: size ? this.formatFileSize(size) : '不明',
            path: filePath
        };
    }

    // ファイルサイズをフォーマット
    formatFileSize(bytes) {
        if (bytes === 0) return '0 B';
        
        const k = 1024;
        const sizes = ['B', 'KB', 'MB', 'GB'];
        const i = Math.floor(Math.log(bytes) / Math.log(k));
        
        return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
    }
}

// グローバルインスタンス
window.fileLoader = new FileLoader();