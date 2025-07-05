# API仕様書

このアプリケーションは2つの主要なAPIを統合しています：
1. **特許庁API**: 特許経過情報の取得
2. **OPD-API**: ワン・ポータル・ドシエの書類実体情報取得

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

---

## OPD-API（ワン・ポータル・ドシエAPI）

### 概要
OPD-APIは、特許出願に関連するXML形式の書類実体から日本語テキストを抽出する機能を提供します。
明細書、特許請求の範囲、図面の簡単な説明などのテキスト情報を構造化して取得できます。

### 認証
特許庁APIと同じOAuth2認証を使用

### エンドポイント

#### 1. OPD書類一覧取得
```
GET https://ip-data.jpo.go.jp/api/opd/v1/global_doc_list
Authorization: Bearer {access_token}
Accept: application/json
Parameters: application_number
```

**機能:**
- 指定された特許出願に関連する書類の一覧を取得
- 書類の種類、番号、日付などの基本情報を提供

#### 2. JP書類実体取得
```
GET https://ip-data.jpo.go.jp/api/opd/v1/jp_doc_cont
Authorization: Bearer {access_token}
Accept: application/zip
Parameters: application_number
```

**機能:**
- XML形式の書類実体をZIPファイルとして取得
- 明細書、特許請求の範囲などの詳細テキスト情報を含有

### アプリケーション内API

#### 1. OPD書類一覧取得
```
POST /opd/documents/
Content-Type: application/json
```

**リクエストボディ:**
```json
{
  "application_number": "2016045210"
}
```

**レスポンス:**
```json
{
  "success": true,
  "data": {
    // OPD書類一覧データ
  }
}
```

#### 2. JP書類テキスト抽出
```
POST /opd/jp-text/
Content-Type: application/json
```

**リクエストボディ:**
```json
{
  "application_number": "2016045210"
}
```

**レスポンス:**
```json
{
  "success": true,
  "data": {
    "application_number": "2016045210",
    "document_count": 2,
    "extracted_documents": {
      "document1.xml": [
        {
          "title": "発明の名称",
          "content": "エネルギーネットワークの運転制御装置"
        },
        {
          "title": "特許請求の範囲",
          "content": "請求項1: エネルギーネットワークにおいて..."
        },
        {
          "title": "発明の詳細な説明",
          "content": "【技術分野】\n本発明は..."
        }
      ]
    }
  }
}
```

### 抽出されるテキストセクション

- **発明の名称**: 特許のタイトル
- **要約**: 発明の概要
- **特許請求の範囲**: 権利範囲を定義する請求項
- **技術分野**: 発明が属する技術領域
- **背景技術**: 従来技術と課題
- **発明の開示**: 発明の内容と効果
- **図面の簡単な説明**: 図面の説明
- **発明の詳細な説明**: 実施形態の詳細
- **明細書**: その他の詳細情報

### XML解析の特徴

1. **複数フォーマット対応**: 異なるXMLスキーマに対応
2. **日本語テキスト抽出**: 日本語および英語のXPath表現を使用
3. **構造化データ**: セクション別に整理されたテキスト出力
4. **エラーハンドリング**: XMLパースエラーや欠損データの適切な処理

### エラーレスポンス

```json
{
  "error": "出願番号が入力されていません"
}
```

```json
{
  "error": "JP書類実体の取得に失敗しました"
}
```

```json
{
  "error": "XMLファイルからのテキスト抽出に失敗しました"
}
```