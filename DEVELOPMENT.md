# 開発者ガイド

## 開発環境セットアップ

### 必要な環境
- Python 3.12+
- Django 4.2+
- 特許庁APIアクセス権限

### 推奨開発ツール
- VSCode または PyCharm
- Git
- Postman (API テスト用)

## プロジェクト構造

```
patent_api/
├── manage.py              # Django管理スクリプト
├── patent_api/           # プロジェクト設定
│   ├── settings.py       # Django設定
│   ├── urls.py           # URL設定
│   └── wsgi.py           # WSGI設定
├── patent_search/        # メインアプリケーション
│   ├── views.py          # ビューロジック
│   ├── urls.py           # URL設定
│   └── models.py         # データモデル
├── templates/            # HTMLテンプレート
│   └── patent_search/
│       └── index.html    # メインページ
├── requirements.txt      # Python依存関係
├── .env.example         # 環境変数テンプレート
└── .gitignore           # Git除外設定
```

## 開発フロー

### 1. ローカル開発
```bash
# 仮想環境作成・有効化
python3 -m venv venv
source venv/bin/activate

# 依存関係インストール
pip install -r requirements.txt

# 環境変数設定
cp .env.example .env
# .envファイルを編集

# データベース初期化
python manage.py migrate

# 開発サーバー起動
python manage.py runserver 127.0.0.1:8003
```

### 2. テスト実行
```bash
# 全テスト実行
python manage.py test

# 特定のテスト実行
python manage.py test patent_search.tests

# カバレッジ付きテスト
coverage run --source='.' manage.py test
coverage report
```

### 3. コード品質チェック
```bash
# Django設定チェック
python manage.py check

# セキュリティチェック
python manage.py check --deploy
```

## 主要コンポーネント

### PatentAPIClient クラス
特許庁APIとの通信を担当

**主要メソッド:**
- `get_token()`: 認証トークン取得
- `get_patent_data(application_number)`: 特許データ取得

### JavaScriptフロントエンド
`templates/patent_search/index.html`

**主要関数:**
- `showResults(data)`: 検索結果表示
- `addTableRow(key, value, isHeader)`: テーブル行追加
- `showTableView()` / `showJsonView()`: 表示切り替え

## 設定管理

### 環境変数
- `SECRET_KEY`: Django秘密鍵
- `DEBUG`: デバッグモード
- `ALLOWED_HOSTS`: 許可ホスト
- `PATENT_API_USERNAME`: 特許庁APIユーザー名
- `PATENT_API_PASSWORD`: 特許庁APIパスワード

### セキュリティ設定
- CORS設定済み
- CSRF保護有効
- 機密情報は環境変数で管理

## トラブルシューティング

### よくある問題

1. **ImportError**: 仮想環境が有効でない
   ```bash
   source venv/bin/activate
   ```

2. **ポート競合**: 8003ポート使用
   ```bash
   python manage.py runserver 127.0.0.1:8003
   ```

3. **API認証失敗**: `.env`設定確認
   ```bash
   cat .env | grep PATENT_API
   ```

4. **静的ファイル問題**: 開発環境では不要
   ```bash
   python manage.py collectstatic --noinput
   ```

### デバッグ手順

1. **Django設定確認**
   ```bash
   python manage.py diffsettings
   ```

2. **ログレベル調整**
   ```python
   # settings.py
   LOGGING = {
       'version': 1,
       'disable_existing_loggers': False,
       'handlers': {
           'console': {
               'class': 'logging.StreamHandler',
           },
       },
       'loggers': {
           'patent_search': {
               'handlers': ['console'],
               'level': 'DEBUG',
           },
       },
   }
   ```

3. **ブラウザ開発者ツール**
   - Network タブでAPI通信確認
   - Console タブでJavaScriptエラー確認

## 機能拡張

### 新機能追加手順

1. **モデル更新** (必要に応じて)
   ```python
   # patent_search/models.py
   class SearchHistory(models.Model):
       application_number = models.CharField(max_length=20)
       searched_at = models.DateTimeField(auto_now_add=True)
   ```

2. **ビュー追加**
   ```python
   # patent_search/views.py
   def search_history(request):
       # 検索履歴表示ロジック
       pass
   ```

3. **URL設定**
   ```python
   # patent_search/urls.py
   path('history/', views.search_history, name='search_history'),
   ```

4. **テンプレート作成**
   ```html
   <!-- templates/patent_search/history.html -->
   ```

### パフォーマンス最適化

1. **キャッシュ導入**
   ```python
   # settings.py
   CACHES = {
       'default': {
           'BACKEND': 'django.core.cache.backends.redis.RedisCache',
           'LOCATION': 'redis://127.0.0.1:6379/1',
       }
   }
   ```

2. **データベース最適化**
   ```python
   # インデックス追加
   class Meta:
       indexes = [
           models.Index(fields=['application_number']),
       ]
   ```

## 本番デプロイ

### 設定変更
```python
# settings.py
DEBUG = False
ALLOWED_HOSTS = ['your-domain.com']
SECRET_KEY = os.environ['SECRET_KEY']  # 強力な秘密鍵
```

### セキュリティチェックリスト
- [ ] SECRET_KEY を本番用に変更
- [ ] DEBUG = False に設定
- [ ] ALLOWED_HOSTS を適切に設定
- [ ] HTTPS 使用
- [ ] セキュリティヘッダー設定
- [ ] 機密情報の環境変数化