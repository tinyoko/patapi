# 特許庁API Webアプリケーション

特許庁APIを使用した特許情報取得Webアプリケーションです。

> **開発履歴**: このプロジェクトは Claude (Anthropic) によって開発されました。詳細は [CLAUDE.md](./CLAUDE.md) をご覧ください。

## 機能

- **14種類の特許情報取得API対応**: 特許経過情報、分割出願情報、優先権情報、申請人情報など
- **API選択機能**: ドロップダウンメニューから使用するAPIを選択可能
- **動的入力フィールド**: 選択したAPIに応じて入力フィールドが自動調整
- **構造化されたテーブル表示**: 基本情報、出願人情報、書誌情報を整理して表示
- **JSON表示切り替え**: 生データの確認も可能
- **詳細な特許情報**: 出願日、公開日、登録日、満了日など包括的な情報表示
- **ファイルダウンロードAPI対応**: 発送書類や拒絶理由通知書のダウンロード情報表示
- エラーハンドリングとローディング表示

## 技術スタック

- **バックエンド**: Python Django 4.2
- **フロントエンド**: HTML, CSS, JavaScript
- **API通信**: Python requests
- **データベース**: SQLite (Django標準)

## セットアップ

### 1. リポジトリのクローン

```bash
git clone https://github.com/tinyoko/patapi.git
cd patapi
```

### 2. 初期状態へのリセット（推奨）

開発を最初のコミット状態から始める場合：

```bash
git reset --hard e895a26  # 最初のコミット状態に戻す
```

### 3. 仮想環境の作成とアクティベート

```bash
python3 -m venv venv
source venv/bin/activate  # Windowsの場合: venv\Scripts\activate
```

### 4. 依存関係のインストール

```bash
pip install -r requirements.txt
```

### 5. 環境変数の設定

**重要**: `.env`ファイルはGit管理対象外のため、別途取得する必要があります。

`.env`ファイルの内容例：

```env
# Django settings
SECRET_KEY=django-insecure-3m#8g2n0uf65db9#up+=m&%tzs0ve9fpb95igvk_pzp1jz9ek$
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Patent API settings
PATENT_API_BASE_URL=https://ip-data.jpo.go.jp
PATENT_API_USERNAME=your-actual-username
PATENT_API_PASSWORD=your-actual-password
PATENT_API_TOKEN_URL=https://ip-data.jpo.go.jp/auth/token
PATENT_API_DATA_URL=https://ip-data.jpo.go.jp/api/patent/v1/app_progress
```

**確認方法**:
```bash
# .envファイルが存在するか確認
ls -la .env
```

### 6. データベースの初期化

```bash
python manage.py migrate
```

### 7. 開発サーバーの起動

**基本的な起動方法**:
```bash
python manage.py runserver 127.0.0.1:8000
```

**バックグラウンドで起動する場合**:
```bash
nohup python manage.py runserver 127.0.0.1:8000 > server.log 2>&1 &
```

**サーバーの動作確認**:
```bash
curl -I http://127.0.0.1:8000/
```

> **注意**: ポート8000が使用中の場合は8003や8080を使用してください。

## 使用方法

1. ブラウザで `http://127.0.0.1:8000/` にアクセス
2. **API種類を選択**（14種類から選択可能）
3. 選択したAPIに応じた検索値を入力
   - 特許出願番号（例：2014192333）
   - 申請人コード（例：123456789）
   - PCT出願番号（例：PCT/JP2016/000001）
4. 「検索」ボタンをクリック
5. 結果をテーブル表示またはJSON表示で確認

### 利用可能なAPI

| API名 | 機能 | 入力値 |
|-------|------|--------|
| 特許経過情報API | 包括的な特許情報を取得 | 特許出願番号 |
| シンプル特許経過情報API | 簡略化された特許情報を取得 | 特許出願番号 |
| 分割出願情報API | 分割出願の関係情報を取得 | 特許出願番号 |
| 優先権基礎出願情報API | 優先権の基礎情報を取得 | 特許出願番号 |
| 申請人氏名・名称API | 申請人コードから名称を取得 | 申請人コード |
| 申請人コードAPI | 申請人名称からコードを取得 | 申請人名称 |
| 出願公開番号API | 出願番号から公開番号を取得 | 特許出願番号 |
| 登録番号API | 出願番号から登録番号を取得 | 特許出願番号 |
| 発送書類の実体ファイルAPI | 発送書類をZIPでダウンロード | 特許出願番号 |
| 拒絶理由通知書API | 拒絶理由通知書をZIPでダウンロード | 特許出願番号 |
| 引用文献情報API | 引用文献情報を取得 | 特許出願番号 |
| 登録情報API | 詳細な登録情報を取得 | 特許出願番号 |
| J-PlatPat固定アドレスAPI | J-PlatPat固定アドレスを取得 | 特許出願番号 |
| PCT国内移行API | PCT出願の国内移行情報を取得 | PCT出願番号 |

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
2. **接続拒否エラー (ERR_CONNECTION_REFUSED)**:
   ```bash
   # サーバーが起動しているか確認
   ps aux | grep "python.*manage.py.*runserver"
   
   # ポートが使用されているか確認
   netstat -an | grep 8000
   
   # バックグラウンドで起動
   nohup python manage.py runserver 127.0.0.1:8000 > server.log 2>&1 &
   ```
3. **ポート競合**: 別のポートを使用してください
   ```bash
   python manage.py runserver 127.0.0.1:8080
   ```
4. **テーブル表示されない**: ブラウザの強制リロード（Ctrl+F5）を試してください
5. **CORS エラー**: `settings.py`の`CORS_ALLOWED_ORIGINS`を確認してください
6. **モジュールエラー**: 仮想環境がアクティブになっているか確認してください

### サーバー管理

**サーバーの停止**:
```bash
# 特定のプロセスを停止
pkill -f "python.*manage.py.*runserver"
```

**サーバーの状態確認**:
```bash
# プロセス確認
ps aux | grep python | grep manage

# 接続テスト
curl -I http://127.0.0.1:8000/
```

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