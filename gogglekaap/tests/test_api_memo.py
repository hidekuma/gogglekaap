def test_get_memo(client, memo_data):
    r = client.get(
        '/api/memos/1',
        follow_redirects=True
    )
    assert r.status_code == 200
    assert r.json['title'] == memo_data['title']

def test_get_memos(client):
    r = client.get(
        '/api/memos',
        follow_redirects=True
    )
    assert r.status_code == 200
    assert len(r.json) == 1

def test_post_memo(client, memo_data):
    r = client.post(
        '/api/memos',
        data=memo_data
    )
    assert r.status_code == 201
    r = client.get(
        '/api/memos',
        follow_redirects=True
    )
    assert r.status_code == 200
    assert len(r.json) == 2

def test_put_memo(client):
    new_data = {
        'title': 'new_title',
        'content': 'new_content'
    }
    r = client.put(
        '/api/memos/1',
        data=new_data
    )
    assert r.status_code == 200
    assert r.json['title'] == new_data['title']
    assert r.json['content'] == new_data['content']

def test_delete_memo(client):
    r = client.delete(
        '/api/memos/1'
    )
    assert r.status_code == 204
    r = client.get(
        '/api/memos',
        follow_redirects=True
    )
    assert r.status_code == 200
    assert len(r.json) == 1