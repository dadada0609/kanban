# PM: Requirements Document

## Goal
現在のStreamlitベースのカンバンツールを、デザイン案「Antigravity Minimalist」に準拠した、超軽量かつ洗練されたモダンUIに刷新する。

## Core Principles
1. **Frictionless**: ユーザーやエージェントの思考を妨げる不要な境界線、強い色、重い装飾を排除。
2. **Airy**: 余白（Margin/Padding）を大胆に取り、情報が「浮いている」ような浮遊感を作る。
3. **Monochromatic**: 基本は白・オフホワイト・薄いグレー。アクセントカラーは #00A3FF (Antigravity Blue) のみ。

## Quantitative / Technical Specifications (CSS & UI)
- **Background**: 全体の背景色 (`.stApp`) を `#FAFAFA` に設定。
- **Card**:
  - `border` を無効化 (`border: none`)。
  - `border-radius: 12px` を適用。
  - `box-shadow: 0 4px 12px rgba(0,0,0,0.03)` を付与。
  - 背景色を `#FFFFFF` に設定。
- **Lane (Column)**:
  - 各カラム背景色 (`[data-testid="stColumn"]`) を `rgba(0,0,0,0.02)` に設定。
  - カラムタイトルのフォントウェイトを `600`、文字間隔(`letter-spacing`)を `0.05em` 等に設定。
- **Font**:
  - `font-family` に `Inter, system-ui, sans-serif` 等を指定。
- **Animations**:
  - カードホバー時に `transform: translateY(-2px)` で浮き上がるような `transition` を付与。
  - ホバー時にカードの左端に `4px` の `#00A3FF` (Antigravity Blue) のボーダーを表示する。

## Verification (CoVe)
- Q1: `st.container(border=True)` を使用した場合のCSSセレクタはStreamlitのDOMに適合しているか？
  - A1: はい。Streamlit 1.30+ では `[data-testid="stVerticalBlockBorderWrapper"]` 等の属性が付与されます。
- Q2: ホバー時の左端ボーダーは実装可能か？
  - A2: `::before` 疑似要素を使用し、`position: absolute; left: 0; width: 4px;` とすることでレイアウトシフトを防ぎつつ実装可能です。
- Q3: ゼロ除算等の既存の論理は維持されるか？
  - A3: 本要件はUIスタイリングに特化しており、バックエンド（Python側のロジック）は完全に維持されます。

**Verdict**: The requirements are logically sound and technically feasible using Streamlit's custom HTML/CSS injection.
