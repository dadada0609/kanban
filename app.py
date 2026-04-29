import streamlit as st
import database
import importlib

# Streamlit Cloudのモジュールキャッシュ起因のエラーを防ぐため、常に最新のモジュールを読み込む
importlib.reload(database)

st.set_page_config(page_title="Kanban Backlog", page_icon="📌", layout="wide")

def inject_custom_css():
    css = """
    <style>
    /* Frictionless & Airy: 全体背景 */
    .stApp {
        background-color: #FAFAFA !important;
        font-family: 'Inter', system-ui, sans-serif !important;
    }

    /* レーン（カラム）: 薄いグレー背景、パディング */
    div[data-testid="stColumn"] {
        background-color: rgba(0,0,0,0.02) !important;
        border-radius: 16px !important;
        padding: 24px 16px !important;
        margin-top: 16px !important;
    }

    /* カラムタイトルのフォント調整 */
    div[data-testid="stColumn"] h3 {
        font-weight: 600 !important;
        letter-spacing: 0.05em !important;
        color: #333333 !important;
        margin-bottom: 16px !important;
    }

    /* カード（st.container(border=True)のラッパー）: ボーダーなし、白背景、薄い影 */
    div[data-testid="stVerticalBlockBorderWrapper"] {
        border: none !important;
        border-radius: 12px !important;
        box-shadow: 0 4px 12px rgba(0,0,0,0.03) !important;
        background-color: #FFFFFF !important;
        padding: 8px !important;
        transition: all 0.3s ease !important;
        position: relative !important;
        overflow: hidden !important;
        margin-bottom: 16px !important;
    }

    /* カードのホバーアニメーション（浮遊感とAntigravity Blue） */
    div[data-testid="stVerticalBlockBorderWrapper"]:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 24px rgba(0,0,0,0.05) !important;
    }

    /* カード左端のAntigravity Blue線（ホバー時） */
    div[data-testid="stVerticalBlockBorderWrapper"]::before {
        content: '' !important;
        position: absolute !important;
        left: 0 !important;
        top: 0 !important;
        bottom: 0 !important;
        width: 4px !important;
        background-color: transparent !important;
        transition: background-color 0.3s ease !important;
        z-index: 10 !important;
    }

    div[data-testid="stVerticalBlockBorderWrapper"]:hover::before {
        background-color: #00A3FF !important;
    }

    /* ヘッダーの非表示化などの不要な線の削除 */
    header[data-testid="stHeader"] {
        background: transparent !important;
    }
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

# ページ設定の直後にCSSを注入
inject_custom_css()

def main():
    st.title("📌 Kanban Backlog Management")

    # 初期化
    database.init_db()

    # ===============================
    # 進捗の定量化 (Visual Metrics)
    # ===============================
    status_counts = database.get_status_counts()
    total_tasks = sum(status_counts.values())
    
    # [QA] ゼロ除算の回避
    progress_rate = (status_counts['Done'] / total_tasks * 100) if total_tasks > 0 else 0.0

    st.header("📊 進行状況")
    col_metric1, col_metric2, col_metric3, col_metric4 = st.columns(4)
    col_metric1.metric("総タスク数", total_tasks)
    col_metric2.metric("To Do", status_counts['To Do'])
    col_metric3.metric("Doing", status_counts['Doing'])
    col_metric4.metric("Done", status_counts['Done'])

    st.progress(progress_rate / 100.0)
    st.write(f"**進捗率 (Doneの割合):** {progress_rate:.1f}%")

    st.markdown("---")

    # ===============================
    # サイドバー：タスク追加 & エクスポート
    # ===============================
    with st.sidebar:
        st.header("➕ 新規タスク追加")
        with st.form("add_task_form", clear_on_submit=True):
            title = st.text_input("タイトル")
            priority = st.selectbox("優先度", ["高", "中", "低"])
            due_date = st.date_input("期限", value=None)
            description = st.text_area("詳細メモ")
            assignee = st.text_input("担当者")
            submitted = st.form_submit_button("追加")
            
            if submitted:
                if title.strip() == "":
                    st.error("タイトルを入力してください。")
                else:
                    due_date_str = str(due_date) if due_date else ""
                    database.add_task(title.strip(), priority, assignee.strip(), due_date_str, description.strip())
                    st.success("タスクを追加しました！")
                    st.rerun()

        st.markdown("---")
        st.header("📥 データエクスポート")
        # [QA] 文字化け防止のためUTF-8-SIG形式でエンコードされたデータを利用
        csv_data = database.get_tasks_csv()
        st.download_button(
            label="全タスクをCSVでダウンロード",
            data=csv_data,
            file_name="tasks.csv",
            mime="text/csv",
            help="Excel等での文字化けを防ぐため、UTF-8-SIG形式でダウンロードされます。"
        )

    # ===============================
    # メイン画面：カンバンボード
    # ===============================
    st.header("📋 タスクボード")
    cols = st.columns(3)
    statuses = ["To Do", "Doing", "Done"]

    tasks = database.get_tasks()

    for col, status in zip(cols, statuses):
        with col:
            st.subheader(f"{status} ({status_counts[status]})")
            
            # ステータスごとのタスクを抽出
            status_tasks = [t for t in tasks if t['status'] == status]
            
            for task in status_tasks:
                with st.container(border=True):
                    st.markdown(f"**{task['title']}**")
                    
                    color_map = {"高": "red", "中": "orange", "低": "blue"}
                    p_color = color_map.get(task['priority'], "gray")
                    st.markdown(f"優先度: <span style='color:{p_color}; font-weight:bold;'>{task['priority']}</span> | 担当者: {task['assignee']}", unsafe_allow_html=True)
                    
                    if task.get('due_date'):
                        st.write(f"📅 期限: {task['due_date']}")
                    if task.get('description'):
                        st.caption(f"📝 {task['description']}")
                    
                    # ステータス変更
                    new_status = st.selectbox(
                        "ステータス",
                        options=statuses,
                        index=statuses.index(task['status']),
                        key=f"status_{task['id']}"
                    )
                    
                    if new_status != task['status']:
                        database.update_task_status(task['id'], new_status)
                        st.rerun()

                    # 削除ボタン
                    if st.button("削除", key=f"delete_{task['id']}", type="primary"):
                        database.delete_task(task['id'])
                        st.rerun()

if __name__ == "__main__":
    main()
