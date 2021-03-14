from io import BytesIO

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

def test_post_memo_with_img(client, memo_data):
    data = memo_data.copy()
    data['linked_image'] = (
        BytesIO(b'dummy'),
        '1234567890qweasdzxc.jpg'
    )
    r = client.post(
        '/api/memos',
        data=data
    )
    assert r.status_code == 201
    assert r.json.get('linked_image') is not None

def test_put_memo_with_img(client, memo_data):
    r = client.post(
        '/api/memos',
        data=memo_data
    )
    assert r.status_code == 201
    memo_id = r.json['id']
    data = {
        'linked_image': (
            BytesIO(b'dummy'),
            '1234567890qweasdzxc.jpg'
        )
    }
    r = client.put(
        f'/api/memos/{memo_id}',
        data=data
    )
    assert r.status_code == 200
    assert r.json.get('linked_image') is not None

def test_delete_memos_img(client, memo_data):
    data = memo_data.copy()
    data['linked_image'] = (
        BytesIO(b'dummy'),
        '1234567890qweasdzxc.jpg'
    )
    r = client.post(
        '/api/memos',
        data=data
    )
    assert r.status_code == 201
    assert r.json.get('linked_image') is not None
    memo_id = r.json['id']

    r = client.delete(
        f'/api/memos/{memo_id}/image',
    )
    assert r.status_code == 204
    r = client.get(
        f'/api/memos/{memo_id}',
        follow_redirects=True
    )
    assert r.json.get('linked_image') is None

def test_put_memo_status_is_deleted(client):
    r = client.get(
        '/api/memos?is_deleted=false',
        follow_redirects=True
    )
    assert r.status_code == 200
    assert r.json[0].get('is_deleted') == False

    r = client.put(
        f'/api/memos/{r.json[0]["id"]}',
        data={
            'is_deleted': True
        }
    )
    assert r.status_code == 200
    assert r.json.get('is_deleted') == True

def test_post_memo_status_is_deleted(client, memo_data):
    data = memo_data.copy()
    data['is_deleted'] = True
    r = client.post(
        '/api/memos',
        data=data
    )
    assert r.status_code == 201
    assert r.json.get('is_deleted') == True

def test_get_memo_status_is_deleted(client):
    r = client.get(
        '/api/memos?is_deleted=true',
        follow_redirects=True
    )
    assert r.status_code == 200
    assert len(r.json) >= 1
    assert r.json[0].get('is_deleted') == True

def test_post_memo_with_labels(client, memo_data):
    new_data = memo_data.copy()
    new_data['labels'] = 'test,'

    r = client.post(
        '/api/memos',
        data=new_data
    )
    assert r.status_code == 201
    assert len(r.json.get('labels', [])) == 1
    assert r.json.get('labels', [])[0]['content'] == 'test'


def test_put_memo_with_labels(client, memo_data):
    r = client.post(
        '/api/memos',
        data=memo_data
    )
    assert r.status_code == 201
    assert len(r.json.get('labels', [])) == 0

    r = client.put(
        f'/api/memos/{r.json["id"]}',
        data={
            'labels': 'test,'
        }
    )

    assert r.status_code == 200
    assert len(r.json.get('labels', [])) == 1
    assert r.json.get('labels', [])[0]['content'] == 'test'

def test_get_memo_with_labels(client):
    r = client.get(
        '/api/memos?label=1',
        follow_redirects=True
    )
    assert r.status_code == 200
    assert len(r.json) >= 1
    assert r.json[0]['labels'][0]['content'] == 'test'
