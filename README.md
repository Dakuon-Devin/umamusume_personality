# umamusume_personality

性格診断→似てるウマ娘レコメンドをRAGでやってみようって感じのPJ

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
