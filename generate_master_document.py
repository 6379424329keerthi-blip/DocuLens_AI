"""
Generator for Comprehensive 6-Page Enterprise Master Document.
Contains rich narrative text, multi-row financial tables, production efficiency metrics,
line/bar/pie charts, and calculation datasets tailored for PSI01 judging.
"""

from pathlib import Path
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

SAMPLE_DIR = Path(__file__).parent / "sample_documents"
SAMPLE_DIR.mkdir(parents=True, exist_ok=True)

def generate_master_pdf():
    pdf_path = SAMPLE_DIR / "comprehensive_enterprise_report.pdf"
    
    with PdfPages(pdf_path) as pdf:
        # =====================================================================
        # PAGE 1: Corporate Governance, Executive Letter & Strategic Pillars
        # =====================================================================
        fig, ax = plt.subplots(figsize=(8.5, 11))
        ax.axis("off")
        
        ax.text(0.5, 0.94, "APEX GLOBAL ENTERPRISES", fontsize=22, weight="bold", ha="center", color="#0f172a")
        ax.text(0.5, 0.90, "INTEGRATED ANNUAL PERFORMANCE & STRATEGY REPORT 2025", fontsize=12, color="#475569", ha="center")
        ax.plot([0.08, 0.92], [0.87, 0.87], color="#4f46e5", lw=3)
        
        ax.text(0.08, 0.82, "Letter from the Chief Executive Officer", fontsize=15, weight="bold", color="#4f46e5")
        ceo_letter = (
            "To Our Shareholders, Partners, and Enterprise Clients:\n\n"
            "Fiscal Year 2025 marked an extraordinary milestone in our corporate trajectory. Against a backdrop of\n"
            "accelerating digital transformation, Apex Global Enterprises delivered record financial expansion, driven\n"
            "by rapid adoption of our sovereign cloud and multimodal intelligence platforms across tier-1 enterprises.\n\n"
            "Our focus on operational discipline and capital allocation allowed us to outpace industry benchmarks while\n"
            "maintaining an uncompromising commitment to customer trust, security, and sustainability."
        )
        ax.text(0.08, 0.64, ceo_letter, fontsize=10.5, linespacing=1.6, color="#1e293b")
        
        ax.text(0.08, 0.58, "Three Core Strategic Pillars (2025 - 2027)", fontsize=15, weight="bold", color="#4f46e5")
        pillars_text = (
            "1. Multimodal AI Infrastructure Leadership:\n"
            "   Accelerate deployment of zero-shot vision-language models across enterprise workflows. In 2025, our AI\n"
            "   infrastructure achieved a 38.5% reduction in token inference latency while scaling to 1.2 billion daily requests.\n\n"
            "2. Global Production & Operational Excellence:\n"
            "   Upgrade our smart manufacturing and server assembly facilities with computer vision inspection systems,\n"
            "   driving double-digit gains in factory floor productivity across North American and European hubs.\n\n"
            "3. Sustainable Clean Compute & Zero-Emission Cloud:\n"
            "   Commitment to 100% renewable energy procurement across all data centers by 2027, reducing carbon\n"
            "   intensity per computed petaflop by 46.2% compared to the 2022 baseline."
        )
        ax.text(0.08, 0.28, pillars_text, fontsize=10.5, linespacing=1.5, color="#1e293b")
        
        ax.text(0.5, 0.05, "Page 1 of 6 · Apex Global Enterprises Annual Report 2025", fontsize=9.5, color="#94a3b8", ha="center")
        pdf.savefig(fig, bbox_inches="tight")
        plt.close(fig)

        # =====================================================================
        # PAGE 2: Production Efficiency, Operational Metrics & Factory Output
        # =====================================================================
        fig, ax = plt.subplots(figsize=(8.5, 11))
        ax.axis("off")
        
        ax.text(0.08, 0.94, "Manufacturing & Production Efficiency Analysis", fontsize=18, weight="bold", color="#4f46e5")
        ax.plot([0.08, 0.92], [0.91, 0.91], color="#4f46e5", lw=2)
        
        intro_p2 = (
            "During fiscal year 2024, our smart manufacturing division monitored production efficiency, scrap rates,\n"
            "and machine uptime across our primary automated server assembly lines on a quarterly basis."
        )
        ax.text(0.08, 0.84, intro_p2, fontsize=10.5, linespacing=1.6, color="#1e293b")
        
        # Table: Production Efficiency
        col_labels_p2 = ["Quarter", "Units Produced", "Machine Uptime", "Production Efficiency", "Cost per Unit", "Scrap Rate"]
        table_data_p2 = [
            ["Q1 2024", "450,000", "91.2%", "82.4%", "$48.50", "3.8%"],
            ["Q2 2024", "520,000", "94.6%", "86.8%", "$44.20", "2.9%"],
            ["Q3 2024", "580,000", "96.1%", "89.5%", "$41.80", "2.1%"],
            ["Q4 2024", "640,000", "97.8%", "93.2%", "$38.90", "1.4%"],
        ]
        table_p2 = ax.table(
            cellText=table_data_p2,
            colLabels=col_labels_p2,
            loc="center",
            cellLoc="center",
            bbox=[0.08, 0.52, 0.84, 0.26]
        )
        table_p2.auto_set_font_size(False)
        table_p2.set_fontsize(10.5)
        for (row, col), cell in table_p2.get_celld().items():
            if row == 0:
                cell.set_facecolor("#4f46e5")
                cell.set_text_props(color="white", weight="bold")
            else:
                cell.set_facecolor("#f8fafc" if row % 2 == 1 else "white")
        
        analysis_p2 = (
            "Detailed Operational Findings & Q2 vs Q4 Efficiency Comparison:\n"
            "• Production efficiency expanded from 86.8% in Q2 to 93.2% in Q4 (an absolute gain of +6.4 percentage points,\n"
            "  representing a +7.37% relative efficiency improvement).\n\n"
            "Three Primary Drivers for the Q2 to Q4 Efficiency Improvement:\n"
            "1. Automated Optical Inspection (AOI): Integrated inline computer vision scanners, slashing scrap rate from 2.9% to 1.4%.\n"
            "2. Predictive Sensor Maintenance: Reduced unscheduled line halts, driving machine uptime from 94.6% to 97.8%.\n"
            "3. Economies of Scale & Labor Re-allocation: Unit production costs fell by 12.0%, dropping from $44.20 to $38.90 per unit."
        )
        ax.text(0.08, 0.16, analysis_p2, fontsize=10.5, linespacing=1.6, color="#1e293b")
        
        ax.text(0.5, 0.05, "Page 2 of 6 · Apex Global Enterprises Annual Report 2025", fontsize=9.5, color="#94a3b8", ha="center")
        pdf.savefig(fig, bbox_inches="tight")
        plt.close(fig)

        # =====================================================================
        # PAGE 3: 5-Year Audited Financial Statement & Margin Analysis
        # =====================================================================
        fig, ax = plt.subplots(figsize=(8.5, 11))
        ax.axis("off")
        
        ax.text(0.08, 0.94, "Five-Year Financial Statements & Margin Analysis", fontsize=18, weight="bold", color="#4f46e5")
        ax.plot([0.08, 0.92], [0.91, 0.91], color="#4f46e5", lw=2)
        
        intro_p3 = (
            "Audited financial performance for fiscal years 2021 through 2025. All figures are presented in Millions\n"
            "of US Dollars ($M), prepared under International Financial Reporting Standards (IFRS)."
        )
        ax.text(0.08, 0.83, intro_p3, fontsize=10.5, linespacing=1.6, color="#1e293b")
        
        # Table: Financials
        col_labels_p3 = ["Financial Metric ($M)", "FY2021", "FY2022", "FY2023", "FY2024", "FY2025"]
        table_data_p3 = [
            ["Gross Revenue ($M)", "$210.0 M", "$260.0 M", "$340.0 M", "$450.0 M", "$612.0 M"],
            ["Cost of Goods Sold ($M)", "$115.5 M", "$137.8 M", "$173.4 M", "$220.5 M", "$287.6 M"],
            ["Gross Profit ($M)", "$94.5 M", "$122.2 M", "$166.6 M", "$229.5 M", "$324.4 M"],
            ["R&D Investments ($M)", "$32.0 M", "$41.5 M", "$56.0 M", "$78.0 M", "$105.0 M"],
            ["Operating Income ($M)", "$38.2 M", "$52.4 M", "$74.8 M", "$108.2 M", "$159.1 M"],
            ["Net Income ($M)", "$28.5 M", "$39.2 M", "$56.1 M", "$81.5 M", "$122.3 M"],
            ["Operating Margin (%)", "18.2%", "20.2%", "22.0%", "24.0%", "26.0%"],
            ["Net Profit Margin (%)", "13.6%", "15.1%", "16.5%", "18.1%", "20.0%"],
        ]
        table_p3 = ax.table(
            cellText=table_data_p3,
            colLabels=col_labels_p3,
            loc="center",
            cellLoc="center",
            bbox=[0.08, 0.40, 0.84, 0.38]
        )
        table_p3.auto_set_font_size(False)
        table_p3.set_fontsize(10)
        for (row, col), cell in table_p3.get_celld().items():
            if row == 0:
                cell.set_facecolor("#4f46e5")
                cell.set_text_props(color="white", weight="bold")
            else:
                cell.set_facecolor("#f8fafc" if row % 2 == 1 else "white")
        
        calc_notes = (
            "Key Financial Calculations & Growth Metrics:\n"
            "• Gross Revenue Growth (FY2023 to FY2025):\n"
            "  Formula: ((FY2025 Revenue - FY2023 Revenue) / FY2023 Revenue) * 100\n"
            "  Calculation: (($612.0 M - $340.0 M) / $340.0 M) * 100 = 80.0% Increase.\n"
            "• Net Income Expansion (FY2023 to FY2025):\n"
            "  Formula: (($122.3 M - $56.1 M) / $56.1 M) * 100 = 118.0% Increase.\n"
            "• Operating Margin expanded by 7.8 percentage points from 18.2% (2021) to 26.0% (2025)."
        )
        ax.text(0.08, 0.12, calc_notes, fontsize=10.5, linespacing=1.6, color="#1e293b")
        
        ax.text(0.5, 0.05, "Page 3 of 6 · Apex Global Enterprises Annual Report 2025", fontsize=9.5, color="#94a3b8", ha="center")
        pdf.savefig(fig, bbox_inches="tight")
        plt.close(fig)

        # =====================================================================
        # PAGE 4: Visual Chart 1 — Quarterly Revenue Expansion & Operating Margins
        # =====================================================================
        fig, ax1 = plt.subplots(figsize=(8.5, 11))
        
        # Subplot positioning
        fig.subplots_adjust(top=0.82, bottom=0.38, left=0.15, right=0.85)
        
        quarters = ["Q1 2024", "Q2 2024", "Q3 2024", "Q4 2024"]
        rev_data = [95.0, 110.0, 122.0, 145.0]  # $M
        margin_data = [21.5, 23.2, 25.1, 28.0]  # %
        
        # Bar plot
        bars = ax1.bar(quarters, rev_data, color="#4f46e5", width=0.45, label="Quarterly Revenue ($M)")
        ax1.set_ylabel("Gross Revenue ($ Millions)", fontsize=11, weight="bold", color="#4f46e5")
        ax1.set_ylim(0, 175)
        ax1.grid(axis='y', linestyle='--', alpha=0.3)
        
        for bar in bars:
            h = bar.get_height()
            ax1.annotate(f"${h:.0f}M", xy=(bar.get_x() + bar.get_width() / 2, h),
                         xytext=(0, 4), textcoords="offset points", ha="center", va="bottom", fontsize=10, weight="bold")

        # Line plot on secondary axis
        ax2 = ax1.twinx()
        line = ax2.plot(quarters, margin_data, color="#06b6d4", marker="o", linewidth=3, markersize=8, label="Operating Margin (%)")
        ax2.set_ylabel("Operating Margin (%)", fontsize=11, weight="bold", color="#06b6d4")
        ax2.set_ylim(15, 32)
        
        for i, val in enumerate(margin_data):
            ax2.annotate(f"{val:.1f}%", xy=(i, val), xytext=(0, 7), textcoords="offset points",
                         ha="center", va="bottom", fontsize=10, weight="bold", color="#0891b2")

        fig.text(0.5, 0.93, "Visual Trend: Quarterly Revenue & Operating Margin (2024)", fontsize=16, weight="bold", color="#0f172a", ha="center")
        fig.text(0.5, 0.89, "Figure 1: Audited quarterly trajectory demonstrating accelerating Q4 business volume.", fontsize=11, color="#64748b", ha="center")

        chart_caption = (
            "Visual Chart Observations:\n"
            "• Revenue accelerated from $95.0M in Q1 to a peak of $145.0M in Q4 2024 (a quarterly increase of $50.0M or +52.6%).\n"
            "• According to the line plot, Operating Margin expanded every quarter, reaching its peak of 28.0% in Q4.\n"
            "• The steepest quarterly revenue increase occurred between Q3 ($122M) and Q4 ($145M), an addition of $23.0M."
        )
        fig.text(0.12, 0.16, chart_caption, fontsize=10.5, linespacing=1.6, color="#1e293b")
        fig.text(0.5, 0.05, "Page 4 of 6 · Apex Global Enterprises Annual Report 2025", fontsize=9.5, color="#94a3b8", ha="center")
        
        pdf.savefig(fig, bbox_inches="tight")
        plt.close(fig)

        # =====================================================================
        # PAGE 5: Visual Chart 2 — Regional Revenue Share & Operational Costs
        # =====================================================================
        fig, (ax_pie, ax_bar) = plt.subplots(1, 2, figsize=(10, 7))
        fig.subplots_adjust(top=0.78, bottom=0.30, left=0.1, right=0.9, wspace=0.35)
        
        # Pie chart
        regions = ["North America", "Europe", "Asia-Pacific", "Latin America & MEA"]
        shares = [44, 28, 20, 8]
        colors = ["#4f46e5", "#06b6d4", "#10b981", "#f59e0b"]
        ax_pie.pie(shares, labels=regions, autopct='%1.0f%%', startangle=140, colors=colors, textprops={'fontsize': 9.5, 'weight': 'bold'})
        ax_pie.set_title("Figure 2A: Regional Revenue Share", fontsize=12, weight="bold", pad=12)

        # Cost Breakdown Bar
        cost_categories = ["R&D Compute", "Sales & Mktg", "General Admin", "Cloud Infra"]
        cost_amounts = [105.0, 78.5, 42.0, 62.1]  # $M
        ax_bar.barh(cost_categories, cost_amounts, color=["#6366f1", "#38bdf8", "#34d399", "#fbbf24"], height=0.5)
        ax_bar.set_xlabel("Expenditure ($ Millions)", fontsize=10, weight="bold")
        ax_bar.set_title("Figure 2B: FY2025 Operating Expenses", fontsize=12, weight="bold", pad=12)
        for i, v in enumerate(cost_amounts):
            ax_bar.text(v + 2, i, f"${v:.1f}M", va='center', fontsize=9.5, weight='bold')

        fig.text(0.5, 0.92, "Visual Modality: Regional Revenue & Expense Distribution", fontsize=16, weight="bold", color="#0f172a", ha="center")
        
        caption_p5 = (
            "Key Observations from Visual Charts:\n"
            "• According to the regional pie chart (Figure 2A), North America represents the largest market at 44% of global revenue,\n"
            "  followed by Europe (28%), Asia-Pacific (20%), and Latin America & MEA (8%).\n"
            "• R&D Compute was the largest single operational investment at $105.0 Million, reflecting ongoing AI infrastructure expansion."
        )
        fig.text(0.1, 0.12, caption_p5, fontsize=10.5, linespacing=1.6, color="#1e293b")
        fig.text(0.5, 0.04, "Page 5 of 6 · Apex Global Enterprises Annual Report 2025", fontsize=9.5, color="#94a3b8", ha="center")
        
        pdf.savefig(fig, bbox_inches="tight")
        plt.close(fig)

        # =====================================================================
        # PAGE 6: Capital Expenditures & Scope Boundary (Anti-Hallucination)
        # =====================================================================
        fig, ax = plt.subplots(figsize=(8.5, 11))
        ax.axis("off")
        
        ax.text(0.08, 0.94, "Capital Allocation & Document Scope Boundaries", fontsize=18, weight="bold", color="#4f46e5")
        ax.plot([0.08, 0.92], [0.91, 0.91], color="#4f46e5", lw=2)
        
        capex_intro = (
            "The following audited schedule outlines Capital Expenditures (CapEx) allocated across primary physical infrastructure\n"
            "and hardware assets for fiscal years 2023 through 2025."
        )
        ax.text(0.08, 0.83, capex_intro, fontsize=10.5, linespacing=1.6, color="#1e293b")

        # Table CapEx
        col_labels_p6 = ["Capital Asset Class", "FY2023 ($M)", "FY2024 ($M)", "FY2025 ($M)", "Growth Rate (23-25)"]
        table_data_p6 = [
            ["AI Server Hardware & GPUs", "$45.0 M", "$72.0 M", "$112.5 M", "+150.0%"],
            ["Green Data Center Facilities", "$28.0 M", "$35.0 M", "$48.0 M", "+71.4%"],
            ["Advanced Robotics & AOI", "$12.0 M", "$18.5 M", "$24.0 M", "+100.0%"],
            ["Corporate Real Estate & Labs", "$10.0 M", "$9.5 M", "$8.5 M", "-15.0%"],
            ["Total Capital Expenditures", "$95.0 M", "$135.0 M", "$193.0 M", "+103.2%"],
        ]
        table_p6 = ax.table(
            cellText=table_data_p6,
            colLabels=col_labels_p6,
            loc="center",
            cellLoc="center",
            bbox=[0.08, 0.52, 0.84, 0.26]
        )
        table_p6.auto_set_font_size(False)
        table_p6.set_fontsize(10.5)
        for (row, col), cell in table_p6.get_celld().items():
            if row == 0:
                cell.set_facecolor("#4f46e5")
                cell.set_text_props(color="white", weight="bold")
            else:
                cell.set_facecolor("#f8fafc" if row % 2 == 1 else "white")

        # Crucial Anti-Hallucination Scope Boundary
        boundary_box = (
            "AUDITOR DISCLOSURE & DOCUMENT BOUNDARY NOTICE:\n\n"
            "• Temporal Scope Limitation:\n"
            "  This integrated annual report covers financial statements, capital allocations, and manufacturing output\n"
            "  strictly for the period of fiscal years 2021 through 2025.\n\n"
            "• Historical Ledgers (Pre-2021 Unavailability):\n"
            "  Financial performance, profit, and production records prior to 2021 (such as fiscal years 2018, 2019, or 2020)\n"
            "  are maintained in separate legacy corporate archives and ARE NOT CONTAINED within this document.\n\n"
            "• Verification Standard:\n"
            "  Any queries regarding corporate revenue or profit for 2018, 2019, or 2020 cannot be verified from this publication."
        )
        ax.text(0.08, 0.16, boundary_box, fontsize=10.5, linespacing=1.6, color="#475569")
        
        ax.text(0.5, 0.05, "Page 6 of 6 · Apex Global Enterprises Annual Report 2025", fontsize=9.5, color="#94a3b8", ha="center")
        pdf.savefig(fig, bbox_inches="tight")
        plt.close(fig)

    print(f"Master Document Generated: {pdf_path}")

if __name__ == "__main__":
    generate_master_pdf()
