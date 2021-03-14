def test_get_labels(client):
    r =  client.get(
        "/api/labels",
        follow_redirects=True
    )
    assert r.status_code == 200
    assert r.json == []

def test_post_label(client):
    r =  client.post(
        "/api/labels",
        data={
            "content": "label"
        }
    )
    assert r.status_code == 201
    assert r.json.get('content') == "label"

def test_delete_label(client):
    r =  client.delete(
        "/api/labels/1",
    )
    assert r.status_code == 204
    r =  client.get(
        "/api/labels",
        follow_redirects=True
    )
    assert r.status_code == 200
    assert r.json == []
