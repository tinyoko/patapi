# 国内特許情報取得API 14種類の詳細ドキュメント

このドキュメントでは、日本国特許庁が提供する14の特許情報取得APIについて詳細に説明します。

## 基本情報

- **ベースURL**: https://ip-data.jpo.go.jp
- **認証方式**: OAuth2 Bearer Token
- **レスポンス形式**: JSON
- **参考記事**: [Qiita - 14の国内特許情報取得APIの使い方](https://qiita.com/kenichiro_ayaki/items/fc3d400142d47c9c27b0)

## 認証について

各APIを使用する前に、トークンの取得が必要です：

```bash
curl -X POST https://ip-data.jpo.go.jp/auth/token \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "grant_type=password&username=YOUR_USERNAME&password=YOUR_PASSWORD"
```

## 14の特許情報取得API

### 1. 特許経過情報API
- **エンドポイント**: `GET /api/patent/v1/app_progress/{出願番号}`
- **機能**: 出願番号に基づき経過情報の一覧を取得
- **パラメータ**: 
  - `出願番号`: 特許出願番号（例：2016045210）
- **レスポンス**: 
  - 出願番号
  - 発明の名称
  - 申請人情報
  - 出願日
  - 公開番号
  - 登録情報
  - 書誌情報
  - 経過情報の詳細

**使用例**:
```bash
curl -H "Authorization: Bearer YOUR_TOKEN" \
  https://ip-data.jpo.go.jp/api/patent/v1/app_progress/2016045210
```

### 2. シンプル特許経過情報API
- **エンドポイント**: `GET /api/patent/v1/app_progress_simple/{出願番号}`
- **機能**: 優先権基礎情報などを除いた簡易的な経過情報を取得
- **パラメータ**: 
  - `出願番号`: 特許出願番号
- **レスポンス**: 基本的な出願情報（優先権情報除く）

**使用例**:
```bash
curl -H "Authorization: Bearer YOUR_TOKEN" \
  https://ip-data.jpo.go.jp/api/patent/v1/app_progress_simple/2016045210
```

### 3. 特許分割出願情報API
- **エンドポイント**: `GET /api/patent/v1/divisional_app_info/{出願番号}`
- **機能**: 分割出願に関する情報を取得
- **パラメータ**: 
  - `出願番号`: 特許出願番号
- **レスポンス**: 
  - 原出願情報
  - 分割出願群情報
  - 分割関係の詳細

**使用例**:
```bash
curl -H "Authorization: Bearer YOUR_TOKEN" \
  https://ip-data.jpo.go.jp/api/patent/v1/divisional_app_info/2016045210
```

### 4. 特許優先基礎出願情報API
- **エンドポイント**: `GET /api/patent/v1/priority_right_app_info/{出願番号}`
- **機能**: 優先権に関する基礎出願情報を取得
- **パラメータ**: 
  - `出願番号`: 特許出願番号
- **レスポンス**: 
  - パリ条約優先権情報
  - 国内優先権情報
  - 優先権基礎出願の詳細

**使用例**:
```bash
curl -H "Authorization: Bearer YOUR_TOKEN" \
  https://ip-data.jpo.go.jp/api/patent/v1/priority_right_app_info/2016045210
```

### 5. 特許申請人氏名・名称API
- **エンドポイント**: `GET /api/patent/v1/applicant_attorney_cd/{申請人コード}`
- **機能**: 申請人コードから氏名・名称を取得
- **パラメータ**: 
  - `申請人コード`: 申請人識別コード
- **レスポンス**: 
  - 申請人の名称
  - 申請人の詳細情報

**使用例**:
```bash
curl -H "Authorization: Bearer YOUR_TOKEN" \
  https://ip-data.jpo.go.jp/api/patent/v1/applicant_attorney_cd/123456789
```

### 6. 特許申請人コードAPI
- **エンドポイント**: `GET /api/patent/v1/applicant_attorney_name/{申請人名称}`
- **機能**: 申請人名称から申請人コードを取得
- **パラメータ**: 
  - `申請人名称`: 申請人の名称
- **レスポンス**: 
  - 申請人コード
  - 関連する申請人情報

**使用例**:
```bash
curl -H "Authorization: Bearer YOUR_TOKEN" \
  https://ip-data.jpo.go.jp/api/patent/v1/applicant_attorney_name/株式会社○○
```

### 7. 特許出願公開番号API
- **エンドポイント**: `GET /api/patent/v1/pub_num/{出願番号}`
- **機能**: 出願番号から公開番号を取得
- **パラメータ**: 
  - `出願番号`: 特許出願番号
- **レスポンス**: 
  - 公開番号
  - 公開日
  - 公開関連情報

**使用例**:
```bash
curl -H "Authorization: Bearer YOUR_TOKEN" \
  https://ip-data.jpo.go.jp/api/patent/v1/pub_num/2016045210
```

### 8. 特許登録番号API
- **エンドポイント**: `GET /api/patent/v1/reg_num/{出願番号}`
- **機能**: 出願番号から登録番号を取得
- **パラメータ**: 
  - `出願番号`: 特許出願番号
- **レスポンス**: 
  - 登録番号
  - 登録日
  - 登録関連情報

**使用例**:
```bash
curl -H "Authorization: Bearer YOUR_TOKEN" \
  https://ip-data.jpo.go.jp/api/patent/v1/reg_num/2016045210
```

### 9. 特許発送書類の実体ファイルAPI
- **エンドポイント**: `GET /api/patent/v1/app_doc_cont_refusal_reason_decision/{出願番号}`
- **機能**: 特許出願に関する発送書類の実体ファイルをZIPでダウンロード
- **パラメータ**: 
  - `出願番号`: 特許出願番号
- **レスポンス**: ZIP形式のファイル（発送書類の実体）

**使用例**:
```bash
curl -H "Authorization: Bearer YOUR_TOKEN" \
  https://ip-data.jpo.go.jp/api/patent/v1/app_doc_cont_refusal_reason_decision/2016045210 \
  -o documents.zip
```

### 10. 特許拒絶理由通知書API
- **エンドポイント**: `GET /api/patent/v1/app_doc_cont_refusal_reason/{出願番号}`
- **機能**: 拒絶理由通知書の実体ファイルをZIPでダウンロード
- **パラメータ**: 
  - `出願番号`: 特許出願番号
- **レスポンス**: ZIP形式のファイル（拒絶理由通知書）

**使用例**:
```bash
curl -H "Authorization: Bearer YOUR_TOKEN" \
  https://ip-data.jpo.go.jp/api/patent/v1/app_doc_cont_refusal_reason/2016045210 \
  -o refusal_reason.zip
```

### 11. 特許引用文献情報取得API
- **エンドポイント**: `GET /api/patent/v1/cite_doc_info/{出願番号}`
- **機能**: 拒絶理由の引用文献情報を取得
- **パラメータ**: 
  - `出願番号`: 特許出願番号
- **レスポンス**: 
  - 引用文献リスト
  - 引用文献の詳細情報
  - 引用理由

**使用例**:
```bash
curl -H "Authorization: Bearer YOUR_TOKEN" \
  https://ip-data.jpo.go.jp/api/patent/v1/cite_doc_info/2016045210
```

### 12. 特許登録情報API
- **エンドポイント**: `GET /api/patent/v1/registration_info/{出願番号}`
- **機能**: 特定の出願番号の登録情報を取得
- **パラメータ**: 
  - `出願番号`: 特許出願番号
- **レスポンス**: 
  - 登録番号
  - 登録日
  - 権利者情報
  - 登録関連の詳細情報

**使用例**:
```bash
curl -H "Authorization: Bearer YOUR_TOKEN" \
  https://ip-data.jpo.go.jp/api/patent/v1/registration_info/2016045210
```

### 13. 特許J-PlatPat固定アドレスAPI
- **エンドポイント**: `GET /api/patent/v1/jpp_fixed_address/{出願番号}`
- **機能**: J-PlatPat固定アドレス情報を取得
- **パラメータ**: 
  - `出願番号`: 特許出願番号
- **レスポンス**: 
  - J-PlatPat固定アドレス
  - 関連URL情報

**使用例**:
```bash
curl -H "Authorization: Bearer YOUR_TOKEN" \
  https://ip-data.jpo.go.jp/api/patent/v1/jpp_fixed_address/2016045210
```

### 14. 特許PCT出願の日本国内移行後の出願番号API
- **エンドポイント**: `GET /api/patent/v1/pct_app_num/{PCT出願番号}`
- **機能**: PCT出願番号から日本国内移行後の出願番号を取得
- **パラメータ**: 
  - `PCT出願番号`: PCT国際出願番号
- **レスポンス**: 
  - 日本国内移行後の出願番号
  - 移行日
  - 移行関連情報

**使用例**:
```bash
curl -H "Authorization: Bearer YOUR_TOKEN" \
  https://ip-data.jpo.go.jp/api/patent/v1/pct_app_num/PCT/JP2016/000001
```

## 利用上の注意点

1. **認証トークン**: すべてのAPIでBearerトークンが必要
2. **レート制限**: API利用には制限があるため、remainAccessCountを確認
3. **エラーハンドリング**: 各APIで適切なエラーハンドリングを実装
4. **データ形式**: レスポンスはJSON形式（ファイルダウンロード系は除く）

## 実装例（JavaScript）

```javascript
// 基本的なAPI呼び出し関数
async function callPatentAPI(endpoint, token) {
    const response = await fetch(`https://ip-data.jpo.go.jp${endpoint}`, {
        headers: {
            'Authorization': `Bearer ${token}`,
            'Accept': 'application/json'
        }
    });
    
    if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
    }
    
    return await response.json();
}

// 特許経過情報を取得する例
async function getPatentProgress(applicationNumber, token) {
    const endpoint = `/api/patent/v1/app_progress/${applicationNumber}`;
    return await callPatentAPI(endpoint, token);
}

// 使用例
(async () => {
    try {
        const token = 'YOUR_ACCESS_TOKEN';
        const applicationNumber = '2016045210';
        const data = await getPatentProgress(applicationNumber, token);
        console.log(data);
    } catch (error) {
        console.error('Error:', error);
    }
})();
```

## 本プロジェクトでの活用

現在のプロジェクトでは **特許経過情報API（1番目）** を使用していますが、以下のAPIも活用可能です：

- **2. シンプル特許経過情報API**: 簡潔な情報表示用
- **11. 特許引用文献情報取得API**: 引用文献の詳細表示
- **12. 特許登録情報API**: 登録状況の詳細表示
- **13. J-PlatPat固定アドレスAPI**: 外部リンク機能

これらのAPIを組み合わせることで、より充実した特許情報検索システムを構築できます。