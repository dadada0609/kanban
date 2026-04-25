# Architecture Document: Kanban-style Backlog Management Tool

## 1. ディレクトリ構造
```text
/
├── app.py           # Streamlitアプリケーションのエントリポイント (UI/UX)
├── database.py      # SQLite DB接続、初期化、CRUD操作のロジック
├── requirements.txt # 依存パッケージ一覧
└── tasks.db         # 実行時に生成・利用されるSQLiteデータベースファイル
```

## 2. データモデル (SQLite Schema)
**Table: `tasks`**
- `id` (INTEGER PRIMARY KEY AUTOINCREMENT)
- `title` (TEXT NOT NULL)
- `status` (TEXT NOT NULL) - 許容値: 'To Do', 'Doing', 'Done'
- `priority` (TEXT NOT NULL) - 許容値: '高', '中', '低'
- `assignee` (TEXT NOT NULL)

## 3. モジュール・インターフェース仕様
### `database.py`
- `init_db() -> None`: データベースファイルと `tasks` テーブルが存在しない場合に作成する。
- `get_tasks() -> list[dict]`: 全タスクを辞書のリスト形式で取得する。
- `add_task(title: str, priority: str, assignee: str) -> None`: 新規タスクをDBに挿入する。
- `update_task_status(task_id: int, new_status: str) -> None`: 指定タスクのステータスを更新する。
- `delete_task(task_id: int) -> None`: 指定タスクをDBから削除する。
- `get_status_counts() -> dict`: 各ステータスのタスク数を集計して返す。
- `get_tasks_csv() -> bytes`: 全タスクをCSV形式（UTF-8-SIGエンコーディング）に変換して返す。

### `app.py`
- Streamlitの再実行モデルに基づくトップダウンのフロー。
- 初期化フェーズ: スクリプト先頭で `database.init_db()` を実行。
- 進捗の定量化: `database.get_status_counts()` で取得したデータを元に、`st.metric` および `st.progress` を用いてタスクの分布と進捗率を描画。
- サイドバーUI: 
  - タスク追加用の入力フォームを配置し、`database.add_task` を呼び出す。
  - データエクスポート用に `database.get_tasks_csv()` を呼び出し、`st.download_button` でCSVダウンロード機能を提供する。
- メインUI: `st.columns(3)` を用いて「To Do」「Doing」「Done」のカラムを作成。
- インタラクション: タスクカード内にステータス変更と削除ボタンを配置。変更時は `database.update_task_status` / `database.delete_task` 後に `st.rerun()`。

## 4. CrossReference検証結果
- **Python標準ライブラリ**: `sqlite3` および `csv` を用いることで、サードパーティライブラリに依存せず軽量かつ安全にデータ永続化とエクスポートを実現。
- **Streamlitのベストプラクティス**: `st.rerun()` とウィジェットの状態管理が正しく設計されている。ゼロ除算エラーの回避も明示的に行われている。
