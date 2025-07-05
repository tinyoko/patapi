# Claude開発履歴

このプロジェクトはClaude (Anthropic)によって開発されました。

## 開発環境情報
- **使用ツール**: Claude Code CLI
- **開発日**: 2025年7月5日
- **Python環境**: Python 3.12.3
- **Django バージョン**: 4.2.23

## 推奨コマンド
開発時によく使用するコマンド：

### 開発サーバー起動
```bash
source venv/bin/activate
python manage.py runserver 127.0.0.1:8003
```

### テストコマンド
```bash
python manage.py test
python manage.py check
```

### 依存関係管理
```bash
pip freeze > requirements.txt
```

## API設定注意点

### 特許庁API
- `.env`ファイルに実際の認証情報を設定する必要があります
- API利用は特許庁の利用規約に従ってください
- 残りアクセス回数に注意してください
- 使用するエンドポイント: 特許経過情報API（`app_progress`）

### OPD-API（新機能）
- 特許庁APIと同じOAuth2認証を使用
- ZIP形式のXMLファイルを取得・解析
- XMLパース処理のため、lxml、BeautifulSoup4が必要
- 使用するエンドポイント: 
  - `global_doc_list`: 書類一覧取得
  - `jp_doc_cont`: JP書類実体取得

## 開発ノート

### 特許庁APIデータ構造
実際のAPIレスポンスは以下の構造：
```
{
  "statusCode": "100",
  "errorMessage": "",
  "remainAccessCount": "XXX",
  "result": {
    "data": {
      "applicationNumber": "...",
      "inventionTitle": "...",
      "applicantAttorney": [...],
      "bibliographyInformation": [...],
      ...
    }
  }
}
```

### トラブルシューティング
- **ポート8000が使用中**: ポート8003を使用
- **ALLOWED_HOSTS設定**: localhost,127.0.0.1を設定済み
- **JavaScript表示問題**: ブラウザの強制リロード（Ctrl+F5）を推奨

### OPD-API開発ノート（2025年7月5日追加）

#### 新機能実装
1. **OPD-APIクライアント**: `patent_search/opd_utils.py`
   - OPDAPIClient: 書類一覧・実体取得
   - PatentXMLParser: XML解析・テキスト抽出

2. **新エンドポイント**: 
   - `/opd/documents/`: OPD書類一覧取得
   - `/opd/jp-text/`: JP書類テキスト抽出

3. **フロントエンド拡張**:
   - タブ切り替えUI
   - OPD専用ボタンとフィーチャー表示
   - 構造化テキスト表示

#### XML解析の特徴
- **マルチフォーマット対応**: 異なるXMLスキーマに対応
- **日本語XPath**: 英語・日本語の要素名に対応
- **セクション別抽出**: 発明の名称、請求項、明細書など
- **エラーハンドリング**: ZIP解析、XMLパースの堅牢性

#### 技術的改善点
- **依存関係追加**: lxml, BeautifulSoup4
- **モジュラー設計**: 既存コードと独立した実装
- **統一認証**: 特許庁APIと同じOAuth2トークン使用

### 今後の改善案
- [ ] 検索履歴機能
- [ ] 複数出願番号の一括検索
- [ ] PDF出力機能
- [ ] データキャッシュ機能
- [ ] テストカバレッジ向上
- [x] **OPD-API統合** ✅ (2025年7月5日完了)
- [ ] OPDテキスト検索・フィルタリング機能
- [ ] XMLファイルの直接ダウンロード機能