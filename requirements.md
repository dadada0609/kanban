# PM: Requirements Document

## Goal
Streamlit製カンバンツールのUIを、日本の代表的なプロジェクト管理ツール（Backlog風）の、視認性が高く実用的なフラットデザインに全面的に刷新する。

## Specifications
1. **カラーパレット (Theme)**
   - 全体背景: `#F4F5F7`
   - カラム背景: `#EBECF0`
   - タスクカード背景: `#FFFFFF`
   - テキスト基本色: `#172B4D`
2. **レーン（カラム）**
   - 背景色: `#EBECF0`
   - 形状: `border-radius: 6px;`
   - 余白: 内側 `8px`
   - タイトル: `font-size: 14px; font-weight: 600; color: #5E6C84;`
3. **タスクカード**
   - 背景と形状: 背景 `#FFFFFF`, `border-radius: 4px;`
   - 境界線: `border: 1px solid #DFE1E6;`
   - 影: `box-shadow: 0 1px 2px rgba(9, 30, 66, 0.25);`
   - ホバー時: `background-color: #F4F5F7;`
   - 余白: `padding: 8px 10px;`

## Verification (CoVe)
- Q1: `padding: 8px 10px` などの指定はStreamlit内で他の要素との競合を引き起こさないか？
  - A1: ターゲットを `div[data-testid="stVerticalBlockBorderWrapper"]` に絞ることで、他の内部ウィジェットを壊すことなくコンテナの余白を制御可能です。
- Q2: `border: 1px solid #DFE1E6` は `st.container(border=True)` のデフォルトボーダーを上書きできるか？
  - A2: `!important` を付与することで確実に上書き可能です。
- Q3: `.streamlit/config.toml` の変更とCSSの変更に競合はないか？
  - A3: `config.toml` がベースのスタイルを提供し、CSSが詳細な構造（レーンやカード）のスタイルを補完・上書きするため、相互補完的に機能します。

**Verdict**: The requirements are logically sound and technically feasible.
