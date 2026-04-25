import streamlit as st
import database

st.set_page_config(page_title="Kanban Backlog", page_icon="📌", layout="wide")

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
            assignee = st.text_input("担当者")
            submitted = st.form_submit_button("追加")
            
            if submitted:
                if title.strip() == "":
                    st.error("タイトルを入力してください。")
                else:
                    database.add_task(title.strip(), priority, assignee.strip())
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
                    st.write(f"優先度: {task['priority']} | 担当者: {task['assignee']}")
                    
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
