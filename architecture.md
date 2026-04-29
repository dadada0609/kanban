# Architect: Architecture & Implementation Strategy

## Structural Design
The Kanban application structure remains standard for a Streamlit app. The UI redesign focuses entirely on styling overrides using Streamlit's official mechanisms (`.streamlit/config.toml`) and custom CSS injected via `st.markdown(..., unsafe_allow_html=True)`.

### Component Modifications
1. **Streamlit Config (`.streamlit/config.toml`)**:
   Sets the global theme colors:
   - `primaryColor` = "#172B4D"
   - `backgroundColor` = "#F4F5F7"
   - `secondaryBackgroundColor` = "#EBECF0"
   - `textColor` = "#172B4D"
   - `font` = "sans serif"

2. **Global CSS Injection (`app.py`)**:
   Updates `inject_custom_css()` to apply the Backlog-style flat design.
   - **App Background (`.stApp`)**: Enforces `#F4F5F7` and basic text color `#172B4D`.
   - **Streamlit Columns (`div[data-testid="stColumn"]`)**: Enforces `#EBECF0`, `border-radius: 6px`, and `padding: 8px`.
   - **Column Headers (`div[data-testid="stColumn"] h3`)**: Enforces `font-size: 14px`, `font-weight: 600`, and `color: #5E6C84`.
   - **Streamlit Containers (`div[data-testid="stVerticalBlockBorderWrapper"]`)**: Enforces `#FFFFFF`, `border-radius: 4px`, `border: 1px solid #DFE1E6`, `box-shadow: 0 1px 2px rgba(9, 30, 66, 0.25)`, and `padding: 8px 10px`.
   - **Container Hover Effect**: Changes background to `#F4F5F7` and overrides any previous transform styles.

## Verification (CrossReference)
- **Target Best Practices**: Instead of overriding all elements randomly, the CSS explicitly targets `stColumn` and `stVerticalBlockBorderWrapper`. `!important` flags ensure that Streamlit's dynamically generated inline styles are overridden consistently.
- **Consistency**: The color palette adheres strictly to the provided flat design specifications without deviating.

**Verdict**: The architectural strategy reliably implements the target Backlog-style UI.
