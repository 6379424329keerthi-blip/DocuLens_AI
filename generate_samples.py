"""
Script to generate sample documents for DocuLens AI hackathon demo.
Creates high-fidelity multi-page PDFs with text, tables, and charts using matplotlib.
"""

from pathlib import Path
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

SAMPLE_DIR = Path(__file__).parent / "sample_documents"
SAMPLE_DIR.mkdir(parents=True, exist_ok=True)

def create_annual_report():
    pdf_path = SAMPLE_DIR / "annual_report.pdf"
    with PdfPages(pdf_path) as pdf:
        # Page 1: Cover & Strategic Priorities
        fig, ax = plt.subplots(figsize=(8.5, 11))
        ax.axis("off")
        
        # Header
        ax.text(0.5, 0.92, "ACME GLOBAL TECHNOLOGIES", fontsize=22, weight="bold", ha="center")
        ax.text(0.5, 0.88, "ANNUAL PERFORMANCE & STRATEGIC REPORT 2025", fontsize=14, color="#333333", ha="center")
        ax.plot([0.1, 0.9], [0.85, 0.85], color="#1a73e8", lw=3)
        
        # Executive Summary
        ax.text(0.1, 0.78, "Executive Summary", fontsize=16, weight="bold", color="#1a73e8")
        summary_text = (
            "Acme Global Technologies delivers next-generation AI and document intelligence solutions.\n"
            "In fiscal year 2025, the company delivered record financial expansion driven by enterprise\n"
            "adoption across North America, Europe, and Asia-Pacific regions."
        )
        ax.text(0.1, 0.71, summary_text, fontsize=11, linespacing=1.6)
        
        # Strategic Priorities
        ax.text(0.1, 0.60, "Company Strategic Priorities", fontsize=16, weight="bold", color="#1a73e8")
        priorities_text = (
            "Our corporate strategy for 2025-2027 focuses on three key strategic priorities:\n\n"
            "1. Multimodal AI Leadership: Accelerate development of vision-language architectures\n"
            "   for zero-shot enterprise document understanding and reasoning.\n\n"
            "2. Global Enterprise Expansion: Scale enterprise presence across Fortune 500 accounts\n"
            "   with certified sovereign cloud and private deployment options.\n\n"
            "3. Operational Efficiency & Sustainability: Reduce carbon intensity per compute job by 45%\n"
            "   and achieve net-zero infrastructure operations by 2028."
        )
        ax.text(0.1, 0.38, priorities_text, fontsize=11, linespacing=1.5)
        
        ax.text(0.5, 0.05, "Page 1 — Annual Report 2025", fontsize=10, color="#888888", ha="center")
        pdf.savefig(fig, bbox_inches="tight")
        plt.close(fig)
        
        # Page 2: Financial Performance Table
        fig, ax = plt.subplots(figsize=(8.5, 11))
        ax.axis("off")
        
        ax.text(0.1, 0.92, "Financial Performance & Revenue Summary", fontsize=18, weight="bold", color="#1a73e8")
        ax.plot([0.1, 0.9], [0.89, 0.89], color="#1a73e8", lw=2)
        
        intro_text = (
            "The following audited financial table outlines key corporate performance indicators\n"
            "for the fiscal years 2022 through 2025. All monetary amounts are in Indian Rupees (Crores)."
        )
        ax.text(0.1, 0.82, intro_text, fontsize=11, linespacing=1.6)
        
        # Table
        col_labels = ["Fiscal Year", "Revenue (Cr)", "Operating Cost (Cr)", "EBITDA (Cr)", "Net Profit (Cr)"]
        table_data = [
            ["2022", "7.5 Cr", "5.2 Cr", "2.3 Cr", "1.8 Cr"],
            ["2023", "10.0 Cr", "6.8 Cr", "3.2 Cr", "2.5 Cr"],
            ["2024", "14.0 Cr", "9.1 Cr", "4.9 Cr", "3.8 Cr"],
            ["2025", "21.0 Cr", "13.0 Cr", "8.0 Cr", "6.2 Cr"],
        ]
        
        table = ax.table(
            cellText=table_data,
            colLabels=col_labels,
            loc="center",
            cellLoc="center",
            bbox=[0.1, 0.52, 0.8, 0.24]
        )
        table.auto_set_font_size(False)
        table.set_fontsize(11)
        for (row, col), cell in table.get_celld().items():
            if row == 0:
                cell.set_facecolor("#1a73e8")
                cell.set_text_props(color="white", weight="bold")
            else:
                cell.set_facecolor("#f8f9fa" if row % 2 == 1 else "white")
        
        notes_text = (
            "Key Observations:\n"
            "• Revenue expanded significantly from 10.0 Cr in 2023 to 21.0 Cr in 2025.\n"
            "• Percentage increase in revenue from 2023 to 2025 is calculated as:\n"
            "  (21.0 - 10.0) / 10.0 * 100 = 110%.\n"
            "• Historical records prior to 2022 are maintained in archived legacy ledgers."
        )
        ax.text(0.1, 0.28, notes_text, fontsize=11, linespacing=1.6)
        
        ax.text(0.5, 0.05, "Page 2 — Financial Performance", fontsize=10, color="#888888", ha="center")
        pdf.savefig(fig, bbox_inches="tight")
        plt.close(fig)

        # Page 3: Visual Chart & Growth Analysis
        fig, ax = plt.subplots(figsize=(8.5, 11))
        
        # Subplot for chart
        plt.subplots_adjust(top=0.85, bottom=0.35, left=0.15, right=0.85)
        years = ["2023", "2024", "2025"]
        growth_rates = [33.3, 40.0, 50.0]  # YoY %
        
        bars = ax.bar(years, growth_rates, color=["#6baed6", "#3182bd", "#08519c"], width=0.55)
        ax.set_ylabel("YoY Revenue Growth Rate (%)", fontsize=12, weight="bold")
        ax.set_ylim(0, 65)
        ax.set_title("Year-over-Year Revenue Growth Trend (2023 - 2025)", fontsize=14, weight="bold", pad=15)
        
        for bar in bars:
            height = bar.get_height()
            ax.annotate(f"{height:.1f}%",
                        xy=(bar.get_x() + bar.get_width() / 2, height),
                        xytext=(0, 5), textcoords="offset points",
                        ha="center", va="bottom", fontsize=11, weight="bold")

        fig.text(0.5, 0.93, "Visual Growth & Trend Analysis", fontsize=18, weight="bold", color="#1a73e8", ha="center")
        caption_text = (
            "Figure 1: Comparative Year-over-Year Growth Rate.\n"
            "According to the chart, the year 2025 recorded the highest growth rate at 50.0%,\n"
            "outperforming 2024 (40.0%) and 2023 (33.3%). This confirms accelerating business momentum."
        )
        fig.text(0.15, 0.22, caption_text, fontsize=11, linespacing=1.6)
        fig.text(0.5, 0.05, "Page 3 — Visual Growth Analysis", fontsize=10, color="#888888", ha="center")
        
        pdf.savefig(fig, bbox_inches="tight")
        plt.close(fig)
        
    print(f"Generated {pdf_path}")

