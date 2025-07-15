# Claude開発履歴

このプロジェクトはClaude (Anthropic)によって開発されました。

## 開発環境情報
- **使用ツール**: Claude Code CLI
- **開発日**: 2025年7月5日
- **更新日**: 2025年7月14日
- **Python環境**: Python 3.12.3
- **Django バージョン**: 4.2.23

## 推奨コマンド
開発時によく使用するコマンド：

### 開発サーバー起動
```bash
source venv/bin/activate

# 基本的な起動
python manage.py runserver 127.0.0.1:8000

# バックグラウンドで起動（推奨）
nohup python manage.py runserver 127.0.0.1:8000 > server.log 2>&1 &

# サーバーの動作確認
curl -I http://127.0.0.1:8000/
```

### テストコマンド
```bash
python manage.py test
python manage.py check

# サーバーの動作チェック
curl -X POST http://127.0.0.1:8000/search/ \
  -H "Content-Type: application/json" \
  -d '{"application_number": "2014192333"}'
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

### .envファイルの設定確認
```bash
# .envファイルの存在確認
ls -la .env

# .envファイルの内容確認（パスワードは非表示）
grep -v PASSWORD .env
```

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

#### サーバー起動関連
- **接続拒否エラー (ERR_CONNECTION_REFUSED)**:
  ```bash
  # サーバープロセスの確認
  ps aux | grep "python.*manage.py.*runserver"
  
  # プロセスを終了して再起動
  pkill -f "python.*manage.py.*runserver"
  nohup python manage.py runserver 127.0.0.1:8000 > server.log 2>&1 &
  ```

- **ポート競合問題**: ポート8000が使用中の場合
  ```bash
  # 別のポートで起動
  python manage.py runserver 127.0.0.1:8080
  # または
  python manage.py runserver 127.0.0.1:8003
  ```

#### アプリケーション関連
- **ALLOWED_HOSTS設定**: localhost,127.0.0.1を設定済み
- **JavaScript表示問題**: ブラウザの強制リロード（Ctrl+F5）を推奨
- **ネットワークエラー**: .envファイルの設定とサーバー再起動を確認

#### サーバー管理コマンド
```bash
# サーバーの状態確認
netstat -an | grep 8000

# サーバーの接続テスト
curl -I http://127.0.0.1:8000/

# サーバーログの確認
tail -f server.log
```

## 実際のセットアップ手順

### 1. リポジトリのクローンと初期化
```bash
git clone https://github.com/tinyoko/patapi.git
cd patapi
# 最初のコミット状態にリセット（開発用）
git reset --hard e895a26
```

### 2. 環境構築
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 3. .envファイルの設定
```bash
# .envファイルをプロジェクトルートに配置
# 必要な設定項目を確認
ls -la .env
grep -v PASSWORD .env  # パスワード以外の設定を確認
```

### 4. データベースの初期化とサーバー起動
```bash
python manage.py migrate
nohup python manage.py runserver 127.0.0.1:8000 > server.log 2>&1 &
```

### 5. 動作確認
```bash
curl -I http://127.0.0.1:8000/
# ブラウザで http://127.0.0.1:8000/ にアクセス
```

### 今後の改善案
- [ ] 検索履歴機能
- [ ] 複数出願番号の一括検索
- [ ] PDF出力機能
- [ ] データキャッシュ機能
- [ ] テストカバレッジ向上
- [ ] サーバー起動時のエラーハンドリング改善