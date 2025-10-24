import regex as re

def extract_specs(snippet: str):
    """
    Pull key facts (BUA, plot range, floor areas) for JSON response.
    """
    norm = " ".join(snippet.split())
    m_bua = re.search(r"TOTAL\s+BUA\s+(\d+)\s*SQM\s+(\d[\d,]*)\s*SQFT", norm, flags=re.I)
    m_plot = re.search(r"PLOT\s+AREA\s+FROM\s+(\d+)\s+TO\s+(\d+)\s+SQM", norm, flags=re.I)
    m_ext = re.search(r"EXTERNAL\s+AREA\s+FROM\s+(\d+)\s+TO\s+(\d+)\s+SQM", norm, flags=re.I)

    payload = {}
    if m_bua: payload["bua_sqm"] = int(m_bua.group(1))
    if m_plot: payload["plot_sqm_range"] = [int(m_plot.group(1)), int(m_plot.group(2))]
    if m_ext: payload["external_sqm_range"] = [int(m_ext.group(1)), int(m_ext.group(2))]
    return payload
