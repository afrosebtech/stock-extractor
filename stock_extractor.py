import streamlit as st
import pandas as pd
import io
import os

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

/* Reset & Base */
html, body, [class*="css"] {
    font-family: 'Nunito', sans-serif;
}

/* Background */
.stApp {
    background: linear-gradient(135deg, #0f1923 0%, #1a2a3a 50%, #0d1f2d 100%);
    min-height: 100vh;
}

/* Hide default Streamlit elements */
#MainMenu, footer, header {visibility: hidden;}
.block-container {
    padding: 1.5rem 1rem 3rem 1rem;
    max-width: 720px;
    margin: auto;
}

/* ── Header ── */
.app-header {
    background: linear-gradient(135deg, #f97316 0%, #fb923c 100%);
    border-radius: 20px;
    padding: 1.5rem 1.5rem 1.2rem;
    margin-bottom: 1.5rem;
    box-shadow: 0 8px 32px rgba(249,115,22,0.35);
    text-align: center;
}
.app-header h1 {
    font-size: 2rem;
    font-weight: 900;
    color: white;
    margin: 0;
    letter-spacing: -0.5px;
}
.app-header p {
    color: rgba(255,255,255,0.85);
    font-size: 0.95rem;
    margin: 0.3rem 0 0;
    font-weight: 600;
}

/* ── Cards ── */
.card {
    background: rgba(255,255,255,0.05);
    border: 1px solid rgba(255,255,255,0.1);
    border-radius: 16px;
    padding: 1.2rem 1.2rem;
    margin-bottom: 1.2rem;
    backdrop-filter: blur(10px);
}
.card-title {
    font-size: 1rem;
    font-weight: 800;
    color: #f97316;
    margin-bottom: 0.8rem;
    display: flex;
    align-items: center;
    gap: 0.4rem;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}

/* ── Step badges ── */
.step-badge {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    background: #f97316;
    color: white;
    font-family: 'Space Mono', monospace;
    font-size: 0.75rem;
    font-weight: 700;
    width: 22px;
    height: 22px;
    border-radius: 6px;
    flex-shrink: 0;
}

/* ── Streamlit widget overrides ── */
.stFileUploader > div {
    border: 2px dashed rgba(249,115,22,0.5) !important;
    border-radius: 12px !important;
    background: rgba(249,115,22,0.06) !important;
    padding: 1rem !important;
}
.stFileUploader label {
    color: #fb923c !important;
    font-weight: 700 !important;
}

/* Text inputs */
.stTextInput > div > div > input {
    background: rgba(255,255,255,0.08) !important;
    border: 1.5px solid rgba(255,255,255,0.15) !important;
    border-radius: 10px !important;
    color: white !important;
    font-size: 1.05rem !important;
    padding: 0.65rem 0.9rem !important;
    font-family: 'Space Mono', monospace !important;
}
.stTextInput > div > div > input:focus {
    border-color: #f97316 !important;
    box-shadow: 0 0 0 3px rgba(249,115,22,0.2) !important;
}
.stTextInput label {
    color: #cbd5e1 !important;
    font-weight: 700 !important;
}

/* Select boxes */
.stSelectbox > div > div {
    background: rgba(255,255,255,0.08) !important;
    border: 1.5px solid rgba(255,255,255,0.15) !important;
    border-radius: 10px !important;
    color: white !important;
}
.stSelectbox label, .stMultiSelect label {
    color: #cbd5e1 !important;
    font-weight: 700 !important;
}

/* Multiselect */
.stMultiSelect > div > div {
    background: rgba(255,255,255,0.08) !important;
    border: 1.5px solid rgba(255,255,255,0.15) !important;
    border-radius: 10px !important;
}

/* Buttons */
.stButton > button {
    width: 100% !important;
    background: linear-gradient(135deg, #f97316, #fb923c) !important;
    color: white !important;
    border: none !important;
    border-radius: 12px !important;
    padding: 0.75rem 1rem !important;
    font-size: 1.05rem !important;
    font-weight: 800 !important;
    font-family: 'Nunito', sans-serif !important;
    cursor: pointer !important;
    transition: all 0.2s !important;
    box-shadow: 0 4px 16px rgba(249,115,22,0.3) !important;
    letter-spacing: 0.3px !important;
    min-height: 52px !important;
}
.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 6px 24px rgba(249,115,22,0.45) !important;
    opacity: 0.95 !important;
}
.stButton > button:active {
    transform: translateY(0px) !important;
}

/* Download button */
.stDownloadButton > button {
    width: 100% !important;
    background: linear-gradient(135deg, #16a34a, #22c55e) !important;
    color: white !important;
    border: none !important;
    border-radius: 12px !important;
    padding: 0.75rem 1rem !important;
    font-size: 1.05rem !important;
    font-weight: 800 !important;
    font-family: 'Nunito', sans-serif !important;
    cursor: pointer !important;
    box-shadow: 0 4px 16px rgba(34,197,94,0.3) !important;
    min-height: 52px !important;
}
.stDownloadButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 6px 24px rgba(34,197,94,0.45) !important;
    opacity: 0.95 !important;
}

/* Dataframe */
.stDataFrame {
    border-radius: 12px !important;
    overflow: hidden !important;
}

/* Metrics */
.metric-row {
    display: flex;
    gap: 0.8rem;
    margin-bottom: 1rem;
    flex-wrap: wrap;
}
.metric-box {
    flex: 1;
    min-width: 100px;
    background: rgba(249,115,22,0.12);
    border: 1px solid rgba(249,115,22,0.25);
    border-radius: 12px;
    padding: 0.8rem;
    text-align: center;
}
.metric-box .mval {
    font-size: 1.6rem;
    font-weight: 900;
    color: #f97316;
    font-family: 'Space Mono', monospace;
    line-height: 1.1;
}
.metric-box .mlbl {
    font-size: 0.72rem;
    color: #94a3b8;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    margin-top: 0.2rem;
}

/* Info / warning boxes */
.info-box {
    background: rgba(59,130,246,0.12);
    border-left: 3px solid #3b82f6;
    border-radius: 0 10px 10px 0;
    padding: 0.7rem 1rem;
    color: #93c5fd;
    font-size: 0.9rem;
    font-weight: 600;
    margin-bottom: 0.8rem;
}
.warn-box {
    background: rgba(234,179,8,0.12);
    border-left: 3px solid #eab308;
    border-radius: 0 10px 10px 0;
    padding: 0.7rem 1rem;
    color: #fde047;
    font-size: 0.9rem;
    font-weight: 600;
    margin-bottom: 0.8rem;
}
.success-box {
    background: rgba(34,197,94,0.12);
    border-left: 3px solid #22c55e;
    border-radius: 0 10px 10px 0;
    padding: 0.7rem 1rem;
    color: #86efac;
    font-size: 0.9rem;
    font-weight: 600;
    margin-bottom: 0.8rem;
}
.error-box {
    background: rgba(239,68,68,0.12);
    border-left: 3px solid #ef4444;
    border-radius: 0 10px 10px 0;
    padding: 0.7rem 1rem;
    color: #fca5a5;
    font-size: 0.9rem;
    font-weight: 600;
    margin-bottom: 0.8rem;
}

/* Column tag pills */
.col-pill {
    display: inline-block;
    background: rgba(249,115,22,0.15);
    border: 1px solid rgba(249,115,22,0.3);
    color: #fb923c;
    border-radius: 6px;
    padding: 2px 8px;
    font-size: 0.78rem;
    font-weight: 700;
    margin: 2px;
    font-family: 'Space Mono', monospace;
}

/* Divider */
.divider {
    border: none;
    border-top: 1px solid rgba(255,255,255,0.08);
    margin: 1rem 0;
}

/* Stacked radio (sheet select hack) */
div[role="radiogroup"] label {
    color: #e2e8f0 !important;
    font-weight: 600 !important;
}
</style>
""", unsafe_allow_html=True)

# ─── Constants ────────────────────────────────────────────────────────────────
WAREHOUSE_COLUMN_ALIASES = [
    "warehouse id", "warehouse_id", "warehouseid",
    "warehouse", "wh id", "wh_id", "whid",
    "location id", "location_id", "locationid",
    "location", "branch", "branch id", "branch_id",
    "store", "store id", "store_id",
    "depot", "depot id", "depot_id",
    "hub", "hub id", "hub_id",
    "site", "site id", "site_id",
]

COMMON_USEFUL_COLUMNS = [
    "product name", "item name", "description", "item description",
    "sku", "item code", "product code", "barcode", "article",
    "mrp", "rate", "price", "selling price", "sp", "sale price", "offer price",
    "quantity", "qty", "stock", "available qty", "available stock",
    "expiry date", "expiry", "exp date", "exp", "best before",
    "batch", "batch no", "batch number",
    "category", "brand",
]

# ─── Helper Functions ─────────────────────────────────────────────────────────

def normalize(text: str) -> str:
    """Lowercase + strip for comparison."""
    return str(text).strip().lower()


def detect_warehouse_column(columns: list[str]) -> str | None:
    """Return the column name that best matches a warehouse identifier."""
    for col in columns:
        if normalize(col) in WAREHOUSE_COLUMN_ALIASES:
            return col
    # Fuzzy: check if any alias is *contained* in the column name
    for col in columns:
        norm = normalize(col)
        for alias in WAREHOUSE_COLUMN_ALIASES:
            if alias in norm or norm in alias:
                return col
    return None


def read_file(uploaded_file) -> dict[str, pd.DataFrame] | None:
    """Read uploaded file into a dict of {sheet_name: DataFrame}."""
    name = uploaded_file.name.lower()
    try:
        if name.endswith(".csv"):
            df = pd.read_csv(uploaded_file, dtype=str, encoding_errors="replace")
            return {"CSV Data": df}
        elif name.endswith(".xlsb"):
            try:
                import pyxlsb
                sheets = {}
                with pyxlsb.open_workbook(uploaded_file) as wb:
                    for sname in wb.sheets:
                        with wb.get_sheet(sname) as sheet:
                            rows = []
                            for row in sheet.rows():
                                rows.append([item.v for item in row])
                        if rows:
                            df = pd.DataFrame(rows[1:], columns=rows[0])
                            sheets[sname] = df.astype(str)
                return sheets
            except ImportError:
                st.markdown('<div class="error-box">⚠️ <b>pyxlsb</b> library not installed. Run: <code>pip install pyxlsb</code></div>', unsafe_allow_html=True)
                return None
        else:  # .xlsx / .xls
            xl = pd.ExcelFile(uploaded_file)
            sheets = {}
            for sname in xl.sheet_names:
                df = xl.parse(sname, dtype=str)
                sheets[sname] = df
            return sheets
    except Exception as e:
        st.markdown(f'<div class="error-box">❌ File read error: {e}</div>', unsafe_allow_html=True)
        return None


def suggest_useful_columns(columns: list[str]) -> list[str]:
    """Return columns that match common useful field names."""
    suggested = []
    for col in columns:
        norm = normalize(col)
        for alias in COMMON_USEFUL_COLUMNS:
            if alias in norm or norm in alias:
                suggested.append(col)
                break
    return suggested


def df_to_excel_bytes(df: pd.DataFrame) -> bytes:
    """Convert dataframe to Excel bytes for download."""
    buf = io.BytesIO()
    with pd.ExcelWriter(buf, engine="openpyxl") as writer:
        df.to_excel(writer, index=False, sheet_name="Filtered Stock")
    return buf.getvalue()

# ─── App Header ───────────────────────────────────────────────────────────────
st.markdown("""
<div class="app-header">
    <h1>📦 Stock Extractor</h1>
    <p>Warehouse Stock Filter Tool — Grocery Liquidation</p>
</div>
""", unsafe_allow_html=True)

# ─── Step 1: File Upload ───────────────────────────────────────────────────────
st.markdown("""
<div class="card">
    <div class="card-title"><span class="step-badge">1</span> Upload Stock File</div>
</div>
""", unsafe_allow_html=True)

uploaded_file = st.file_uploader(
    "Choose your Excel or CSV file",
    type=["xlsx", "xls", "xlsb", "csv"],
    help="Supports .xlsx, .xls, .xlsb and .csv files from WhatsApp or email",
    label_visibility="collapsed",
)

if uploaded_file is None:
    st.markdown('<div class="info-box">📲 Upload a stock file received from WhatsApp, email, or any source. Supports Excel and CSV formats.</div>', unsafe_allow_html=True)
    st.stop()

# ─── Read File ─────────────────────────────────────────────────────────────────
with st.spinner("Reading file...."):
    sheets_dict = read_file(uploaded_file)

if not sheets_dict:
    st.stop()

file_info_cols = st.columns(3)
with file_info_cols[0]:
    st.markdown(f'<div class="metric-box"><div class="mval">{len(sheets_dict)}</div><div class="mlbl">Sheets</div></div>', unsafe_allow_html=True)

# ─── Step 2: Sheet Selection ───────────────────────────────────────────────────
st.markdown("""
<div class="card">
    <div class="card-title"><span class="step-badge">2</span> Select Sheet</div>
</div>
""", unsafe_allow_html=True)

sheet_names = list(sheets_dict.keys())
if len(sheet_names) == 1:
    selected_sheet = sheet_names[0]
    st.markdown(f'<div class="success-box">✅ Auto-selected sheet: <b>{selected_sheet}</b></div>', unsafe_allow_html=True)
else:
    selected_sheet = st.selectbox(
        "Multiple sheets found — choose one:",
        options=sheet_names,
        help="Select the sheet that contains your stock data",
    )

df_raw = sheets_dict[selected_sheet].copy()

# Drop completely empty rows/cols
df_raw = df_raw.dropna(how="all").reset_index(drop=True)
df_raw.columns = [str(c).strip() for c in df_raw.columns]

total_rows = len(df_raw)
total_cols = len(df_raw.columns)

st.markdown(f"""
<div class="metric-row">
    <div class="metric-box"><div class="mval">{total_rows:,}</div><div class="mlbl">Total Rows</div></div>
    <div class="metric-box"><div class="mval">{total_cols}</div><div class="mlbl">Columns</div></div>
</div>
""", unsafe_allow_html=True)

# ─── Step 3: Warehouse Search ──────────────────────────────────────────────────
st.markdown("""
<div class="card">
    <div class="card-title"><span class="step-badge">3</span> Search Warehouse</div>
</div>
""", unsafe_allow_html=True)

wh_col = detect_warehouse_column(df_raw.columns.tolist())

if wh_col:
    st.markdown(f'<div class="success-box">🔍 Warehouse column auto-detected: <b>{wh_col}</b></div>', unsafe_allow_html=True)
    unique_wh = sorted(df_raw[wh_col].dropna().unique().tolist())

    # Show available warehouse IDs
    if len(unique_wh) <= 50:
        pills_html = "".join([f'<span class="col-pill">{w}</span>' for w in unique_wh])
        st.markdown(f"<div style='margin-bottom:0.8rem;'><b style='color:#94a3b8;font-size:0.8rem;'>Available Warehouses:</b><br>{pills_html}</div>", unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="info-box">📋 {len(unique_wh)} unique warehouse IDs found in column <b>{wh_col}</b></div>', unsafe_allow_html=True)
else:
    st.markdown('<div class="warn-box">⚠️ Could not auto-detect warehouse column. Please select it manually below.</div>', unsafe_allow_html=True)
    wh_col = st.selectbox(
        "Select the Warehouse / Location column:",
        options=["— None —"] + df_raw.columns.tolist(),
    )
    if wh_col == "— None —":
        wh_col = None

warehouse_input = st.text_input(
    "🏭 Enter Warehouse ID to filter:",
    placeholder="e.g.  WH001  or  MUMBAI  or  LOC-42",
    help="Type the warehouse name or ID exactly as shown above",
)

# ─── Apply Filter ──────────────────────────────────────────────────────────────
df_filtered = None
if warehouse_input and wh_col:
    mask = df_raw[wh_col].astype(str).str.strip().str.lower() == warehouse_input.strip().lower()
    df_filtered = df_raw[mask].copy()

    if df_filtered.empty:
        # Try partial match
        mask_partial = df_raw[wh_col].astype(str).str.contains(warehouse_input.strip(), case=False, na=False)
        df_partial = df_raw[mask_partial].copy()

        if not df_partial.empty:
            st.markdown(f'<div class="warn-box">⚠️ No exact match for "<b>{warehouse_input}</b>". Showing {len(df_partial)} partial matches instead.</div>', unsafe_allow_html=True)
            df_filtered = df_partial
        else:
            st.markdown(f'<div class="error-box">❌ No rows found for warehouse "<b>{warehouse_input}</b>". Please check the ID above.</div>', unsafe_allow_html=True)
            df_filtered = None
    else:
        st.markdown(f'<div class="success-box">✅ Found <b>{len(df_filtered):,} rows</b> for warehouse: <b>{warehouse_input}</b></div>', unsafe_allow_html=True)

elif warehouse_input and not wh_col:
    st.markdown('<div class="error-box">❌ Please select a warehouse column first.</div>', unsafe_allow_html=True)

# ─── Step 4: Column Selection ──────────────────────────────────────────────────
if df_filtered is not None and not df_filtered.empty:
    st.markdown("""
    <div class="card">
        <div class="card-title"><span class="step-badge">4</span> Choose Columns to Keep</div>
    </div>
    """, unsafe_allow_html=True)

    all_cols = df_filtered.columns.tolist()
    suggested = suggest_useful_columns(all_cols)

    # Always include warehouse column in suggestions
    if wh_col and wh_col not in suggested:
        suggested = [wh_col] + suggested

    # Default to suggested if available, else all columns (max 10)
    default_selection = suggested if suggested else all_cols[:10]

    st.markdown(f'<div class="info-box">💡 <b>{len(suggested)}</b> useful columns auto-suggested. You can add or remove as needed.</div>', unsafe_allow_html=True)

    selected_cols = st.multiselect(
        "Select columns to include in your download:",
        options=all_cols,
        default=[c for c in default_selection if c in all_cols],
        help="Pick only the columns you need. You can add or remove any.",
    )

    if not selected_cols:
        st.markdown('<div class="warn-box">⚠️ Please select at least one column.</div>', unsafe_allow_html=True)
    else:
        df_output = df_filtered[selected_cols].reset_index(drop=True)

        # ─── Step 5: Preview & Download ───────────────────────────────────────
        st.markdown("""
        <div class="card">
            <div class="card-title"><span class="step-badge">5</span> Preview & Download</div>
        </div>
        """, unsafe_allow_html=True)

        preview_rows = min(50, len(df_output))
        st.dataframe(
            df_output.head(preview_rows),
            use_container_width=True,
            height=min(400, 50 + preview_rows * 35),
        )

        if len(df_output) > preview_rows:
            st.markdown(f'<div class="info-box">👁 Showing first {preview_rows} of {len(df_output):,} rows. Full data will be in the downloaded file.</div>', unsafe_allow_html=True)

        st.markdown("<hr class='divider'>", unsafe_allow_html=True)

        # Metrics
        st.markdown(f"""
        <div class="metric-row">
            <div class="metric-box"><div class="mval">{len(df_output):,}</div><div class="mlbl">Rows</div></div>
            <div class="metric-box"><div class="mval">{len(selected_cols)}</div><div class="mlbl">Columns</div></div>
        </div>
        """, unsafe_allow_html=True)

        # Generate Excel
        try:
            excel_bytes = df_to_excel_bytes(df_output)
            safe_wh = warehouse_input.strip().replace(" ", "_").replace("/", "-")
            filename = f"stock_{safe_wh}_{selected_sheet}.xlsx"

            st.download_button(
                label=f"⬇️  Download Excel ({len(df_output):,} rows)",
                data=excel_bytes,
                file_name=filename,
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            )
        except Exception as e:
            st.markdown(f'<div class="error-box">❌ Download error: {e}<br>Try: <code>pip install openpyxl</code></div>', unsafe_allow_html=True)

# ─── Footer ───────────────────────────────────────────────────────────────────
st.markdown("""
<div style='text-align:center; margin-top:2rem; color:rgba(255,255,255,0.2); font-size:0.78rem; font-weight:700;'>
    STOCK EXTRACTOR v1.0 · No data is stored or sent anywhere
</div>
""", unsafe_allow_html=True)
