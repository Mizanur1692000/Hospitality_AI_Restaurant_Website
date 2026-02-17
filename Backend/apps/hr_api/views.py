from __future__ import annotations

import html
import logging
import re
from uuid import uuid4

from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.parsers import FormParser, JSONParser, MultiPartParser
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import HrChatRequestSerializer, HrUploadRequestSerializer

logger = logging.getLogger(__name__)


PERCENT_KEYS = {
    "turnover_rate",
    "industry_average",
    "customer_satisfaction",
    "sales_performance",
    "efficiency_score",
    "attendance_rate",
    "customer_satisfaction_target",
    "sales_performance_target",
    "efficiency_target",
    "attendance_target",
}


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

    if "<" in candidate and ">" in candidate:
        return candidate

    return f"<div><pre style=\"white-space:pre-wrap\">{html.escape(candidate)}</pre></div>"


def _snake_key(key: str) -> str:
    key = key.strip().lower()
    key = re.sub(r"[^a-z0-9_\s]", "", key)
    key = re.sub(r"\s+", "_", key)
    key = re.sub(r"_+", "_", key)
    return key.strip("_")


def _coerce_scalar(value: str):
    raw = value.strip()
    if not raw:
        return ""

    lowered = raw.lower()
    if lowered in {"true", "false"}:
        return lowered == "true"

    # Remove currency/percent/commas for numeric parsing.
    numeric_candidate = raw.replace(",", "")
    numeric_candidate = re.sub(r"^\$", "", numeric_candidate)
    numeric_candidate = numeric_candidate.replace("$", "")
    numeric_candidate = numeric_candidate.replace("%", "")

    try:
        if re.fullmatch(r"-?\d+", numeric_candidate):
            return int(numeric_candidate)
        if re.fullmatch(r"-?\d*\.\d+", numeric_candidate) or re.fullmatch(
            r"-?\d+\.\d+", numeric_candidate
        ):
            return float(numeric_candidate)
    except Exception:
        pass

    return raw


def _parse_kv_message(message: str) -> dict:
    # The backend dashboard sample prompts start with "<topic> sample:".
    # Strip that prefix so "turnover_rate: ..." becomes a top-level pair.
    candidate = message
    sample_match = re.search(r"\bsample\s*:\s*", candidate, flags=re.IGNORECASE)
    if sample_match:
        candidate = candidate[sample_match.end() :]

    # Accept both “key: value, key2: value2” and “key: value\nkey2: value2”.
    params: dict = {}
    for match in re.finditer(
        r"(?P<key>[A-Za-z_][A-Za-z0-9_ ]*?)\s*:\s*(?P<value>[^,\n]+)",
        candidate,
    ):
        key = _snake_key(match.group("key"))
        value = _coerce_scalar(match.group("value"))
        if key:
            params[key] = value

    # Normalize common aliases
    if "industry_avg" in params and "industry_average" not in params:
        params["industry_average"] = params.pop("industry_avg")
    if "employee" in params and "employee_name" not in params:
        params["employee_name"] = params.pop("employee")
    if "employee_name" not in params and "employee" in message.lower() and "name:" in message.lower():
        # no-op; handled by KV parser
        pass

    # Convert ratio values (0-1) into percent (0-100) for known percent keys.
    for key in list(params.keys()):
        if key not in PERCENT_KEYS:
            continue
        val = params.get(key)
        if isinstance(val, (int, float)) and 0 <= float(val) <= 1:
            params[key] = float(val) * 100

    return params


