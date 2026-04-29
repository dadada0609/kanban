import streamlit as st
import database
import importlib
import datetime

# モジュールキャッシュクリア
importlib.reload(database)

# 1. ページ設定（Backlog風のワイドレイアウト）
st.set_page_config(page_title="Backlog | Kanban", page_icon="📋", layout="wide")

def inject_backlog_css():
    """
    Backlogの質感を再現するための超強力なCSS注入
    """
    timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    css = f"""
    <style>
    /* Cache Buster: {timestamp} */
    
    /* 全体の背景色をBacklog風の薄グレーに強制 */
    .stApp, [data-testid="stAppViewContainer"] {{
        background-color: #F4F5F7 !important;
    }}

    /* ヘッダー（タイトル部分）の装飾 */
    .main-title {{
        font-size: 24px !important;
        font-weight: 700 !important;
        color: #172B4D !important;
        border-bottom: 2px solid #0078D4;
        padding-bottom: 10px;
        margin-bottom: 25px;
    }}

    /* カンバンカラム（レーン）の装飾 */
    [data-testid="stColumn"] {{
        background-color: #EBECF0 !important;
        border-radius: 8px !important;
        padding: 15px !important;
        min-height: 80vh;
    }}

    /* タスクカード（container）の装飾 */
    [data-testid="stVerticalBlockBorderWrapper"] {{
        background-color: #FFFFFF !important;
        border: 1px solid #DFE1E6 !important;
        border-radius: 4px !important;
        box-shadow: 0 1px 2px rgba(9, 30, 66, 0.2) !important;
        margin-bottom: 10px !important;
        padding: 2px !important;
    }}

    /* サイドバーの簡素化 */
    section[data-testid="stSidebar"] {{
        background-color: #2D3E50 !important;
    }}
    section[data-testid="stSidebar"] * {{
        color: #FFFFFF !important;
    }}

    /* デバッグ用：バージョン情報のフローティング表示 */
    .version-tag {{
        position: fixed;
        top: 10px;
        right: 70px;
        background: #0078D4;
        color: white;
        padding: 2px 10px;
        border-radius: 20px;
        font-size: 10px;
        z-index: 9999;
    }}
    </style>
    <div class="version-tag">System Ver: 2.5 (Backlog Mode Active)</div>
    """
    st.markdown(css, unsafe_allow_html=True)

def main():
    inject_backlog_css()
    
    # 生存確認用のタイトル
    st.markdown('<h1 class="main-title">📋 プロジェクトボード</h1>', unsafe_allow_html=True)

    database.init_db()

    # メトリクス（進行状況）
    status_counts = database.get_status_counts()
    total_tasks = sum(status_counts.values())
    
    cols_m = st.columns(4)
    cols_m[0].metric("未完了", status_counts['To Do'])
    cols_m[1].metric("処理中", status_counts['Doing'])
    cols_m[2].metric("完了", status_counts['Done'])
    if total_tasks > 0:
        progress = status_counts['Done'] / total_tasks
        st.progress(progress)

    # メインボード
    st.markdown("---")
    cols = st.columns(3)
    statuses = ["To Do", "Doing", "Done"]
    tasks = database.get_tasks()

    for col, status in zip(cols, statuses):
        with col:
            # カラムヘッダー
            st.markdown(f"### {status} `{status_counts[status]}`")
            
            status_tasks = [t for t in tasks if t['status'] == status]
            for task in status_tasks:
                # カード本体
                with st.container(border=True):
                    # タイトルとID風表示
                    st.markdown(f"**{task['title']}**")
                    
                    # 担当者と優先度（Backlog風ラベル）
                    p_colors = {"高": "#F14C4C", "中": "#F5A623", "低": "#0078D4"}
                    p_color = p_colors.get(task['priority'], "#5E6C84")
                    
                    st.markdown(f"""
                        <div style="font-size: 12px; color: #5E6C84;">
                            <span style="background: {p_color}; color: white; padding: 1px 6px; border-radius: 3px;">{task['priority']}</span>
                            &nbsp;👤 {task['assignee']}
                        </div>
                    """, unsafe_allow_html=True)
                    
                    if task.get('due_date'):
                        st.caption(f"📅 {task['due_date']}")
                    
                    # 操作系
                    with st.expander("操作"):
                        new_status = st.selectbox(
                            "移動:", statuses, 
                            index=statuses.index(task['status']),
                            key=f"status_{task['id']}"
                        )
                        if new_status != task['status']:
                            database.update_task_status(task['id'], new_status)
                            st.rerun()
                        
                        if st.button("削除", key=f"del_{task['id']}", type="secondary"):
                            database.delete_task(task['id'])
                            st.rerun()

    # サイドバー
    with st.sidebar:
        st.title("Settings")
        with st.form("add"):
            st.subheader("新規課題")
            t = st.text_input("件名")
            p = st.selectbox("優先度", ["高", "中", "低"])
            a = st.text_input("担当者")
            d = st.date_input("期限")
            desc = st.text_area("内容")
            if st.form_submit_button("追加"):
                if t:
                    database.add_task(t, p, a, str(d), desc)
                    st.rerun()

if __name__ == "__main__":
    main()
