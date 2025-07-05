# API仕様書

## 特許庁API

### 認証
OAuth2 password grant方式を使用

### エンドポイント

#### 1. トークン取得
```
POST https://ip-data.jpo.go.jp/auth/token
Content-Type: application/x-www-form-urlencoded

grant_type=password&username=YOUR_USERNAME&password=YOUR_PASSWORD
```

**レスポンス例:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "expires_in": 3600
}
```

#### 2. 特許経過情報取得
特許の出願から登録までの経過情報を取得します。

```
GET https://ip-data.jpo.go.jp/api/patent/v1/app_progress/{application_number}
Authorization: Bearer {access_token}
Accept: application/json
```

**エンドポイント機能:**
- 特許出願の経過情報の取得
- 出願から登録までのプロセス情報
- 書誌的事項の詳細情報

**レスポンス構造:**
```json
{
  "statusCode": "100",
  "errorMessage": "",
  "remainAccessCount": "385",
  "result": {
    "data": {
      "applicationNumber": "2014192333",
      "inventionTitle": "エネルギーネットワークの運転制御装置及び運転制御方法",
      "filingDate": "20140922",
      "publicationDate": "20160425",
      "registrationDate": "20181026",
      "registrationNumber": "6422710",
      "expireDate": "20340922",
      "applicantAttorney": [
        {
          "applicantAttorneyCd": "000005108",
          "repeatNumber": "1",
          "name": "株式会社日立製作所",
          "applicantAttorneyClass": "1"
        }
      ],
      "bibliographyInformation": [
        {
          "numberType": "01",
          "number": "2014192333",
          "documentList": [
            {
              "legalDate": "20140922",
              "irirFlg": "0",
              "availabilityFlag": "1",
              "documentCode": "A63",
              "documentDescription": "明細書",
              "documentNumber": "51401938471"
            }
          ]
        }
      ]
    }
  }
}
```

## 内部API

### 特許情報検索

#### エンドポイント
```
POST /search/
Content-Type: application/json
```

#### リクエスト
```json
{
  "application_number": "2014192333"
}
```

#### レスポンス
```json
{
  "success": true,
  "data": {
    // 特許庁APIのレスポンスデータ
  }
}
```

#### エラーレスポンス
```json
{
  "error": "出願番号が入力されていません"
}
```

## データ構造詳細

### applicantAttorney配列
出願人・代理人情報
- `applicantAttorneyCd`: コード
- `repeatNumber`: 繰り返し番号
- `name`: 名称
- `applicantAttorneyClass`: 分類（1=出願人、2=代理人）

### bibliographyInformation配列
書誌情報
- `numberType`: 番号種別
- `number`: 番号
- `documentList`: 文書リスト
  - `legalDate`: 法定日付
  - `documentCode`: 文書コード
  - `documentDescription`: 文書説明
  - `documentNumber`: 文書番号

### 日付フォーマット
すべての日付は YYYYMMDD 形式