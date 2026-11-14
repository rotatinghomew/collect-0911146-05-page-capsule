import json
from local_http import Reply


class AssetOrigin:
    def __init__(self):
        self.requests = []

    def handle(self, method, path, headers, body):
        self.requests.append((method, path))
        if path == '/shared/badge.svg':
            return Reply(200, b'<svg xmlns="http://www.w3.org/2000/svg" width="30" height="20"><rect width="30" height="20" fill="green"/></svg>',
                         {'Content-Type': 'image/svg+xml'})
        if path == '/frame':
            return Reply(200, b'<!doctype html><meta charset="utf-8"><h2>Frame source</h2><img src="/shared/badge.svg">',
                         {'Content-Type': 'text/html'})
        return Reply(404)


class Course:
    def __init__(self, asset_origin):
        self.asset_origin = asset_origin
        self.requests = []

    def handle(self, method, path, headers, body):
        self.requests.append((method, path, body))
        if path == '/':
            html = """<!doctype html><html lang="zh"><meta charset="utf-8"><title>授权课程</title>
            <link rel="stylesheet" href="/css/site.css"><main><h1>仓储课程</h1><p id="lesson">加载中</p>
            <img src="/badge"><iframe src="ASSET/frame" title="课程附件"></iframe></main>
            <script src="/course.js"></script></html>"""
            return Reply(200, html.replace('ASSET', self.asset_origin).encode(), {'Content-Type': 'text/html; charset=utf-8'})
        if path == '/css/site.css':
            return Reply(200, b'@import url("/css/theme.css"); main{background-image:url("../shared/badge.svg");} iframe{width:300px;height:100px}', {'Content-Type': 'text/css'})
        if path == '/css/theme.css':
            return Reply(200, b'h1{color:#235}', {'Content-Type': 'text/css'})
        if path == '/badge':
            return Reply(302, headers={'Location': '/shared/badge.svg'})
        if path == '/shared/badge.svg':
            return Reply(200, b'<svg xmlns="http://www.w3.org/2000/svg" width="30" height="20"><rect width="30" height="20" fill="blue"/></svg>', {'Content-Type': 'image/svg+xml'})
        if path == '/course.js':
            script = """fetch('/lesson', {method:'POST', headers:{'Content-Type':'application/json'}, body:JSON.stringify({lesson:'A'})})
            .then(response=>response.json()).then(value=>{document.querySelector('#lesson').textContent=value.text;document.querySelector('main').dataset.ready='yes';});"""
            return Reply(200, script.encode(), {'Content-Type': 'text/javascript'})
        if path == '/lesson' and method == 'POST':
            lesson = json.loads(body).get('lesson')
            return Reply.json({'text': '授权课程 ' + str(lesson)}, headers={'Set-Cookie': 'training-session=synthetic-private; HttpOnly; Path=/'})
        return Reply(404)
