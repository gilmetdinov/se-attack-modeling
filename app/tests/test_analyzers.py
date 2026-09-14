"""Smoke-тесты анализаторов уязвимостей (логика детекта, без сети)."""
from __future__ import annotations

import pytest

from core.analyzers.dto import PayloadResult
from core.analyzers.sqli import SQLiAnalyzer
from core.analyzers.xss import XSSAnalyzer


def make_result(payload, body="", code=200, time=0.1):
    return PayloadResult(
        payload=payload,
        response_code=code,
        response_time=time,
        response_body=body,
        is_vulnerable=False,
    )


class TestSQLiAnalyzer:
    def test_payloads_non_empty(self):
        assert len(SQLiAnalyzer(site_map=None).get_payloads()) > 0

    def test_error_based_detection(self):
        a = SQLiAnalyzer(site_map=None)
        r = make_result("'", body="You have an error in your SQL syntax near '1")
        assert a.check_vulnerability(r) is True

    def test_time_based_detection(self):
        a = SQLiAnalyzer(site_map=None)
        r = make_result("' AND SLEEP(5)--", body="ok", time=5.5)
        assert a.check_vulnerability(r) is True

    def test_no_false_positive(self):
        a = SQLiAnalyzer(site_map=None)
        r = make_result("'", body="<html>hello world</html>")
        assert a.check_vulnerability(r) is False

    def test_create_vulnerability_cwe_and_severity(self):
        a = SQLiAnalyzer(site_map=None)
        r = make_result("'", body="SQL syntax error")
        v = a.create_vulnerability("http://x/", "id", "GET", r)
        assert v.cwe_id == "CWE-89"
        assert v.severity == 4  # SeverityEnum.CRITICAL


class TestXSSAnalyzer:
    def test_payloads_non_empty(self):
        assert len(XSSAnalyzer(site_map=None).get_payloads()) > 0

    def test_reflected_payload_detected(self):
        a = XSSAnalyzer(site_map=None)
        r = make_result(
            "<script>alert('XSS')</script>",
            body="<div><script>alert('XSS')</script></div>",
        )
        assert a.check_vulnerability(r) is True

    def test_no_reflection_no_vuln(self):
        a = XSSAnalyzer(site_map=None)
        r = make_result("<script>alert('XSS')</script>", body="<html>nothing here</html>")
        assert a.check_vulnerability(r) is False

    def test_create_vulnerability_script_is_critical(self):
        a = XSSAnalyzer(site_map=None)
        r = make_result("<script>x</script>", body="<script>x</script>")
        v = a.create_vulnerability("http://x/", "q", "GET", r)
        assert v.cwe_id == "CWE-79"
        assert v.severity == 4  # CRITICAL для <script>
