from fastapi.testclient import TestClient

from lingualoop import main


def test_web_page_and_stylesheet_are_served(monkeypatch, tmp_path) -> None:
    database_file = tmp_path / "web-test.sqlite3"
    monkeypatch.setenv("LINGUALOOP_DB_PATH", str(database_file))

    with TestClient(main.app) as client:
        page = client.get("/")
        stylesheet = client.get("/static/styles.css")

    assert page.status_code == 200
    assert "<h1>LinguaLoop</h1>" in page.text
    assert 'href="/static/styles.css"' in page.text

    assert stylesheet.status_code == 200
    assert "font-family" in stylesheet.text