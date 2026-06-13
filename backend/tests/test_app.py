import pytest

from backend.app import app


class MockResponse:
    def __init__(self, status_code, json_data):
        self.status_code = status_code
        self._json = json_data

    def raise_for_status(self):
        if self.status_code >= 400:
            raise Exception('HTTP error')

    def json(self):
        return self._json


def test_no_city():
    client = app.test_client()
    r = client.get('/events')
    assert r.status_code == 400


def test_success(monkeypatch):
    sample = {
        '_embedded': {
            'events': [
                {
                    'id': '1',
                    'name': 'Test Event',
                    'dates': {'start': {'dateTime': '2026-06-13T20:00:00Z'}},
                    'url': 'http://example.com',
                    'images': [{'url': 'http://img'}],
                    '_embedded': {'venues': [{'name': 'Venue A'}]},
                }
            ]
        }
    }

    def mock_get(url, params=None, timeout=None):
        return MockResponse(200, sample)

    monkeypatch.setattr('backend.app.requests.get', mock_get)
    client = app.test_client()
    r = client.get('/events?city=Seattle')
    assert r.status_code == 200
    data = r.get_json()
    assert data['count'] == 1
    assert data['events'][0]['name'] == 'Test Event'


def test_upstream_error(monkeypatch):
    def mock_get(url, params=None, timeout=None):
        return MockResponse(500, {})

    monkeypatch.setattr('backend.app.requests.get', mock_get)
    client = app.test_client()
    r = client.get('/events?city=Seattle')
    assert r.status_code == 502
