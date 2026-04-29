# Architect: Architecture & Implementation Strategy

## Structural Design
The Kanban application structure remains standard for a Streamlit app, relying on `app.py` as the entry point and `database.py` for SQLite interactions. 
To implement the "Antigravity Minimalist" design without conflicting with Streamlit's virtual DOM or standard components, we inject global CSS via `st.markdown(..., unsafe_allow_html=True)`.

### Component Modifications
1. **Global CSS Injection**: 
   A new function `inject_custom_css()` will be added to `app.py`. It holds the precise CSS blocks needed for the redesign.
2. **Streamlit Columns (Lanes)**:
   Targeted via `div[data-testid="stColumn"]`. These represent the To Do, Doing, and Done lanes.
3. **Streamlit Containers (Cards)**:
   Targeted via `div[data-testid="stVerticalBlockBorderWrapper"]`. We rely on `st.container(border=True)` generating this wrapper, overriding its border, and giving it the floating shadow and hover effects.
4. **Typography & Layout**:
   Applied to `.stApp` and `.stMarkdown`.

## Verification (CrossReference)
- **Target Best Practices**: Instead of overriding all elements randomly, the CSS targets specific data-testids which are the Streamlit standard for column (`stColumn`) and bordered block (`stVerticalBlockBorderWrapper`).
- **Standard Library Spec**: Using `st.markdown` with `unsafe_allow_html=True` is the official Streamlit workaround for global styles.
- **Consistency**: This approach avoids breaking Streamlit's built-in widget event handlers (like click on selectboxes or buttons), while fully controlling their outer containers' appearances.

**Verdict**: The architectural strategy aligns perfectly with Streamlit constraints and effectively implements the minimalist design.
