from __future__ import annotations

import html
import logging
import re
from datetime import datetime
from uuid import uuid4

from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.parsers import FormParser, JSONParser, MultiPartParser
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import KpiChatRequestSerializer, KpiUploadRequestSerializer

logger = logging.getLogger(__name__)


def _format_kpi_csv_report_html(result: dict) -> str:
    """Render the same KPI CSV report HTML used by the legacy dashboard UI.

    The KPI CSV processor returns a dict with keys like:
    - status, message/help (error)
    - summary, recommendations, daily_kpis, ai_analysis (success)
    """
    if not isinstance(result, dict):
        return _ensure_html(str(result))

    if result.get("status") == "error":
        message = html.escape(str(result.get("message") or "Unknown error"))
        help_text = result.get("help")
        found_columns = result.get("found_columns")

        parts = [
            '<div class="report">',
            '<div class="report__header" style="background: linear-gradient(135deg, #ef4444, #dc2626);">',
            '<h2>❌ Analysis Error</h2>',
            "</div>",
            '<div class="report__body">',
            f"<p><strong>Error:</strong> {message}</p>",
        ]

        if help_text:
            parts.append(
                f"<p><strong>Help:</strong> {html.escape(str(help_text))}</p>"
            )
        if found_columns and isinstance(found_columns, list):
            safe_cols = ", ".join(html.escape(str(c)) for c in found_columns)
            parts.append(f"<p><strong>Found columns:</strong> {safe_cols}</p>")

        parts.extend(["</div>", "</div>"])
        return "".join(parts)

    summary = result.get("summary") if isinstance(result.get("summary"), dict) else None
    recommendations = result.get("recommendations")
    daily_kpis = result.get("daily_kpis")
    ai_analysis = result.get("ai_analysis")

    if not (summary or recommendations or daily_kpis or ai_analysis):
        return (
            result.get("business_report_html")
            or result.get("business_report")
            or _ensure_html(str(result))
        )

    now_str = datetime.now().strftime("%m/%d/%Y, %I:%M:%S %p")
    file_info = result.get("file_info")
    period_analyzed = result.get("period_analyzed")

    parts: list[str] = [
        '<div class="report">',
        '<div class="report__header">',
        '<h2>📊 KPI Analysis Report</h2>',
        f'<div class="report__meta">Generated: {html.escape(now_str)}</div>',
    ]
    if file_info:
        file_info_safe = html.escape(str(file_info))
        period_safe = html.escape(str(period_analyzed or "N/A"))
        parts.append(
            f'<div class="report__meta">File: {file_info_safe} | Period: {period_safe}</div>'
        )
    parts.extend(["</div>", '<div class="report__body">'])

    # Summary KPI Grid
    if summary:
        parts.append(
            '<h3 style="color: #667eea; margin-bottom: 1rem;">📈 Summary Metrics</h3>'
            '<div class="kpi-grid">'
        )

        def _kpi_card(value_html: str, label: str, status_html: str | None = None) -> str:
            status = status_html or ""
            return (
                '<div class="kpi-card">'
                f'<div class="kpi-value">{value_html}</div>'
                f'<div class="kpi-label">{html.escape(label)}</div>'
                f"{status}"  # already contains safe markup
                "</div>"
            )

        if summary.get("total_sales"):
            parts.append(_kpi_card(html.escape(str(summary["total_sales"])), "Total Sales"))

        def _status_span(status: str, text: str) -> str:
            return f'<span class="kpi-status {status}">{html.escape(text)}</span>'

        if summary.get("avg_labor_percent"):
            labor_val = float(str(summary["avg_labor_percent"]).replace("%", "") or 0)
            status = "good" if labor_val <= 30 else "warning" if labor_val <= 35 else "alert"
            parts.append(
                _kpi_card(
                    html.escape(str(summary["avg_labor_percent"])),
                    "Avg Labor Cost",
                    _status_span(
                        status,
                        "✓ Good" if status == "good" else "⚠ Watch" if status == "warning" else "⚠ Alert",
                    ),
                )
            )

        if summary.get("avg_food_percent"):
            food_val = float(str(summary["avg_food_percent"]).replace("%", "") or 0)
            status = "good" if food_val <= 30 else "warning" if food_val <= 35 else "alert"
            parts.append(
                _kpi_card(
                    html.escape(str(summary["avg_food_percent"])),
                    "Avg Food Cost",
                    _status_span(
                        status,
                        "✓ Good" if status == "good" else "⚠ Watch" if status == "warning" else "⚠ Alert",
                    ),
                )
            )

        if summary.get("avg_prime_percent"):
            prime_val = float(str(summary["avg_prime_percent"]).replace("%", "") or 0)
            status = "good" if prime_val <= 60 else "warning" if prime_val <= 65 else "alert"
            parts.append(
                _kpi_card(
                    html.escape(str(summary["avg_prime_percent"])),
                    "Avg Prime Cost",
                    _status_span(
                        status,
                        "✓ Good" if status == "good" else "⚠ Watch" if status == "warning" else "⚠ Alert",
                    ),
                )
            )

        if summary.get("avg_sales_per_hour"):
            parts.append(
                _kpi_card(
                    html.escape(str(summary["avg_sales_per_hour"])),
                    "Avg Sales/Hour",
                )
            )

        if summary.get("trend"):
            trend = str(summary["trend"]).lower()
            trend_icon = "📈" if trend == "improving" else "📉" if trend == "declining" else "➡️"
            trend_status = "good" if trend == "improving" else "alert" if trend == "declining" else "warning"
            label = trend[:1].upper() + trend[1:] if trend else "N/A"
            parts.append(
                _kpi_card(
                    f"{trend_icon} {html.escape(label)}",
                    "Performance Trend",
                    _status_span(
                        trend_status,
                        "✓ Positive" if trend == "improving" else "⚠ Negative" if trend == "declining" else "○ Stable",
                    ),
                )
            )

        parts.append("</div>")
    else:
        parts.append('<p style="color: #888;">No summary data available</p>')

    # Recommendations
    if isinstance(recommendations, list) and recommendations:
        parts.append(
            '<h3 style="color: #667eea; margin: 1.5rem 0 1rem;">💡 Strategic Recommendations</h3>'
        )
        parts.append('<div class="recommendations-grid" style="display: grid; gap: 1rem;">')
        for rec in recommendations:
            if not isinstance(rec, dict):
                continue
            priority = str(rec.get("priority") or "").strip() or "Medium"
            priority_class = (
                "alert"
                if priority == "Critical"
                else "warning"
                if priority == "High"
                else "good"
            )
            border_color = (
                "#ef4444" if priority_class == "alert" else "#f59e0b" if priority_class == "warning" else "#10b981"
            )
            category = html.escape(str(rec.get("category") or "Recommendation"))
            action = html.escape(str(rec.get("action") or ""))
            impact = html.escape(str(rec.get("impact") or ""))

            parts.append(
                f'<div style="background: rgba(102, 126, 234, 0.1); border-radius: 0.5rem; padding: 1rem; border-left: 4px solid {border_color};">'
                '<div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.5rem;">'
                f'<strong style="color: #667eea;">{category}</strong>'
                f'<span class="kpi-status {priority_class}">{html.escape(priority)}</span>'
                "</div>"
                f'<p style="margin: 0.5rem 0; color: var(--text-primary);">{action}</p>'
                f'<p style="margin: 0; font-size: 0.875rem; color: var(--text-secondary);"><em>Impact: {impact}</em></p>'
                "</div>"
            )
        parts.append("</div>")

    # Daily KPIs Table
    if isinstance(daily_kpis, list) and daily_kpis:
        parts.append(
            f'<h3 style="color: #667eea; margin: 1.5rem 0 1rem;">📅 Daily Performance (Last {len(daily_kpis)} Days)</h3>'
        )
        parts.append(
            '<div style="overflow-x: auto;">'
            '<table style="width: 100%; border-collapse: collapse; font-size: 0.875rem;">'
            '<thead><tr style="background: linear-gradient(135deg, #667eea, #764ba2); color: white;">'
            '<th style="padding: 0.75rem; text-align: left;">Date</th>'
            '<th style="padding: 0.75rem; text-align: right;">Sales</th>'
            '<th style="padding: 0.75rem; text-align: right;">Labor %</th>'
            '<th style="padding: 0.75rem; text-align: right;">Food %</th>'
            '<th style="padding: 0.75rem; text-align: right;">Prime %</th>'
            '<th style="padding: 0.75rem; text-align: right;">Sales/Hour</th>'
            "</tr></thead><tbody>"
        )

        def _pct_status(value: float, good: float, warn: float) -> str:
            return "good" if value <= good else "warning" if value <= warn else "alert"

        for idx, day in enumerate(daily_kpis):
            if not isinstance(day, dict):
                continue
            row_bg = "rgba(102, 126, 234, 0.05)" if idx % 2 == 0 else "transparent"
            date_val = html.escape(str(day.get("date") or "N/A"))
            sales_val = day.get("sales")
            try:
                sales_num = float(sales_val) if sales_val is not None else None
            except Exception:
                sales_num = None
            sales_str = f"${sales_num:,.0f}" if isinstance(sales_num, (int, float)) else "N/A"

            def _fmt_pct(key: str) -> tuple[str, float | None]:
                raw = day.get(key)
                try:
                    return (f"{float(raw):.1f}%", float(raw))
                except Exception:
                    return ("N/A", None)

            labor_str, labor_num = _fmt_pct("labor_percent")
            food_str, food_num = _fmt_pct("food_percent")
            prime_str, prime_num = _fmt_pct("prime_percent")

            sph_raw = day.get("sales_per_hour")
            try:
                sph = float(sph_raw)
                sph_str = f"${sph:.2f}"
            except Exception:
                sph_str = "N/A"

            labor_class = _pct_status(labor_num, 30, 35) if labor_num is not None else "warning"
            food_class = _pct_status(food_num, 30, 35) if food_num is not None else "warning"
            prime_class = _pct_status(prime_num, 60, 65) if prime_num is not None else "warning"

            parts.append(
                f'<tr style="background: {row_bg}; border-bottom: 1px solid rgba(102, 126, 234, 0.1);">'
                f'<td style="padding: 0.75rem;">{date_val}</td>'
                f'<td style="padding: 0.75rem; text-align: right;">{sales_str}</td>'
                f'<td style="padding: 0.75rem; text-align: right;"><span class="kpi-status {labor_class}">{html.escape(labor_str)}</span></td>'
                f'<td style="padding: 0.75rem; text-align: right;"><span class="kpi-status {food_class}">{html.escape(food_str)}</span></td>'
                f'<td style="padding: 0.75rem; text-align: right;"><span class="kpi-status {prime_class}">{html.escape(prime_str)}</span></td>'
                f'<td style="padding: 0.75rem; text-align: right;">{html.escape(sph_str)}</td>'
                "</tr>"
            )

        parts.append("</tbody></table></div>")

    # AI Analysis Section
    if ai_analysis:
        parts.append(
            '<h3 style="color: #667eea; margin: 1.5rem 0 1rem;">🤖 AI-Powered Analysis</h3>'
            '<div style="background: linear-gradient(135deg, rgba(102, 126, 234, 0.1), rgba(118, 75, 162, 0.1)); border-radius: 0.75rem; padding: 1.5rem; border: 1px solid rgba(102, 126, 234, 0.2);">'
        )

        ai_content = html.escape(str(ai_analysis))
        ai_content = re.sub(
            r"\*\*(.+?)\*\*",
            r'<strong style="color: #667eea;">\1</strong>',
            ai_content,
            flags=re.DOTALL,
        )
        ai_content = ai_content.replace(
            "\n\n",
            '</p><p style="margin: 1rem 0; line-height: 1.6;">',
        )
        ai_content = ai_content.replace(
            "\n- ",
            '</p><li style="margin-left: 1.5rem; padding: 0.25rem 0;">',
        )
        ai_content = re.sub(
            r"\n\d+\. ",
            '</p><li style="margin-left: 1.5rem; padding: 0.25rem 0;">',
            ai_content,
        )

        parts.append(
            f'<div style="color: var(--text-primary); line-height: 1.6;"><p style="margin: 0 0 1rem 0;">{ai_content}</p></div>'
            "</div>"
        )

    parts.extend(["</div>", "</div>"])
    return "".join(parts)


