# JavaScript 基礎

## はじめに
JavaScriptはWebブラウザ上で動作するプログラミング言語です。

## 基本構文

### 変数宣言
```javascript
// ES6以降の推奨記法
const name = "太郎";
let age = 25;

// 従来の記法（非推奨）
var city = "東京";
```

### 関数定義
```javascript
// 関数宣言
function greet(name) {
    return `こんにちは、${name}さん！`;
}

// アロー関数
const add = (a, b) => a + b;
```

### 配列操作
```javascript
const fruits = ['りんご', 'バナナ', 'オレンジ'];

// 要素追加
fruits.push('ぶどう');

// 要素検索
const hasApple = fruits.includes('りんご');

// 配列変換
const upperFruits = fruits.map(fruit => fruit.toUpperCase());
```

## DOM操作

### 要素の取得
```javascript
// IDで取得
const element = document.getElementById('myId');

// クラス名で取得
const elements = document.getElementsByClassName('myClass');

// セレクタで取得
const element = document.querySelector('.my-class');
```

### イベント処理
```javascript
button.addEventListener('click', function() {
    console.log('ボタンがクリックされました');
});
```

## 非同期処理

### Promiseとasync/await
```javascript
// Promise
fetch('/api/data')
    .then(response => response.json())
    .then(data => console.log(data));

// async/await
async function fetchData() {
    try {
        const response = await fetch('/api/data');
        const data = await response.json();
        return data;
    } catch (error) {
        console.error('エラー:', error);
    }
}
```

## まとめ
JavaScriptはWebアプリケーション開発には欠かせない言語です。
基本構文を理解して、段階的に学習を進めましょう。