def create_financial_report():
    pdf_path = SAMPLE_DIR / "financial_report.pdf"
    with PdfPages(pdf_path) as pdf:
        fig, ax = plt.subplots(figsize=(8.5, 11))
        ax.axis("off")
        ax.text(0.5, 0.92, "TECHNOVA CORP — FINANCIAL STATEMENTS", fontsize=20, weight="bold", ha="center")
        ax.text(0.5, 0.87, "Quarterly Earnings & Balance Sheet Analysis (Q1 - Q4 2024)", fontsize=13, ha="center")
        ax.plot([0.1, 0.9], [0.84, 0.84], color="#2ca02c", lw=2.5)

        col_labels = ["Quarter", "Gross Margin (%)", "Operating Margin (%)", "R&D Spend ($M)", "Free Cash Flow ($M)"]
        data = [
            ["Q1 2024", "64.2%", "22.1%", "$45.2 M", "$28.0 M"],
            ["Q2 2024", "65.8%", "23.5%", "$48.0 M", "$32.4 M"],
            ["Q3 2024", "67.1%", "25.0%", "$51.6 M", "$37.8 M"],
            ["Q4 2024", "69.4%", "27.2%", "$55.1 M", "$44.5 M"],
        ]
        table = ax.table(cellText=data, colLabels=col_labels, loc="center", cellLoc="center", bbox=[0.1, 0.55, 0.8, 0.24])
        table.auto_set_font_size(False)
        table.set_fontsize(11)
        for (row, col), cell in table.get_celld().items():
            if row == 0:
                cell.set_facecolor("#2ca02c")
                cell.set_text_props(color="white", weight="bold")
            else:
                cell.set_facecolor("#f0fdf4" if row % 2 == 1 else "white")

        ax.text(0.1, 0.38, "Auditor Notes:\nGross margins demonstrated quarter-over-quarter expansion reaching 69.4% in Q4.\nTotal full-year R&D commitment amounted to $199.9 Million.", fontsize=11, linespacing=1.6)
        ax.text(0.5, 0.05, "Page 1 — Financial Statements", fontsize=10, color="#888888", ha="center")
        pdf.savefig(fig, bbox_inches="tight")
        plt.close(fig)
    print(f"Generated {pdf_path}")