def _format_hr_dashboard_like_html(*, subtask: str, result: dict) -> str:
    """Mimic the backend dashboard `formatHRResponse()` HTML structure."""
    focus_areas = {
        "staff_retention": {
            "title": "Staff Retention",
            "items": [
                "Turnover analysis",
                "Retention strategies",
                "Cost impact assessment",
            ],
        },
        "labor_scheduling": {
            "title": "Labor Scheduling",
            "items": [
                "Shift optimization",
                "Peak hour coverage",
                "Overtime management",
            ],
        },
        "performance_management": {
            "title": "Training Programs",
            "items": [
                "Onboarding optimization",
                "Skill development",
                "Performance tracking",
            ],
        },
    }

    data = result.get("data", {}) if isinstance(result.get("data"), dict) else {}

    summary: dict[str, object] = {}
    if subtask == "staff_retention":
        for k in [
            "turnover_rate",
            "retention_rate",
            "industry_average",
            "vs_industry",
            "risk_level",
            "estimated_annual_cost",
        ]:
            if k in data:
                summary[k] = data[k]
    elif subtask == "labor_scheduling":
        for k in [
            "total_sales",
            "labor_hours",
            "hourly_rate",
            "total_labor_cost",
            "sales_per_hour",
            "labor_percent",
            "peak_hours",
            "off_peak_hours",
        ]:
            if k in data:
                summary[k] = data[k]
    else:
        for k in [
            "overall_score",
            "customer_satisfaction",
            "sales_performance",
            "efficiency_score",
            "attendance_rate",
            "performance_rating",
        ]:
            if k in data:
                summary[k] = data[k]

    report_html = data.get("business_report_html") or data.get("business_report")
    report_html = _ensure_html(str(report_html)) if report_html is not None else ""

    html_parts: list[str] = []

    focus = focus_areas.get(subtask)
    if focus:
        html_parts.append(f"<strong>🎯 {html.escape(str(focus['title']))} Focus Areas:</strong><br>")
        items = focus.get("items") or []
        html_parts.append("<ul>")
        for item in items:
            html_parts.append(f"<li>{html.escape(str(item))}</li>")
        html_parts.append("</ul>")

    if summary:
        html_parts.append("<strong>📊 Analysis Summary:</strong><br>")
        for key, value in summary.items():
            label = " ".join(word[:1].upper() + word[1:] for word in str(key).split("_"))
            if isinstance(value, (int, float)):
                value_str = f"{value:,.2f}" if isinstance(value, float) else f"{value:,}"
            else:
                value_str = html.escape(str(value))
            html_parts.append(f"• {html.escape(label)}: {value_str}<br>")
        html_parts.append("<br>")

    if report_html:
        html_parts.append(f"<strong>📋 Business Report:</strong><br>{report_html}")

    return "".join(html_parts) or _ensure_html(str(result))


def _detect_subtask(message: str, params: dict) -> str:
    msg = message.lower()
    if any(k in params for k in ["turnover_rate", "industry_average", "retention_rate"]):
        return "staff_retention"
    if any(k in params for k in ["total_sales", "labor_hours", "hours_worked", "hourly_rate", "peak_hours"]):
        return "labor_scheduling"
    if any(
        k in params
        for k in [
            "customer_satisfaction",
            "sales_performance",
            "efficiency_score",
            "attendance_rate",
        ]
    ):
        return "performance_management"

    if any(w in msg for w in ["turnover", "retention", "attrition"]):
        return "staff_retention"
    if any(w in msg for w in ["schedule", "scheduling", "labor hours", "shift"]):
        return "labor_scheduling"
    if any(w in msg for w in ["training", "onboarding", "performance", "csat", "attendance"]):
        return "performance_management"

    return "performance_management"


def _format_hr_csv_report_html(result: dict) -> str:
    if not isinstance(result, dict):
        return _ensure_html(str(result))

    if result.get("status") == "error":
        message = html.escape(str(result.get("message") or "Unknown error"))
        help_text = result.get("help")
        found_columns = result.get("found_columns")

        parts = [
            '<div class="report">',
            '<div class="report__header" style="background: linear-gradient(135deg, #ef4444, #dc2626);">',
            "<h2>❌ HR CSV Analysis Error</h2>",
            "</div>",
            '<div class="report__body">',
            f"<p><strong>Error:</strong> {message}</p>",
        ]
        if help_text:
            parts.append(f"<p><strong>Help:</strong> {html.escape(str(help_text))}</p>")
        if found_columns and isinstance(found_columns, list):
            safe_cols = ", ".join(html.escape(str(c)) for c in found_columns)
            parts.append(f"<p><strong>Found columns:</strong> {safe_cols}</p>")
        parts.extend(["</div>", "</div>"])
        return "".join(parts)

    html_report = (
        result.get("business_report_html")
        or result.get("data", {}).get("business_report_html")
        or result.get("business_report")
        or result.get("data", {}).get("business_report")
    )
    return _ensure_html(str(html_report))


