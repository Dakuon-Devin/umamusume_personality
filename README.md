# ウマ娘性格診断システム (RAG ベース)

ChatGPT との協働 PJ です。

このプロジェクトは、ウマ娘の性格診断結果に基づいて、最も似たウマ娘キャラクターをレコメンドする Web アプリケーションです。FAISS インデックスを使用してウマ娘のデータを効率的に検索し、性格診断クイズの結果に基づいてウマ娘キャラクターを返します。

## 目次

- [ウマ娘性格診断システム (RAG ベース)](#ウマ娘性格診断システム-rag-ベース)
  - [目次](#目次)
  - [機能概要](#機能概要)
  - [インストールとセットアップ](#インストールとセットアップ)
    - [必要条件](#必要条件)
    - [クローンとセットアップ](#クローンとセットアップ)
  - [使い方](#使い方)
  - [プロジェクト構成](#プロジェクト構成)
  - [技術スタック](#技術スタック)

---

## 機能概要

- ユーザーは性格診断クイズに回答し、その結果に基づいて最も似たウマ娘キャラクターがレコメンドされます。
- FastAPI をバックエンド、React (TypeScript) をフロントエンドとして使用。
- FAISS インデックスを使用し、保存済みのウマ娘キャラクターデータを効率的に検索。
- OpenAI 埋め込みを使用した類似度検索。

---

## インストールとセットアップ

### 必要条件

- Python 3.10 以上
- Node.js 14 以上
- Docker (オプション)
- Poetry (Python パッケージ管理)

### クローンとセットアップ

1. **リポジトリをクローン**

```bash
git clone https://github.com/username/umamusume_personality.git
cd umamusume_personality
```

2. バックエンドの環境構築

```bash
cd backend
poetry install
touch .env
```

環境変数を設定

環境変数の設定については、`.env.example`を参照してください。実際の環境変数は`.env`ファイルに設定してください。

```bash
cp .env.example .env
# .envファイルを編集して、実際の値を設定してください
```

3. フロントエンドの環境構築

```bash
cd ../frontend
npm install
```

4. サーバの起動

- バックエンド

```bash
cd ../backend
poetry run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

- フロントエンド

```bash
cd ../frontend
npm start
```

## 使い方

ログイン画面にアクセスし、適切なクレデンシャルを使用してログインします。
ログイン後、性格診断クイズのページにリダイレクトされます。
質問に答えて「Submit」ボタンを押すと、クイズの結果に基づいて最も似たウマ娘キャラクターがレコメンドされます。

## プロジェクト構成

```plaintext
umamusume_personality/
│
├── backend/                      # バックエンド (FastAPI)
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py               # FastAPIのエントリーポイント
│   │   ├── models.py             # Pydanticモデル (リクエスト/レスポンス用)
│   │   ├── auth.py               # JWT認証用ロジック
│   │   ├── rag.py                # RAG (ウマ娘検索用ロジック)
│   │   └── umamusume_data.py     # ウマ娘のキャラクターデータ
│   ├── Dockerfile                # Docker設定 (バックエンド用)
│   └── requirements.txt          # Python依存関係 (FastAPI, JWT, etc.)
│
├── frontend/                     # フロントエンド (React + TypeScript)
│   ├── public/
│   │   └── index.html            # HTMLのエントリーポイント
│   ├── src/
│   │   ├── components/           # Reactコンポーネント
│   │   │   └── PersonalityQuiz.tsx   # 性格診断フォーム
│   │   │   └── LoginForm.tsx         # ログインフォーム
│   │   ├── api/                  # API通信用モジュール
│   │   │   └── authApi.ts            # 認証API通信
│   │   ├── App.tsx               # アプリ全体のコンポーネント
│   │   └── index.tsx             # Reactエントリーポイント
│   ├── Dockerfile                # Docker設定 (フロントエンド用)
│   ├── package.json              # Node.js依存関係
│   ├── tsconfig.json             # TypeScript設定
│   └── .env                      # APIエンドポイントなどの環境変数設定
│
├── docker-compose.yml            # Docker Composeファイル (フロント/バックエンドの統合)
└── README.md                     # プロジェクト概要説明
```

## 技術スタック

- バックエンド: FastAPI, Python, FAISS, OpenAI API
- フロントエンド: React, TypeScript
- データベース: FAISSインデックスを用いた類似度検索
