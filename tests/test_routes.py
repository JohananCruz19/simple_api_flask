from app import create_app
def test_ping():
    c = create_app().test_client()
    r = c.get('/api/ping')
    assert r.json['status'] == 'ok'
