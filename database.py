import sqlite3
import csv
from io import StringIO

DB_FILE = 'tasks.db'

def init_db():
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                status TEXT NOT NULL,
                priority TEXT NOT NULL,
                assignee TEXT NOT NULL,
                due_date TEXT,
                description TEXT
            )
        ''')
        
        # 既存テーブルへのカラム追加（エラー無視で対応）
        try:
            cursor.execute("ALTER TABLE tasks ADD COLUMN due_date TEXT")
        except sqlite3.OperationalError:
            pass
            
        try:
            cursor.execute("ALTER TABLE tasks ADD COLUMN description TEXT")
        except sqlite3.OperationalError:
            pass
            
        conn.commit()

def get_tasks() -> list[dict]:
    with sqlite3.connect(DB_FILE) as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM tasks")
        return [dict(row) for row in cursor.fetchall()]

def add_task(title: str, priority: str, assignee: str, due_date: str = None, description: str = None):
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO tasks (title, status, priority, assignee, due_date, description)
            VALUES (?, 'To Do', ?, ?, ?, ?)
        ''', (title, priority, assignee, due_date, description))
        conn.commit()

def update_task_status(task_id: int, new_status: str):
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE tasks SET status = ? WHERE id = ?
        ''', (new_status, task_id))
        conn.commit()

def delete_task(task_id: int):
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            DELETE FROM tasks WHERE id = ?
        ''', (task_id,))
        conn.commit()

def get_status_counts() -> dict:
    """ステータスごとのタスク数を集計するクエリ"""
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            SELECT status, COUNT(*) as count FROM tasks GROUP BY status
        ''')
        counts = {'To Do': 0, 'Doing': 0, 'Done': 0}
        for row in cursor.fetchall():
            counts[row[0]] = row[1]
        return counts

def get_tasks_csv() -> bytes:
    """CSVエクスポート用に全タスクをUTF-8-SIG形式で取得する"""
    tasks = get_tasks()
    output = StringIO()
    if not tasks:
        writer = csv.writer(output)
        writer.writerow(['id', 'title', 'status', 'priority', 'assignee', 'due_date', 'description'])
    else:
        writer = csv.DictWriter(output, fieldnames=tasks[0].keys())
        writer.writeheader()
        writer.writerows(tasks)
    # Excel等での文字化けを防ぐために utf-8-sig でエンコード
    return output.getvalue().encode('utf-8-sig')
