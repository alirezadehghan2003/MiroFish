import pytest

from app import create_app
from app.services.report_agent import ReportManager
from app.utils.security import (
    find_unsafe_id,
    host_without_port,
    is_host_allowed,
    is_loopback_host,
    is_safe_id,
    safe_id_path,
)


@pytest.mark.parametrize("value", ["proj_0123abcd4567", "sim-1", "report_x"])
def test_generated_style_ids_are_safe(value):
    assert is_safe_id(value)


@pytest.mark.parametrize(
    "value",
    ["", "..", ".", "../etc", "a/b", "/Users/me", "a\\b", "a b", "sim_1\n", "x" * 129, None, 5],
)
def test_path_like_ids_are_rejected(value):
    assert not is_safe_id(value)


def test_safe_id_path_stays_inside_base(tmp_path):
    assert safe_id_path(str(tmp_path), "sim_1", "state.json") == str(
        tmp_path / "sim_1" / "state.json"
    )
    with pytest.raises(ValueError):
        safe_id_path(str(tmp_path), "..")
    with pytest.raises(ValueError):
        safe_id_path(str(tmp_path), "/etc")


def test_find_unsafe_id_only_checks_path_fields():
    assert find_unsafe_id({"simulation_id": "../x"}) == "simulation_id"
    assert find_unsafe_id({"graph_id": "anything/at all"}) is None
    assert find_unsafe_id({"report_id": None}) is None
    assert find_unsafe_id(["not", "a", "mapping"]) is None
    assert find_unsafe_id(None) is None


def test_host_allowlist():
    allowed = ["localhost", "127.0.0.1", "::1"]
    assert host_without_port("localhost:5001") == "localhost"
    assert host_without_port("[::1]:5001") == "::1"
    assert is_host_allowed("LOCALHOST:3000", allowed)
    assert is_host_allowed("[::1]:5001", allowed)
    assert not is_host_allowed("attacker.example:5001", allowed)
    assert is_host_allowed("attacker.example", ["*"])


def test_loopback_detection():
    assert is_loopback_host("127.0.0.1")
    assert is_loopback_host("localhost")
    assert not is_loopback_host("0.0.0.0")


@pytest.fixture
def client(tmp_path, monkeypatch):
    monkeypatch.setattr(ReportManager, "REPORTS_DIR", str(tmp_path))
    app = create_app()
    app.config.update(TESTING=True)
    return app.test_client()


def test_foreign_host_header_is_rejected(client):
    assert client.get("/health").status_code == 200
    response = client.get("/health", headers={"Host": "attacker.example"})
    assert response.status_code == 403


def test_unsafe_ids_are_rejected_from_every_input(client):
    assert client.post(
        "/api/simulation/start", json={"simulation_id": "../../outside"}
    ).status_code == 400
    assert client.get(
        "/api/report/list", query_string={"simulation_id": "../x"}
    ).status_code == 400
    assert client.delete("/api/report/bad%20id").status_code == 400


def test_report_delete_cannot_escape_reports_dir(client, tmp_path, monkeypatch):
    reports_dir = tmp_path / "reports"
    reports_dir.mkdir()
    monkeypatch.setattr(ReportManager, "REPORTS_DIR", str(reports_dir))
    sentinel = tmp_path / "keep.txt"
    sentinel.write_text("keep")

    client.delete("/api/report/..")

    assert sentinel.exists()


def test_tracebacks_are_not_returned(client, monkeypatch):
    def boom(report_id):
        raise RuntimeError("internal failure")

    monkeypatch.setattr(ReportManager, "get_report", boom)
    response = client.get("/api/report/report_abc")

    assert response.status_code == 500
    assert response.json["error"] == "internal failure"
    assert "traceback" not in response.json


def test_cors_only_allows_local_frontend(client):
    preflight = {"Access-Control-Request-Method": "DELETE"}
    allowed = client.options(
        "/api/report/report_abc",
        headers={**preflight, "Origin": "http://localhost:3000"},
    )
    assert allowed.headers.get("Access-Control-Allow-Origin") == "http://localhost:3000"

    blocked = client.options(
        "/api/report/report_abc",
        headers={**preflight, "Origin": "https://attacker.example"},
    )
    assert "Access-Control-Allow-Origin" not in blocked.headers
