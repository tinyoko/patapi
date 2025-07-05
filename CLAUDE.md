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

## 特許庁API設定注意点
- `.env`ファイルに実際の認証情報を設定する必要があります
- API利用は特許庁の利用規約に従ってください
- 残りアクセス回数に注意してください
- 使用するエンドポイント: 特許経過情報API（`app_progress`）

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

### 今後の改善案
- [ ] 検索履歴機能
- [ ] 複数出願番号の一括検索
- [ ] PDF出力機能
- [ ] データキャッシュ機能
- [ ] テストカバレッジ向上