@method_decorator(csrf_exempt, name="dispatch")
class HrChatAPIView(APIView):
    authentication_classes: list = []
    permission_classes = [AllowAny]
    parser_classes = [JSONParser]

    def post(self, request, *args, **kwargs):
        serializer = HrChatRequestSerializer(data=request.data)
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
            params = _parse_kv_message(message)
            subtask = _detect_subtask(message, params)

            if not params:
                return Response(
                    {
                        "html_response": _ensure_html(
                            "Provide HR inputs as key:value pairs. Example: turnover_rate: 45, industry_average: 70"
                        )
                    },
                    status=status.HTTP_200_OK,
                )

            if subtask == "staff_retention":
                from backend.consulting_services.hr.staff_retention import run as run_retention

                result, code = run_retention(params)
            elif subtask == "labor_scheduling":
                from backend.consulting_services.hr.labor_scheduling import run as run_scheduling

                result, code = run_scheduling(params)
            else:
                from backend.consulting_services.hr.performance_management import (
                    run as run_performance,
                )

                result, code = run_performance(params)

            if isinstance(result, dict) and result.get("status") == "success":
                html_response = _format_hr_dashboard_like_html(subtask=subtask, result=result)
                return Response(
                    {"html_response": _ensure_html(str(html_response))},
                    status=status.HTTP_200_OK,
                )

            error_message = (
                result.get("error")
                if isinstance(result, dict)
                else "HR analysis failed."
            )
            return Response(
                _error_payload(
                    code="ANALYSIS_ERROR",
                    message=str(error_message or "HR analysis failed."),
                    details={"subtask": subtask},
                ),
                status=code if isinstance(code, int) else status.HTTP_400_BAD_REQUEST,
            )
        except Exception as exc:
            trace_id = str(uuid4())
            logger.exception("HR chat API failed trace_id=%s: %s", trace_id, exc)
            return Response(
                _error_payload(
                    code="INTERNAL_ERROR",
                    message="Server error while generating HR analysis.",
                    trace_id=trace_id,
                ),
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


@method_decorator(csrf_exempt, name="dispatch")
class HrUploadAPIView(APIView):
    authentication_classes: list = []
    permission_classes = [AllowAny]
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request, *args, **kwargs):
        serializer = HrUploadRequestSerializer(data=request.data)
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
            from backend.consulting_services.hr.hr_csv_processor import process_hr_csv_data

            required_result = process_hr_csv_data(required_csv, analysis_type="auto")
            required_html = _format_hr_csv_report_html(required_result)
            required_wrapped = _format_hr_dashboard_like_html(
                subtask=str(required_result.get("analysis_type") or "performance_management"),
                result={"data": {"business_report_html": required_html}, "status": "success"},
            )

            combined_html_parts = [
                "<div>",
                "<h2>HR Analysis (CSV)</h2>",
                _ensure_html(required_wrapped),
            ]

            if optional_csv is not None:
                optional_result = process_hr_csv_data(optional_csv, analysis_type="auto")
                optional_html = _format_hr_csv_report_html(optional_result)
                optional_wrapped = _format_hr_dashboard_like_html(
                    subtask=str(optional_result.get("analysis_type") or "performance_management"),
                    result={"data": {"business_report_html": optional_html}, "status": "success"},
                )
                combined_html_parts.extend(
                    [
                        "<hr />",
                        "<h2>Optional HR Dataset</h2>",
                        _ensure_html(optional_wrapped),
                    ]
                )

            combined_html_parts.append("</div>")
            return Response(
                {"html_response": "\n".join(combined_html_parts)},
                status=status.HTTP_200_OK,
            )
        except Exception as exc:
            trace_id = str(uuid4())
            logger.exception("HR upload API failed trace_id=%s: %s", trace_id, exc)
            return Response(
                _error_payload(
                    code="INTERNAL_ERROR",
                    message="Server error while processing HR CSV upload.",
                    trace_id=trace_id,
                ),
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
