"""PPTX Export Engine — generates executive slide decks from simulation data.

Uses python-pptx to create professional presentations with:
  - Slide 1: Title + Executive Summary
  - Slide 2: KPI Dashboard
  - Slide 3: Sentiment Timeline
  - Slide 4: Action Plan + ROI
  - Slide 5: Recommendations
"""

import io
import logging
from typing import Dict, Any, List, Optional
from datetime import datetime

logger = logging.getLogger("mirofish.export_engine")


# ---------------------------------------------------------------
# PPTX Generator
# ---------------------------------------------------------------

class PPTXGenerator:
    """Generates a professional PPTX from MSaaS data."""

    # Color palette
    PRIMARY = "FF4500"      # Orange-red
    DARK = "1A1A1A"         # Near-black
    WHITE = "FFFFFF"
    GRAY = "888888"
    GREEN = "22C55E"
    RED = "EF4444"
    BLUE = "3498DB"

    def __init__(self):
        self.prs = None

    def generate(self, data: Dict[str, Any]) -> io.BytesIO:
        """Generate a full PPTX file and return as BytesIO."""
        try:
            from pptx import Presentation
            from pptx.util import Inches, Pt, Emu
            from pptx.enum.text import PP_ALIGN
            from pptx.dml.color import RGBColor
        except ImportError:
            return self._generate_fallback_xlsx(data)

        self.prs = Presentation()
        self.prs.slide_width = Inches(13.333)  # 16:9 widescreen
        self.prs.slide_height = Inches(7.5)

        slide_type = data.get("slide_type", "dashboard")

        if slide_type == "dashboard":
            self._slide_title(data)
            self._slide_kpi(data)
            self._slide_timeline(data)
            self._slide_action_plan(data)

        elif slide_type == "comparison":
            self._slide_title(data)
            self._slide_comparison(data)

        elif slide_type == "impact":
            self._slide_title(data)
            self._slide_impact(data)

        elif slide_type == "war_room":
            self._slide_title(data)
            self._slide_war_room(data)

        # Save to BytesIO
        buffer = io.BytesIO()
        self.prs.save(buffer)
        buffer.seek(0)
        return buffer

    # -----------------------------------------------------------
    # Slide builders
    # -----------------------------------------------------------

    def _slide_title(self, data: Dict[str, Any]):
        from pptx.util import Inches, Pt
        from pptx.enum.text import PP_ALIGN
        from pptx.dml.color import RGBColor

        slide = self.prs.slides.add_slide(self.prs.slide_layouts[6])  # blank

        # Background
        bg = slide.background
        bg.fill.solid()
        bg.fill.fore_color.rgb = RGBColor(0x1A, 0x1A, 0x1A)

        # Title
        title_box = slide.shapes.add_textbox(Inches(1), Inches(2), Inches(11), Inches(1.5))
        tf = title_box.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = data.get("title", "MSaaS Executive Report")
        p.font.size = Pt(36)
        p.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
        p.font.bold = True
        p.alignment = PP_ALIGN.LEFT

        # Subtitle
        sub_box = slide.shapes.add_textbox(Inches(1), Inches(3.5), Inches(11), Inches(1))
        tf2 = sub_box.text_frame
        p2 = tf2.paragraphs[0]
        p2.text = data.get("subtitle", f"Generated {datetime.now().strftime('%d %B %Y')}")
        p2.font.size = Pt(18)
        p2.font.color.rgb = RGBColor(0x88, 0x88, 0x88)

        # Orange accent line
        line = slide.shapes.add_shape(1, Inches(1), Inches(3.2), Inches(2), Inches(0.04))  # rectangle as line
        line.fill.solid()
        line.fill.fore_color.rgb = RGBColor(0xFF, 0x45, 0x00)
        line.line.fill.background()

        # Logo text
        logo_box = slide.shapes.add_textbox(Inches(1), Inches(6.5), Inches(4), Inches(0.5))
        tf3 = logo_box.text_frame
        p3 = tf3.paragraphs[0]
        p3.text = "MiroFish MSaaS"
        p3.font.size = Pt(12)
        p3.font.color.rgb = RGBColor(0x88, 0x88, 0x88)

    def _slide_kpi(self, data: Dict[str, Any]):
        from pptx.util import Inches, Pt
        from pptx.enum.text import PP_ALIGN
        from pptx.dml.color import RGBColor

        kpis = data.get("kpis", {})
        slide = self.prs.slides.add_slide(self.prs.slide_layouts[6])

        # Title
        self._add_section_title(slide, "KPI Dashboard")

        # KPI cards (2 rows × 4 columns)
        metrics = [
            ("Overall Sentiment", kpis.get("overall_sentiment", 0), ""),
            ("Conversion", kpis.get("conversion_probability", 0), "%"),
            ("Social Influence", kpis.get("social_influence_index", 0), "/100"),
            ("Message Resonance", kpis.get("message_resonance", 0), "%"),
            ("Crisis Risk", kpis.get("crisis_risk", 0), "%"),
            ("Brand Shift", kpis.get("brand_perception_shift", 0), ""),
            ("Polarization", kpis.get("opinion_polarization", 0), ""),
            ("ROI", kpis.get("roi_pct", 0), "%"),
        ]

        for i, (label, value, unit) in enumerate(metrics[:8]):
            col = i % 4
            row = i // 4
            x = Inches(1 + col * 3)
            y = Inches(2 + row * 2.5)

            card = slide.shapes.add_shape(5, x, y, Inches(2.5), Inches(2))  # rounded rect
            card.fill.solid()
            card.fill.fore_color.rgb = RGBColor(0xF5, 0xF5, 0xF5)
            card.line.color.rgb = RGBColor(0xE0, 0xE0, 0xE0)

            tf = card.text_frame
            tf.word_wrap = True

            p_label = tf.paragraphs[0]
            p_label.text = label
            p_label.font.size = Pt(10)
            p_label.font.color.rgb = RGBColor(0x88, 0x88, 0x88)
            p_label.alignment = PP_ALIGN.CENTER

            p_value = tf.add_paragraph()
            p_value.text = f"{value}{unit}"
            p_value.font.size = Pt(28)
            p_value.font.bold = True
            p_value.alignment = PP_ALIGN.CENTER

            if isinstance(value, (int, float)):
                p_value.font.color.rgb = RGBColor(0x22, 0xC5, 0x5E) if value >= 0 else RGBColor(0xEF, 0x44, 0x44)

    def _slide_timeline(self, data: Dict[str, Any]):
        from pptx.util import Inches, Pt
        from pptx.dml.color import RGBColor

        timeline = data.get("timeline", [])
        if not timeline:
            return

        slide = self.prs.slides.add_slide(self.prs.slide_layouts[6])
        self._add_section_title(slide, "Sentiment Timeline")

        # Simple table for timeline
        rows = min(len(timeline), 12)
        cols = 3

        table = slide.shapes.add_table(rows + 1, cols, Inches(1), Inches(2), Inches(11), Inches(5)).table
        table.columns[0].width = Inches(2)
        table.columns[1].width = Inches(5)
        table.columns[2].width = Inches(4)

        # Headers
        headers = ["Round", "Sentiment", "Actions"]
        for j, h in enumerate(headers):
            cell = table.cell(0, j)
            cell.text = h
            for p in cell.text_frame.paragraphs:
                p.font.bold = True
                p.font.size = Pt(10)

        for i, pt in enumerate(timeline[:rows]):
            r = i + 1
            table.cell(r, 0).text = f"R{pt.get('round_num', r)}"
            sent = pt.get("avg_sentiment", 0)
            table.cell(r, 1).text = f"{'+' if sent > 0 else ''}{sent}"
            table.cell(r, 2).text = str(pt.get("action_count", 0))

    def _slide_action_plan(self, data: Dict[str, Any]):
        from pptx.util import Inches, Pt
        from pptx.dml.color import RGBColor
        from pptx.enum.text import PP_ALIGN

        slide = self.prs.slides.add_slide(self.prs.slide_layouts[6])
        self._add_section_title(slide, "Action Plan & Recommendations")

        # Recommendation box
        rec = data.get("recommendation", "No recommendation available.")
        box = slide.shapes.add_textbox(Inches(1), Inches(2), Inches(11), Inches(1.5))
        tf = box.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = rec
        p.font.size = Pt(14)
        p.font.color.rgb = RGBColor(0xFF, 0x45, 0x00)

        action_plan = data.get("action_plan") or {}
        action_rows = self._action_plan_rows(action_plan)
        if action_rows:
            source = (action_plan.get("source") or {}).get("type", "unknown")
            disclaimer = action_plan.get("disclaimer", "")
            meta_box = slide.shapes.add_textbox(Inches(1), Inches(3.35), Inches(11), Inches(0.45))
            meta_p = meta_box.text_frame.paragraphs[0]
            meta_p.text = f"Source: {source} | {disclaimer}"
            meta_p.font.size = Pt(9)
            meta_p.font.color.rgb = RGBColor(0x88, 0x88, 0x88)

            rows = min(len(action_rows), 4)
            table = slide.shapes.add_table(rows + 1, 4, Inches(1), Inches(3.95), Inches(11.3), Inches(2.5)).table
            widths = [2.1, 3.4, 3.0, 2.8]
            for col_idx, width in enumerate(widths):
                table.columns[col_idx].width = Inches(width)
            for col_idx, header in enumerate(["Section", "Recommendation", "Expected Impact", "Risk"]):
                cell = table.cell(0, col_idx)
                cell.text = header
                for par in cell.text_frame.paragraphs:
                    par.font.bold = True
                    par.font.size = Pt(8)
            for row_idx, item in enumerate(action_rows[:rows], start=1):
                values = [
                    item.get("section", ""),
                    item.get("recommendation", ""),
                    item.get("expected_impact", ""),
                    item.get("risk", ""),
                ]
                for col_idx, value in enumerate(values):
                    cell = table.cell(row_idx, col_idx)
                    cell.text = str(value)[:180]
                    for par in cell.text_frame.paragraphs:
                        par.font.size = Pt(7)

            footer = slide.shapes.add_textbox(Inches(1), Inches(6.8), Inches(11), Inches(0.4))
            p4 = footer.text_frame.paragraphs[0]
            p4.text = f"Generated by 3C Simulator • {datetime.now().strftime('%Y-%m-%d %H:%M')}"
            p4.font.size = Pt(9)
            p4.font.color.rgb = RGBColor(0xAA, 0xAA, 0xAA)
            p4.alignment = PP_ALIGN.CENTER
            return

        # KPI summary
        kpis = data.get("kpis", {})
        summary = (
            f"Sentiment: {kpis.get('overall_sentiment', 'N/A')}  |  "
            f"Conversion: {kpis.get('conversion_probability', 'N/A')}%  |  "
            f"Message Resonance: {kpis.get('message_resonance', 'N/A')}%"
        )
        box2 = slide.shapes.add_textbox(Inches(1), Inches(3.8), Inches(11), Inches(0.5))
        tf2 = box2.text_frame
        p2 = tf2.paragraphs[0]
        p2.text = summary
        p2.font.size = Pt(12)
        p2.font.color.rgb = RGBColor(0x88, 0x88, 0x88)

        # Revenue projection
        rev = data.get("revenue_projection", {})
        if rev:
            proj = (
                f"Projected Monthly: ฿{rev.get('monthly', 0):,.0f}  |  "
                f"Annual: ฿{rev.get('annual', 0):,.0f}  |  "
                f"Crisis Risk: ฿{rev.get('crisis_loss', 0):,.0f}"
            )
            box3 = slide.shapes.add_textbox(Inches(1), Inches(4.5), Inches(11), Inches(0.5))
            tf3 = box3.text_frame
            p3 = tf3.paragraphs[0]
            p3.text = proj
            p3.font.size = Pt(12)
            p3.font.color.rgb = RGBColor(0x22, 0xC5, 0x5E)

        # Footer
        footer = slide.shapes.add_textbox(Inches(1), Inches(6.8), Inches(11), Inches(0.4))
        tf4 = footer.text_frame
        p4 = tf4.paragraphs[0]
        p4.text = f"Generated by 3C Simulator • {datetime.now().strftime('%Y-%m-%d %H:%M')}"
        p4.font.size = Pt(9)
        p4.font.color.rgb = RGBColor(0xAA, 0xAA, 0xAA)
        p4.alignment = PP_ALIGN.CENTER

    def _action_plan_rows(self, action_plan: Dict[str, Any]) -> List[Dict[str, Any]]:
        rows = []
        for section_key, section in (action_plan.get("sections") or {}).items():
            title = section.get("title", section_key)
            for item in section.get("items", []):
                rows.append({
                    "section": title,
                    "recommendation": item.get("recommendation", ""),
                    "reason": item.get("reason", ""),
                    "expected_impact": item.get("expected_impact", ""),
                    "risk": item.get("risk", ""),
                })
        return rows

    def _slide_comparison(self, data: Dict[str, Any]):
        from pptx.util import Inches, Pt
        from pptx.dml.color import RGBColor
        from pptx.enum.text import PP_ALIGN

        slide = self.prs.slides.add_slide(self.prs.slide_layouts[6])
        self._add_section_title(slide, "A/B Comparison Results")

        comparison = data.get("comparison", {})
        winner = comparison.get("overall_winner", {})
        metrics = comparison.get("metrics_comparison", [])
        source = comparison.get("source") or data.get("source") or {}

        # Winner banner
        win_box = slide.shapes.add_textbox(Inches(1), Inches(2), Inches(11), Inches(1))
        tf = win_box.text_frame
        p = tf.paragraphs[0]
        p.text = f"🏆 Winner: {winner.get('campaign_name', 'N/A')} — {winner.get('metric_wins', 0)}/{winner.get('total_metrics', 7)} metrics won"
        p.font.size = Pt(20)
        p.font.color.rgb = RGBColor(0xFF, 0x45, 0x00)
        p.font.bold = True
        p.alignment = PP_ALIGN.CENTER

        if source:
            source_box = slide.shapes.add_textbox(Inches(1), Inches(2.95), Inches(11), Inches(0.35))
            source_p = source_box.text_frame.paragraphs[0]
            source_p.text = f"Source: {source.get('source_mode') or source.get('type', 'unknown')} | Basis: {source.get('data_basis', 'unknown')}"
            source_p.font.size = Pt(9)
            source_p.font.color.rgb = RGBColor(0x88, 0x88, 0x88)
            source_p.alignment = PP_ALIGN.CENTER

        # Metrics table
        if metrics:
            rows = len(metrics) + 1
            table = slide.shapes.add_table(rows, 3, Inches(1), Inches(3.5), Inches(11), Inches(3.5)).table
            table.columns[0].width = Inches(4)
            table.columns[1].width = Inches(4)
            table.columns[2].width = Inches(3)

            for j, h in enumerate(["Metric", "Best Value", "Difference"]):
                cell = table.cell(0, j)
                cell.text = h
                for par in cell.text_frame.paragraphs:
                    par.font.bold = True

            for i, m in enumerate(metrics):
                r = i + 1
                vals = m.get("values", [])
                unit = m.get("unit", "")
                best_val = m.get("winner_value", "")
                diff = m.get("max_diff", 0)

                table.cell(r, 0).text = m.get("label", "")
                table.cell(r, 1).text = f"{best_val}{unit}"
                table.cell(r, 2).text = f"Δ {diff}{unit}"

    def _slide_impact(self, data: Dict[str, Any]):
        from pptx.util import Inches, Pt
        from pptx.dml.color import RGBColor
        from pptx.enum.text import PP_ALIGN

        slide = self.prs.slides.add_slide(self.prs.slide_layouts[6])
        self._add_section_title(slide, "Business Impact Projection")

        scenarios = data.get("scenarios", [])
        if not scenarios:
            return

        # Scenario cards
        cols = len(scenarios)
        card_width = 11 / cols - 0.5

        for i, s in enumerate(scenarios):
            x = Inches(1 + i * (card_width + 0.5))
            y = Inches(2.5)

            card = slide.shapes.add_shape(5, x, y, Inches(card_width), Inches(3.5))
            card.fill.solid()
            card.fill.fore_color.rgb = RGBColor(0xF5, 0xF5, 0xF5)
            card.line.color.rgb = RGBColor(0xE0, 0xE0, 0xE0)

            tf = card.text_frame
            tf.word_wrap = True

            p_name = tf.paragraphs[0]
            p_name.text = s.get("scenario", "")
            p_name.font.size = Pt(14)
            p_name.font.bold = True
            p_name.alignment = PP_ALIGN.CENTER

            for label, key in [("Revenue", "estimated_revenue"), ("Units", "estimated_units"), ("ROI", "roi_pct")]:
                p_val = tf.add_paragraph()
                val = s.get(key, 0)
                unit = "%" if key == "roi_pct" else "฿" if key == "estimated_revenue" else ""
                p_val.text = f"\n{label}\n{val:,.0f}{unit}" if isinstance(val, (int, float)) else f"\n{label}\n{val}"
                p_val.font.size = Pt(11)
                p_val.alignment = PP_ALIGN.CENTER

        # Recommendation
        rec = data.get("recommendation", "")
        if rec:
            rec_box = slide.shapes.add_textbox(Inches(1), Inches(6.3), Inches(11), Inches(0.8))
            tf2 = rec_box.text_frame
            p2 = tf2.paragraphs[0]
            p2.text = rec
            p2.font.size = Pt(13)
            p2.font.color.rgb = RGBColor(0xFF, 0x45, 0x00)

    def _slide_war_room(self, data: Dict[str, Any]):
        from pptx.util import Inches, Pt
        from pptx.dml.color import RGBColor
        from pptx.enum.text import PP_ALIGN

        slide = self.prs.slides.add_slide(self.prs.slide_layouts[6])
        self._add_section_title(slide, "Competitor War Room Results")

        winner = data.get("winner", "N/A")
        shares = data.get("final_market_share", {})

        # Winner box
        w_box = slide.shapes.add_textbox(Inches(1), Inches(2), Inches(11), Inches(1))
        tf = w_box.text_frame
        p = tf.paragraphs[0]
        p.text = f"🏆 Winner: {winner}"
        p.font.size = Pt(24)
        p.font.color.rgb = RGBColor(0xFF, 0x45, 0x00)
        p.font.bold = True
        p.alignment = PP_ALIGN.CENTER

        # Share table
        if shares:
            rows = len(shares) + 1
            table = slide.shapes.add_table(rows, 3, Inches(2), Inches(3.5), Inches(9), Inches(2)).table
            table.columns[0].width = Inches(4)
            table.columns[1].width = Inches(2.5)
            table.columns[2].width = Inches(2.5)

            for j, h in enumerate(["Brand", "Share", "Change"]):
                cell = table.cell(0, j)
                cell.text = h
                for par in cell.text_frame.paragraphs:
                    par.font.bold = True

            shifts = data.get("share_shift", {})
            for i, (brand, share) in enumerate(shares.items()):
                r = i + 1
                shift = shifts.get(brand, 0)
                table.cell(r, 0).text = brand
                table.cell(r, 1).text = f"{share}%"
                table.cell(r, 2).text = f"{'+' if shift >= 0 else ''}{shift}%"

        # Key events
        events = data.get("key_events", [])
        if events:
            events_text = "\n".join(f"R{ev.get('round', '?')}: {ev.get('impact', '')}" for ev in events)
            ev_box = slide.shapes.add_textbox(Inches(1), Inches(6), Inches(11), Inches(1))
            tf2 = ev_box.text_frame
            p2 = tf2.paragraphs[0]
            p2.text = "Key Events:\n" + events_text
            p2.font.size = Pt(10)
            p2.font.color.rgb = RGBColor(0x88, 0x88, 0x88)

    # -----------------------------------------------------------
    # Helpers
    # -----------------------------------------------------------

    def _add_section_title(self, slide, text: str):
        from pptx.util import Inches, Pt
        from pptx.dml.color import RGBColor

        box = slide.shapes.add_textbox(Inches(1), Inches(0.5), Inches(11), Inches(1))
        tf = box.text_frame
        p = tf.paragraphs[0]
        p.text = text
        p.font.size = Pt(24)
        p.font.bold = True
        p.font.color.rgb = RGBColor(0x1A, 0x1A, 0x1A)

        # Orange underline
        line = slide.shapes.add_shape(1, Inches(1), Inches(1.4), Inches(2), Inches(0.04))
        line.fill.solid()
        line.fill.fore_color.rgb = RGBColor(0xFF, 0x45, 0x00)
        line.line.fill.background()

    def _generate_fallback_xlsx(self, data: Dict[str, Any]) -> io.BytesIO:
        """Fallback: generate simple CSV instead of PPTX when python-pptx unavailable."""
        import csv
        buffer = io.BytesIO()
        wrapper = io.TextIOWrapper(buffer, write_through=True, encoding='utf-8', newline='')
        writer = csv.writer(wrapper)
        writer.writerow(["MSaaS Export", data.get("title", "Report")])
        writer.writerow(["Generated", datetime.now().isoformat()])
        writer.writerow([])

        kpis = data.get("kpis", {})
        writer.writerow(["KPI", "Value"])
        for k, v in kpis.items():
            writer.writerow([k, v])

        wrapper.detach()
        buffer.seek(0)
        return buffer
