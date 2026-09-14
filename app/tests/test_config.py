"""Тесты конфигурации и DTO: секреты вынесены из кода, маппинги корректны."""
from __future__ import annotations

import os

import config
from core.analyzers.dto import AnalyzerResult, VulnerabilityDTO


class TestConfigNoSecrets:
    def test_no_hardcoded_secrets_in_source(self):
        """В config.py не должно быть старых реальных значений."""
        path = os.path.join(os.path.dirname(config.__file__), "config.py")
        src = open(path, encoding="utf-8").read()
        assert "45a0a5d595" not in src          # старый SECRET_KEY
        assert '"123456"' not in src            # старый DB_PASS

    def test_secret_key_has_env_or_dev_default(self):
        assert config.SECRET_KEY != "45a0a5d595c54f5bc76f1e408b80fe503922af19d2"
        assert isinstance(config.SECRET_KEY, str) and config.SECRET_KEY

    def test_db_pass_empty_by_default(self):
        # Без env пароль БД должен быть пустым, а не захардкоженным.
        assert config.DB_PASS == ""

    def test_cors_origins_is_list(self):
        assert isinstance(config.CORS_ORIGINS, list)
        assert "http://localhost" in config.CORS_ORIGINS


class TestDTO:
    def test_to_orm_dict_maps_cwe(self):
        v = VulnerabilityDTO(
            name="x", description="d", vuln_type=2, severity=3,
            url_path="/", cwe_id="CWE-79",
        )
        d = v.to_orm_dict()
        assert d["cwe_id"] == "CWE-79"
        assert d["type"] == 2
        assert d["severity"] == 3

    def test_analyzer_result_get_by_severity(self):
        r = AnalyzerResult(analyzer_name="test")
        r.vulnerabilities = [
            VulnerabilityDTO(name="a", description="", vuln_type=1, severity=4, url_path="/", cwe_id=""),
            VulnerabilityDTO(name="b", description="", vuln_type=1, severity=1, url_path="/", cwe_id=""),
        ]
        assert len(r.get_by_severity(4)) == 1
        assert len(r.get_by_severity(1)) == 1
        assert len(r.get_by_severity(2)) == 0