def create_research_report():
    pdf_path = SAMPLE_DIR / "research_report.pdf"
    with PdfPages(pdf_path) as pdf:
        fig, ax = plt.subplots(figsize=(8.5, 11))
        ax.axis("off")
        ax.text(0.5, 0.92, "Multimodal RAG Architectures: An Empirical Benchmark", fontsize=18, weight="bold", ha="center")
        ax.text(0.5, 0.87, "AI Research Labs — Technical Report #2025-04", fontsize=12, color="#555555", ha="center")
        ax.plot([0.1, 0.9], [0.84, 0.84], color="#7b1fa2", lw=2.5)

        abstract = (
            "Abstract:\n"
            "We evaluate multimodal document intelligence frameworks across complex documents containing\n"
            "dense tabular structures, high-resolution chart images, and multi-column typography.\n"
            "Our findings indicate that multimodal grounding achieves a 94.2% factual precision rate,\n"
            "drastically reducing hallucinations compared to text-only baselines."
        )
        ax.text(0.1, 0.68, abstract, fontsize=11, linespacing=1.6)

        col_labels = ["Model Pipeline", "Table QA Accuracy", "Chart Reasoning", "Hallucination Rate"]
        data = [
            ["Text-Only RAG", "62.4%", "14.2%", "34.8%"],
            ["OCR + Text RAG", "74.1%", "28.5%", "22.6%"],
            ["DocuLens Multimodal", "92.8%", "89.4%", "4.1%"],
        ]
        table = ax.table(cellText=data, colLabels=col_labels, loc="center", cellLoc="center", bbox=[0.1, 0.38, 0.8, 0.22])
        table.auto_set_font_size(False)
        table.set_fontsize(11)
        for (row, col), cell in table.get_celld().items():
            if row == 0:
                cell.set_facecolor("#7b1fa2")
                cell.set_text_props(color="white", weight="bold")
            else:
                cell.set_facecolor("#faf5ff" if row % 2 == 1 else "white")

        ax.text(0.5, 0.05, "Page 1 — Empirical Benchmark", fontsize=10, color="#888888", ha="center")
        pdf.savefig(fig, bbox_inches="tight")
        plt.close(fig)
    print(f"Generated {pdf_path}")

if __name__ == "__main__":
    create_annual_report()
    create_financial_report()
    create_research_report()
