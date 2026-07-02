# ニュース＆株価要約・通知Bot 仕様書

## 1. システム概要
本システムは、1日1回（指定時刻）にGitHub ActionsのCronトリガーによって起動し、特定のテーマ（例：半導体）に関連する最新ニュースと関連銘柄の株価データを取得、Google Gemini APIを用いてその内容を要約・分析した上で、指定のチャットツール（Webhook）へ通知する自動化Botである。

## 2. 技術スタック
- プログラミング言語: Python 3.11以上
- ニュース取得: feedparser (Google News RSS)
- 株価取得: yfinance (Yahoo Finance API)
- AIモデル: google-generativeai (gemini-3.5-flash)
- 通知送信: requests (DiscordまたはSlack互換Webhook)
- CI/CD・実行環境: GitHub Actions
- テストフレームワーク: pytest, pytest-mock, responses

## 3. ディレクトリ構成
```
project_root/
├── .github/
│   └── workflows/
│       └── daily_summary.yml   # GitHub Actions定義ファイル
├── src/
│   ├── __init__.py
│   ├── main.py                 # エントリーポイント
│   ├── config.py               # 環境変数・設定管理
│   ├── fetcher.py              # ニュース・株価取得ロジック
│   ├── ai_summarizer.py        # Gemini API連携ロジック
│   └── notifier.py             # 通知ロジック
├── tests/
│   ├── __init__.py
│   ├── test_fetcher.py
│   ├── test_ai_summarizer.py
│   ├── test_notifier.py
│   └── test_main.py
├── requirements.txt
├── .env.example
└── SPEC.md                     # 本仕様書
```

## 4. 詳細機能要件

### 4.1. データ取得ロジック (src/fetcher.py)
- **ニュース取得機能**:
  - 引数として「検索キーワード（テーマ）」を受け取る。
  - Google News RSSフィードから、直近24時間以内のニュースタイトルとURL、要約を最大5〜10件取得する。
- **株価取得機能**:
  - 引数として「ティッカーシンボルのリスト」を受け取る。
  - `yfinance`を使用し、前日終値、前日比（％および実数）、出来高を取得する。

### 4.2. AI要約ロジック (src/ai_summarizer.py)
- **Gemini連携**:
  - 取得データをプロンプトに組み込み、Gemini APIへ送信する。
  - プロの金融アナリストとして、該当テーマの市場動向を300〜400文字程度で要約。
  - 箇条書きを活用し、視覚的に読みやすくする。
  - tenacityライブラリ等でエラー時のリトライを実装する。

### 4.3. 通知ロジック (src/notifier.py)
- **Webhook送信**:
  - Webhook URLに含まれる文字列（例: `discord.com`）を自動判定し、Discord用 (`content`) またはSlack用 (`text`) の適切なJSONペイロードを構築し、POST送信する。
  - エラー時は例外をスローする。

### 4.4. 実行環境・自動化 (GitHub Actions: daily_summary.yml)
- **トリガー**: `schedule` (cron) で平日日本時間の午前8時（UTC午後11時）に実行。
- **手順**: コードチェックアウト → Pythonセットアップ → 依存関係インストール → pytest実行 → `src/main.py`実行。

## 5. 環境変数・設定項目
- `GEMINI_API_KEY`: Google Gemini APIキー
- `WEBHOOK_URL`: 通知先Webhook URL
- `TARGET_THEME`: 検索対象テーマ (デフォルト: "半導体")
- `TARGET_TICKERS`: 対象銘柄カンマ区切り (デフォルト: "NVDA,TSM,6920.T")

## 6. テスト仕様
- 外部APIへの通信はすべてモック化し、各モジュールとメインロジックの動作検証を行う。