def _error_payload(*, code: str, message: str, details=None, trace_id: str | None = None):
    payload = {"error": {"code": code, "message": message}}
    if details is not None:
        payload["error"]["details"] = details
    if trace_id:
        payload["error"]["trace_id"] = trace_id
    return payload


def _ensure_html(text_or_html: str) -> str:
    if not isinstance(text_or_html, str):
        text_or_html = str(text_or_html)
    candidate = text_or_html.strip()
    if not candidate:
        return "<div>No analysis returned.</div>"

    # Heuristic: if it already looks like HTML, pass through.
    if "<" in candidate and ">" in candidate:
        return candidate

    return f"<div><pre style=\"white-space:pre-wrap\">{html.escape(candidate)}</pre></div>"


@method_decorator(csrf_exempt, name="dispatch")
class KpiChatAPIView(APIView):
    authentication_classes: list = []
    permission_classes = [AllowAny]
    parser_classes = [JSONParser]

    def post(self, request, *args, **kwargs):
        serializer = KpiChatRequestSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                _error_payload(
                    code="VALIDATION_ERROR",
                    message="Invalid request body.",
                    details=serializer.errors,
                ),
                status=status.HTTP_400_BAD_REQUEST,
            )

        message: str = serializer.validated_data["message"]

        try:
            # Prefer KPI-specific handler to preserve existing KPI calculation logic.
            from apps.chat_assistant.openai_utils import handle_kpi_analysis, chat_with_gpt

            result = handle_kpi_analysis(message)
            if result is None:
                result = chat_with_gpt(message, context="kpi")

            return Response({"html_response": _ensure_html(result)}, status=status.HTTP_200_OK)
        except Exception as exc:
            trace_id = str(uuid4())
            logger.exception("KPI chat API failed trace_id=%s: %s", trace_id, exc)
            return Response(
                _error_payload(
                    code="INTERNAL_ERROR",
                    message="Server error while generating KPI analysis.",
                    trace_id=trace_id,
                ),
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


@method_decorator(csrf_exempt, name="dispatch")
class KpiUploadAPIView(APIView):
    authentication_classes: list = []
    permission_classes = [AllowAny]
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request, *args, **kwargs):
        serializer = KpiUploadRequestSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                _error_payload(
                    code="VALIDATION_ERROR",
                    message="Invalid upload payload.",
                    details=serializer.errors,
                ),
                status=status.HTTP_400_BAD_REQUEST,
            )

        required_csv = serializer.validated_data["required_csv"]
        optional_csv = serializer.validated_data.get("optional_csv")

        try:
            from backend.consulting_services.kpi.kpi_utils import process_kpi_csv_data

            required_result = process_kpi_csv_data(required_csv)
            required_html = (
                _format_kpi_csv_report_html(required_result)
                if isinstance(required_result, dict)
                else _ensure_html(str(required_result))
            )

            combined_html_parts = [
                "<div>",
                "<h2>KPI Analysis (CSV)</h2>",
                _ensure_html(required_html),
            ]

            if optional_csv is not None:
                optional_result = process_kpi_csv_data(optional_csv)
                optional_html = (
                    _format_kpi_csv_report_html(optional_result)
                    if isinstance(optional_result, dict)
                    else _ensure_html(str(optional_result))
                )

                combined_html_parts.extend(
                    [
                        "<hr />",
                        "<h2>Optional KPI Dataset</h2>",
                        _ensure_html(optional_html),
                    ]
                )

            combined_html_parts.append("</div>")
            return Response(
                {"html_response": "\n".join(combined_html_parts)},
                status=status.HTTP_200_OK,
            )
        except Exception as exc:
            trace_id = str(uuid4())
            logger.exception("KPI upload API failed trace_id=%s: %s", trace_id, exc)
            return Response(
                _error_payload(
                    code="INTERNAL_ERROR",
                    message="Server error while processing KPI CSV upload.",
                    trace_id=trace_id,
                ),
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
