import streamlit as st
import pandas as pd
import io

# ─── Page Config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Stock Extractor",
    page_icon="📦",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# ─── Custom CSS ───────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Nunito:wght@400;600;700;800;900&family=Space+Mono:wght@400;700&display=swap');

html, body, [class*="css"] { font-family: 'Nunito', sans-serif; }

.stApp {
    background: linear-gradient(135deg, #0f1923 0%, #1a2a3a 50%, #0d1f2d 100%);
    min-height: 100vh;
}

#MainMenu, footer, header {visibility: hidden;}
.block-container {
    padding: 1.5rem 1rem 3rem 1rem;
    max-width: 720px;
    margin: auto;
}

.app-header {
    background: linear-gradient(135deg, #f97316 0%, #fb923c 100%);
    border-radius: 20px;
    padding: 1.5rem 1.5rem 1.2rem;
    margin-bottom: 1.5rem;
    box-shadow: 0 8px 32px rgba(249,115,22,0.35);
    text-align: center;
}
.app-header h1 { font-size: 2rem; font-weight: 900; color: white; margin: 0; letter-spacing: -0.5px; }
.app-header p  { color: rgba(255,255,255,0.85); font-size: 0.95rem; margin: 0.3rem 0 0; font-weight: 600; }

.card {
    background: rgba(255,255,255,0.05);
    border: 1px solid rgba(255,255,255,0.1);
    border-radius: 16px;
    padding: 1.2rem;
    margin-bottom: 1.2rem;
    backdrop-filter: blur(10px);
}
.card-title {
    font-size: 1rem; font-weight: 800; color: #f97316;
    margin-bottom: 0.8rem; display: flex; align-items: center;
    gap: 0.4rem; text-transform: uppercase; letter-spacing: 0.5px;
}
.step-badge {
    display: inline-flex; align-items: center; justify-content: center;
    background: #f97316; color: white; font-family: 'Space Mono', monospace;
    font-size: 0.75rem; font-weight: 700; width: 22px; height: 22px;
    border-radius: 6px; flex-shrink: 0;
}

/* Raw preview table */
.raw-preview-wrap {
    overflow-x: auto;
    border-radius: 10px;
    border: 1px solid rgba(255,255,255,0.1);
    margin-bottom: 0.8rem;
}
.raw-preview-wrap table {
    border-collapse: collapse;
    width: 100%;
    font-size: 0.75rem;
    font-family: 'Space Mono', monospace;
}
.raw-preview-wrap th {
    background: rgba(249,115,22,0.25);
    color: #fb923c;
    padding: 6px 10px;
    text-align: left;
    font-weight: 700;
    white-space: nowrap;
    border-bottom: 1px solid rgba(249,115,22,0.3);
}
.raw-preview-wrap td {
    padding: 5px 10px;
    color: #e2e8f0;
    border-bottom: 1px solid rgba(255,255,255,0.05);
    white-space: nowrap;
    max-width: 160px;
    overflow: hidden;
    text-overflow: ellipsis;
}
.raw-preview-wrap tr:nth-child(even) td { background: rgba(255,255,255,0.03); }
.row-highlight td { background: rgba(249,115,22,0.12) !important; border-left: 3px solid #f97316; }
.row-num { color: #64748b !important; font-size: 0.7rem !important; }

/* Inputs */
.stFileUploader > div {
    border: 2px dashed rgba(249,115,22,0.5) !important;
    border-radius: 12px !important;
    background: rgba(249,115,22,0.06) !important;
    padding: 1rem !important;
}
.stTextInput > div > div > input {
    background: rgba(255,255,255,0.08) !important;
    border: 1.5px solid rgba(255,255,255,0.15) !important;
    border-radius: 10px !important; color: white !important;
    font-size: 1.05rem !important; padding: 0.65rem 0.9rem !important;
    font-family: 'Space Mono', monospace !important;
}
.stTextInput > div > div > input:focus {
    border-color: #f97316 !important;
    box-shadow: 0 0 0 3px rgba(249,115,22,0.2) !important;
}
.stTextInput label, .stSelectbox label, .stMultiSelect label, .stNumberInput label {
    color: #cbd5e1 !important; font-weight: 700 !important;
}
.stSelectbox > div > div {
    background: rgba(255,255,255,0.08) !important;
    border: 1.5px solid rgba(255,255,255,0.15) !important;
    border-radius: 10px !important; color: white !important;
}
.stMultiSelect > div > div {
    background: rgba(255,255,255,0.08) !important;
    border: 1.5px solid rgba(255,255,255,0.15) !important;
    border-radius: 10px !important;
}
.stNumberInput > div > div > input {
    background: rgba(255,255,255,0.08) !important;
    border: 1.5px solid rgba(255,255,255,0.15) !important;
    border-radius: 10px !important; color: white !important;
    font-size: 1.1rem !important; font-family: 'Space Mono', monospace !important;
}

/* Buttons */
.stButton > button {
    width: 100% !important;
    background: linear-gradient(135deg, #f97316, #fb923c) !important;
    color: white !important; border: none !important;
    border-radius: 12px !important; padding: 0.75rem 1rem !important;
    font-size: 1.05rem !important; font-weight: 800 !important;
    font-family: 'Nunito', sans-serif !important;
    box-shadow: 0 4px 16px rgba(249,115,22,0.3) !important;
    min-height: 52px !important; transition: all 0.2s !important;
}
.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 6px 24px rgba(249,115,22,0.45) !important;
}
.stDownloadButton > button {
    width: 100% !important;
    background: linear-gradient(135deg, #16a34a, #22c55e) !important;
    color: white !important; border: none !important;
    border-radius: 12px !important; padding: 0.75rem 1rem !important;
    font-size: 1.05rem !important; font-weight: 800 !important;
    font-family: 'Nunito', sans-serif !important;
    box-shadow: 0 4px 16px rgba(34,197,94,0.3) !important;
    min-height: 52px !important;
}
.stDownloadButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 6px 24px rgba(34,197,94,0.45) !important;
}

/* Boxes */
.info-box    { background: rgba(59,130,246,0.12); border-left: 3px solid #3b82f6; border-radius: 0 10px 10px 0; padding: 0.7rem 1rem; color: #93c5fd; font-size: 0.9rem; font-weight: 600; margin-bottom: 0.8rem; }
.warn-box    { background: rgba(234,179,8,0.12);  border-left: 3px solid #eab308; border-radius: 0 10px 10px 0; padding: 0.7rem 1rem; color: #fde047; font-size: 0.9rem; font-weight: 600; margin-bottom: 0.8rem; }
.success-box { background: rgba(34,197,94,0.12);  border-left: 3px solid #22c55e; border-radius: 0 10px 10px 0; padding: 0.7rem 1rem; color: #86efac; font-size: 0.9rem; font-weight: 600; margin-bottom: 0.8rem; }
.error-box   { background: rgba(239,68,68,0.12);  border-left: 3px solid #ef4444; border-radius: 0 10px 10px 0; padding: 0.7rem 1rem; color: #fca5a5; font-size: 0.9rem; font-weight: 600; margin-bottom: 0.8rem; }

.metric-row { display: flex; gap: 0.8rem; margin-bottom: 1rem; flex-wrap: wrap; }
.metric-box {
    flex: 1; min-width: 100px;
    background: rgba(249,115,22,0.12); border: 1px solid rgba(249,115,22,0.25);
    border-radius: 12px; padding: 0.8rem; text-align: center;
}
.metric-box .mval { font-size: 1.6rem; font-weight: 900; color: #f97316; font-family: 'Space Mono', monospace; line-height: 1.1; }
.metric-box .mlbl { font-size: 0.72rem; color: #94a3b8; font-weight: 700; text-transform: uppercase; letter-spacing: 0.5px; margin-top: 0.2rem; }

.col-pill {
    display: inline-block; background: rgba(249,115,22,0.15);
    border: 1px solid rgba(249,115,22,0.3); color: #fb923c;
    border-radius: 6px; padding: 2px 8px; font-size: 0.78rem;
    font-weight: 700; margin: 2px; font-family: 'Space Mono', monospace;
}
.divider { border: none; border-top: 1px solid rgba(255,255,255,0.08); margin: 1rem 0; }
div[role="radiogroup"] label { color: #e2e8f0 !important; font-weight: 600 !important; }
.stDataFrame { border-radius: 12px !important; overflow: hidden !important; }
</style>
""", unsafe_allow_html=True)

# ─── Constants ────────────────────────────────────────────────────────────────
WAREHOUSE_ALIASES = [
    "warehouse id","warehouse_id","warehouseid","warehouse",
    "wh id","wh_id","whid","location id","location_id","locationid",
    "location","branch","branch id","branch_id","store","store id",
    "store_id","depot","depot id","depot_id","hub","hub id","hub_id",
    "site","site id","site_id",
]

USEFUL_COLUMNS = [
    "product name","item name","description","item description",
    "sku","item code","product code","barcode","article",
    "mrp","rate","price","selling price","sp","sale price","offer price",
    "quantity","qty","stock","available qty","available stock",
    "expiry date","expiry","exp date","exp","best before",
    "batch","batch no","batch number","category","brand",
]

# ─── Helpers ──────────────────────────────────────────────────────────────────
def norm(t): return str(t).strip().lower()

def detect_wh_col(cols):
    for c in cols:
        if norm(c) in WAREHOUSE_ALIASES: return c
    for c in cols:
        for a in WAREHOUSE_ALIASES:
            if a in norm(c) or norm(c) in a: return c
    return None

def suggest_cols(cols):
    out = []
    for c in cols:
        for a in USEFUL_COLUMNS:
            if a in norm(c) or norm(c) in a:
                out.append(c); break
    return out

def df_to_excel(df):
    buf = io.BytesIO()
    with pd.ExcelWriter(buf, engine="openpyxl") as w:
        df.to_excel(w, index=False, sheet_name="Filtered Stock")
    return buf.getvalue()

def read_raw_sheet(uploaded_file, sheet_name, is_csv=False):
    """Read sheet WITHOUT headers — returns raw DataFrame, all rows as data."""
    uploaded_file.seek(0)
    if is_csv:
        return pd.read_csv(uploaded_file, header=None, dtype=str, encoding_errors="replace")
    else:
        xl = pd.ExcelFile(uploaded_file)
        return xl.parse(sheet_name, header=None, dtype=str)

def build_df_with_header(raw_df, header_row_idx):
    """Use chosen row as header, return clean DataFrame of rows below it."""
    headers = [str(v).strip() if pd.notna(v) else f"Col_{i}"
               for i, v in enumerate(raw_df.iloc[header_row_idx])]
    # Handle duplicate column names
    seen = {}
    clean_headers = []
    for h in headers:
        if h in seen:
            seen[h] += 1
            clean_headers.append(f"{h}_{seen[h]}")
        else:
            seen[h] = 0
            clean_headers.append(h)
    df = raw_df.iloc[header_row_idx + 1:].copy()
    df.columns = clean_headers
    df = df.dropna(how="all").reset_index(drop=True)
    return df

def render_raw_preview(raw_df, header_row_idx, preview_rows=12):
    """Render raw top rows as styled HTML table — highlight selected header row."""
    show = raw_df.head(preview_rows)
    rows_html = ""
    for i, (_, row) in enumerate(show.iterrows()):
        highlight = "row-highlight" if i == header_row_idx else ""
        tag = "🔖 " if i == header_row_idx else ""
        cells = f'<td class="row-num">{tag}Row {i}</td>'
        for val in row:
            val_str = "" if pd.isna(val) else str(val)[:30]
            cells += f"<td>{val_str}</td>"
        rows_html += f"<tr class='{highlight}'>{cells}</tr>"

    col_headers = '<th>#</th>' + "".join([f"<th>Col {i}</th>" for i in range(len(show.columns))])
    html = f"""
    <div class="raw-preview-wrap">
      <table>
        <thead><tr>{col_headers}</tr></thead>
        <tbody>{rows_html}</tbody>
      </table>
    </div>
    """
    return html

def get_sheet_names(uploaded_file, is_csv):
    if is_csv:
        return ["CSV Data"]
    uploaded_file.seek(0)
    return pd.ExcelFile(uploaded_file).sheet_names

# ─── App Header ───────────────────────────────────────────────────────────────
st.markdown("""
<div class="app-header">
    <h1>📦 Stock Extractor</h1>
    <p>Warehouse Stock Filter Tool — Grocery Liquidation</p>
</div>
""", unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════
# STEP 1 — Upload
# ════════════════════════════════════════════════════════════
st.markdown('<div class="card"><div class="card-title"><span class="step-badge">1</span> Upload Stock File</div></div>', unsafe_allow_html=True)

uploaded_file = st.file_uploader(
    "file", type=["xlsx","xls","xlsb","csv"],
    label_visibility="collapsed",
)

if uploaded_file is None:
    st.markdown('<div class="info-box">📲 WhatsApp ya email se mila Excel / CSV file yahan upload karo.</div>', unsafe_allow_html=True)
    st.stop()

is_csv = uploaded_file.name.lower().endswith(".csv")

# Get sheet names
try:
    sheet_names = get_sheet_names(uploaded_file, is_csv)
except Exception as e:
    st.markdown(f'<div class="error-box">❌ File read error: {e}</div>', unsafe_allow_html=True)
    st.stop()

# ════════════════════════════════════════════════════════════
# STEP 2 — Sheet Select
# ════════════════════════════════════════════════════════════
st.markdown('<div class="card"><div class="card-title"><span class="step-badge">2</span> Select Sheet</div></div>', unsafe_allow_html=True)

if len(sheet_names) == 1:
    selected_sheet = sheet_names[0]
    st.markdown(f'<div class="success-box">✅ Sheet auto-selected: <b>{selected_sheet}</b></div>', unsafe_allow_html=True)
else:
    selected_sheet = st.selectbox("Kaun sa sheet use karna hai?", options=sheet_names)

# Read raw (no header)
try:
    uploaded_file.seek(0)
    raw_df = read_raw_sheet(uploaded_file, selected_sheet, is_csv)
    raw_df = raw_df.fillna("").astype(str)
except Exception as e:
    st.markdown(f'<div class="error-box">❌ Sheet read error: {e}</div>', unsafe_allow_html=True)
    st.stop()

total_raw_rows = len(raw_df)

st.markdown(f"""
<div class="metric-row">
    <div class="metric-box"><div class="mval">{total_raw_rows:,}</div><div class="mlbl">Total Rows</div></div>
    <div class="metric-box"><div class="mval">{len(raw_df.columns)}</div><div class="mlbl">Columns</div></div>
</div>
""", unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════
# STEP 3 — Raw Preview + Header Row Select
# ════════════════════════════════════════════════════════════
st.markdown('<div class="card"><div class="card-title"><span class="step-badge">3</span> Raw Preview — Header Row Chuno</div></div>', unsafe_allow_html=True)

st.markdown('<div class="info-box">👇 Neeche file ki pehli rows dikha raha hoon. Dekho ki <b>actual column names (headers) kis row mein hain</b> — woh row number select karo.</div>', unsafe_allow_html=True)

# Row selector
max_row = min(20, total_raw_rows - 1)
header_row = st.number_input(
    "📌 Header Row Number (0 = pehli row):",
    min_value=0,
    max_value=max_row,
    value=0,
    step=1,
    help="0 matlab pehli row. Agar headers 3rd row mein hain toh 2 daalo.",
)

# Render raw preview with highlight
preview_html = render_raw_preview(raw_df, int(header_row), preview_rows=min(15, total_raw_rows))
st.markdown(preview_html, unsafe_allow_html=True)

# Show what headers will be used
selected_headers = [
    str(raw_df.iloc[int(header_row), c]).strip() or f"Col_{c}"
    for c in range(len(raw_df.columns))
]
selected_headers = [h for h in selected_headers if h and h != "nan"]

if selected_headers:
    pills = "".join([f'<span class="col-pill">{h}</span>' for h in selected_headers[:20]])
    suffix = f' <span style="color:#64748b">+{len(selected_headers)-20} more</span>' if len(selected_headers) > 20 else ""
    st.markdown(f'<div style="margin:0.5rem 0 1rem;"><b style="color:#94a3b8;font-size:0.8rem;">IS ROW KE HEADERS:</b><br>{pills}{suffix}</div>', unsafe_allow_html=True)

# Confirm button
confirm = st.button("✅ Yahi Header Row Confirm Karo")

if not confirm and "header_confirmed" not in st.session_state:
    st.markdown('<div class="warn-box">⬆️ Row number select karo aur <b>Confirm</b> karo aage badhne ke liye.</div>', unsafe_allow_html=True)
    st.stop()

if confirm:
    st.session_state["header_confirmed"] = True
    st.session_state["confirmed_header_row"] = int(header_row)

confirmed_row = st.session_state.get("confirmed_header_row", int(header_row))

# Build clean DataFrame
try:
    df_clean = build_df_with_header(raw_df, confirmed_row)
except Exception as e:
    st.markdown(f'<div class="error-box">❌ Header set karne mein error: {e}</div>', unsafe_allow_html=True)
    st.stop()

st.markdown(f'<div class="success-box">✅ Header row <b>{confirmed_row}</b> confirmed! <b>{len(df_clean):,} data rows</b> ready hain.</div>', unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════
# STEP 4 — Warehouse Search
# ════════════════════════════════════════════════════════════
st.markdown('<div class="card"><div class="card-title"><span class="step-badge">4</span> Warehouse Search</div></div>', unsafe_allow_html=True)

wh_col = detect_wh_col(df_clean.columns.tolist())

if wh_col:
    st.markdown(f'<div class="success-box">🔍 Warehouse column auto-detect hua: <b>{wh_col}</b></div>', unsafe_allow_html=True)
    unique_wh = sorted(df_clean[wh_col].dropna().unique().tolist())
    if len(unique_wh) <= 60:
        pills_html = "".join([f'<span class="col-pill">{w}</span>' for w in unique_wh])
        st.markdown(f"<div style='margin-bottom:0.8rem;'><b style='color:#94a3b8;font-size:0.8rem;'>AVAILABLE WAREHOUSES:</b><br>{pills_html}</div>", unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="info-box">📋 {len(unique_wh)} unique warehouses column <b>{wh_col}</b> mein hain.</div>', unsafe_allow_html=True)
else:
    st.markdown('<div class="warn-box">⚠️ Warehouse column auto-detect nahi hua. Manually select karo:</div>', unsafe_allow_html=True)
    wh_col = st.selectbox("Warehouse / Location column:", ["— None —"] + df_clean.columns.tolist())
    if wh_col == "— None —":
        wh_col = None

warehouse_input = st.text_input(
    "🏭 Warehouse ID daalo:",
    placeholder="e.g. WH001 ya MUMBAI ya LOC-42",
)

# Filter
df_filtered = None
if warehouse_input and wh_col:
    mask = df_clean[wh_col].astype(str).str.strip().str.lower() == warehouse_input.strip().lower()
    df_filtered = df_clean[mask].copy()
    if df_filtered.empty:
        mask2 = df_clean[wh_col].astype(str).str.contains(warehouse_input.strip(), case=False, na=False)
        df_filtered = df_clean[mask2].copy()
        if not df_filtered.empty:
            st.markdown(f'<div class="warn-box">⚠️ Exact match nahi mila. <b>{len(df_filtered)}</b> partial matches dikh rahe hain.</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="error-box">❌ "<b>{warehouse_input}</b>" ke liye koi rows nahi mili.</div>', unsafe_allow_html=True)
            df_filtered = None
    else:
        st.markdown(f'<div class="success-box">✅ <b>{len(df_filtered):,} rows</b> mili — Warehouse: <b>{warehouse_input}</b></div>', unsafe_allow_html=True)
elif warehouse_input and not wh_col:
    st.markdown('<div class="error-box">❌ Pehle warehouse column select karo.</div>', unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════
# STEP 5 — Column Selection
# ════════════════════════════════════════════════════════════
if df_filtered is not None and not df_filtered.empty:
    st.markdown('<div class="card"><div class="card-title"><span class="step-badge">5</span> Columns Chuno</div></div>', unsafe_allow_html=True)

    all_cols = df_filtered.columns.tolist()
    suggested = suggest_cols(all_cols)
    if wh_col and wh_col not in suggested:
        suggested = [wh_col] + suggested

    st.markdown(f'<div class="info-box">💡 <b>{len(suggested)}</b> useful columns auto-suggest kiye hain. Add/remove kar sakte ho.</div>', unsafe_allow_html=True)

    selected_cols = st.multiselect(
        "Download mein kaunse columns chahiye?",
        options=all_cols,
        default=[c for c in suggested if c in all_cols],
    )

    if not selected_cols:
        st.markdown('<div class="warn-box">⚠️ Kam se kam ek column select karo.</div>', unsafe_allow_html=True)
    else:
        df_output = df_filtered[selected_cols].reset_index(drop=True)

        # ── Step 6: Summary & Totals ──────────────────────────────────────────
        st.markdown('<div class="card"><div class="card-title"><span class="step-badge">6</span> Summary & Totals</div></div>', unsafe_allow_html=True)

        # Detect numeric columns from selected cols
        numeric_cols = []
        for c in selected_cols:
            try:
                converted = pd.to_numeric(df_output[c], errors="coerce")
                if converted.notna().sum() > 0:
                    numeric_cols.append(c)
            except:
                pass

        sum_cols = []
        if numeric_cols:
            st.markdown('<div class="info-box">📊 Jinke columns ka total chahiye woh select karo (sirf numeric columns dikh rahe hain):</div>', unsafe_allow_html=True)
            sum_cols = st.multiselect(
                "🔢 Total karne wale columns chuno:",
                options=numeric_cols,
                default=numeric_cols,
                key="sum_cols",
            )
        else:
            st.markdown('<div class="warn-box">⚠️ Koi numeric column nahi mila selected columns mein.</div>', unsafe_allow_html=True)

        # Show summary cards
        total_items = len(df_output)
        st.markdown(f"""
        <div class="metric-row">
            <div class="metric-box">
                <div class="mval">{total_items:,}</div>
                <div class="mlbl">📦 Total Items</div>
            </div>
            <div class="metric-box">
                <div class="mval">{len(selected_cols)}</div>
                <div class="mlbl">📋 Columns</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Per-column totals cards
        col_totals = {}
        if sum_cols:
            cards_html = '<div class="metric-row">'
            for c in sum_cols:
                total_val = pd.to_numeric(df_output[c], errors="coerce").sum()
                col_totals[c] = total_val
                # Format: if large number show in K/L
                if total_val >= 100000:
                    display_val = f"₹{total_val/100000:.1f}L"
                elif total_val >= 1000:
                    display_val = f"{total_val:,.0f}"
                else:
                    display_val = f"{total_val:,.2f}"
                short_name = c[:14] + ("…" if len(c) > 14 else "")
                cards_html += f'''
                <div class="metric-box">
                    <div class="mval" style="font-size:1.2rem">{display_val}</div>
                    <div class="mlbl">Σ {short_name}</div>
                </div>'''
            cards_html += '</div>'
            st.markdown(cards_html, unsafe_allow_html=True)

        # ── Step 7: Preview & Download ────────────────────────────────────────
        st.markdown('<div class="card"><div class="card-title"><span class="step-badge">7</span> Preview & Download</div></div>', unsafe_allow_html=True)

        preview_n = min(50, len(df_output))
        st.dataframe(df_output.head(preview_n), use_container_width=True, height=min(400, 50 + preview_n * 35))

        if len(df_output) > preview_n:
            st.markdown(f'<div class="info-box">👁 Pehle {preview_n} rows dikh rahe hain. Download mein sab {len(df_output):,} rows honge.</div>', unsafe_allow_html=True)

        st.markdown("<hr class='divider'>", unsafe_allow_html=True)

        # Build Excel with totals row at bottom
        try:
            # Make a copy to add totals row
            df_download = df_output.copy()

            if sum_cols and col_totals:
                # Build totals row
                totals_row = {}
                for c in df_download.columns:
                    if c in col_totals:
                        totals_row[c] = col_totals[c]
                    elif c == selected_cols[0]:
                        totals_row[c] = "TOTAL ▶"
                    else:
                        totals_row[c] = ""
                totals_df = pd.DataFrame([totals_row])
                df_download = pd.concat([df_download, totals_df], ignore_index=True)

            # Write to Excel with formatting
            buf = io.BytesIO()
            with pd.ExcelWriter(buf, engine="openpyxl") as writer:
                df_download.to_excel(writer, index=False, sheet_name="Filtered Stock")

                # Style the totals row
                if sum_cols and col_totals:
                    from openpyxl.styles import PatternFill, Font, Alignment
                    ws = writer.sheets["Filtered Stock"]
                    last_row = ws.max_row
                    total_cols_count = ws.max_column

                    orange_fill = PatternFill(start_color="F97316", end_color="F97316", fill_type="solid")
                    bold_white   = Font(bold=True, color="FFFFFF", size=11)

                    for col_idx in range(1, total_cols_count + 1):
                        cell = ws.cell(row=last_row, column=col_idx)
                        cell.fill   = orange_fill
                        cell.font   = bold_white
                        cell.alignment = Alignment(horizontal="center")

                    # Auto-width columns
                    for col_cells in ws.columns:
                        max_len = 0
                        col_letter = col_cells[0].column_letter
                        for cell in col_cells:
                            try:
                                max_len = max(max_len, len(str(cell.value or "")))
                            except:
                                pass
                        ws.column_dimensions[col_letter].width = min(max_len + 4, 30)

            excel_bytes = buf.getvalue()
            safe_wh = warehouse_input.strip().replace(" ","_").replace("/","-")

            st.markdown('<div class="success-box">✅ Excel ready! Last row mein <b>TOTAL row</b> (orange color) hogi.</div>', unsafe_allow_html=True)

            st.download_button(
                label=f"⬇️  Download Excel ({len(df_output):,} rows + Totals)",
                data=excel_bytes,
                file_name=f"stock_{safe_wh}_{selected_sheet}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            )
        except Exception as e:
            st.markdown(f'<div class="error-box">❌ Download error: {e}</div>', unsafe_allow_html=True)

# ─── Footer ───────────────────────────────────────────────────────────────────
st.markdown("""
<div style='text-align:center;margin-top:2rem;color:rgba(255,255,255,0.2);font-size:0.78rem;font-weight:700;'>
    STOCK EXTRACTOR v3.0 · No data stored or sent anywhere
</div>
""", unsafe_allow_html=True)
