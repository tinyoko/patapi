# 特許庁API Webアプリケーション

特許庁APIを使用した特許情報取得Webアプリケーションです。

> **開発履歴**: このプロジェクトは Claude (Anthropic) によって開発されました。詳細は [CLAUDE.md](./CLAUDE.md) をご覧ください。

## 機能

- 特許出願番号による検索
- 特許庁APIからのリアルタイム情報取得
- **構造化されたテーブル表示**: 基本情報、出願人情報、書誌情報を整理して表示
- **JSON表示切り替え**: 生データの確認も可能
- **詳細な特許情報**: 出願日、公開日、登録日、満了日など包括的な情報表示
- エラーハンドリングとローディング表示

## 技術スタック

- **バックエンド**: Python Django 4.2
- **フロントエンド**: HTML, CSS, JavaScript
- **API通信**: Python requests
- **データベース**: SQLite (Django標準)

## セットアップ

### 1. リポジトリのクローン

```bash
cd /path/to/your/project
```

### 2. 仮想環境の作成とアクティベート

```bash
python3 -m venv venv
source venv/bin/activate  # Windowsの場合: venv\Scripts\activate
```

### 3. 依存関係のインストール

```bash
pip install -r requirements.txt
```

### 4. 環境変数の設定

```bash
cp .env.example .env
```

`.env`ファイルを編集して、特許庁APIの認証情報を設定してください：

```env
PATENT_API_USERNAME=your-actual-username
PATENT_API_PASSWORD=your-actual-password
```

### 5. データベースの初期化

```bash
python manage.py migrate
```

### 6. 開発サーバーの起動

```bash
python manage.py runserver 127.0.0.1:8003
```

> **注意**: ポート8000が使用中の場合は8003を使用してください。

## 使用方法

1. ブラウザで `http://127.0.0.1:8003/` にアクセス
2. 特許出願番号を入力（例：2014192333）
3. 「検索」ボタンをクリック
4. 結果をテーブル表示またはJSON表示で確認

### 表示される情報
- **基本情報**: 出願番号、発明の名称、各種日付、登録番号
- **出願人・代理人情報**: 名称、コード、分類
- **書誌情報**: 文書リストの詳細
- **特許期間・状態情報**: 満了日、消滅日、消去識別子
- **公開番号情報**: 公開番号、AD公開番号
- **国際出願情報**: 国際出願番号、国際公開情報

## API仕様

### 特許庁API
- **認証**: OAuth2 password grant
- **トークン取得**: POST https://ip-data.jpo.go.jp/auth/token
- **データ取得**: GET https://ip-data.jpo.go.jp/api/patent/v1/app_progress/{出願番号}
  - **エンドポイント機能**: 特許経過情報（出願から登録までの経過情報）の取得

### 内部API
- **POST /search/**: 特許情報検索
  - Body: `{"application_number": "2014192333"}`
  - Response: 構造化された特許情報JSON

## 設定可能な環境変数

| 変数名 | 説明 | デフォルト値 |
|--------|------|--------------|
| `SECRET_KEY` | Django secret key | ランダム値 |
| `DEBUG` | デバッグモード | `True` |
| `ALLOWED_HOSTS` | 許可されたホスト | `localhost,127.0.0.1` |
| `PATENT_API_BASE_URL` | 特許庁API base URL | `https://ip-data.jpo.go.jp` |
| `PATENT_API_USERNAME` | 特許庁API ユーザー名 | (必須) |
| `PATENT_API_PASSWORD` | 特許庁API パスワード | (必須) |
| `PATENT_API_TOKEN_URL` | トークン取得URL | `https://ip-data.jpo.go.jp/auth/token` |
| `PATENT_API_DATA_URL` | データ取得URL | `https://ip-data.jpo.go.jp/api/patent/v1/app_progress` |

## トラブルシューティング

### よくある問題

1. **API認証エラー**: `.env`ファイルの認証情報を確認してください
2. **ポート8000が使用中**: ポート8003を使用してください
3. **テーブル表示されない**: ブラウザの強制リロード（Ctrl+F5）を試してください
4. **CORS エラー**: `settings.py`の`CORS_ALLOWED_ORIGINS`を確認してください
5. **モジュールエラー**: 仮想環境がアクティブになっているか確認してください

### ログの確認

```bash
# Djangoのログを確認
python manage.py runserver --verbosity=2
```

## 開発

### 新しい機能の追加

1. `patent_search/views.py`にビューを追加
2. `patent_search/urls.py`にURLパターンを追加
3. `templates/patent_search/`にテンプレートを追加

### テストの実行

```bash
python manage.py test
```

## ライセンス

MIT License