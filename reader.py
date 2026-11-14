from local_http import Reply


class EvidenceView:
    def __init__(self, assets):
        self.assets = assets

    def handle(self, method, path, headers, body):
        if path == '/index':
            return Reply.json(self.assets.records())
        if path.startswith('/blob/'):
            try:
                return Reply(200, self.assets.evidence.get(path.removeprefix('/blob/')),
                             {'Content-Type': 'application/octet-stream'})
            except (ValueError, FileNotFoundError):
                return Reply(404)
        return Reply(404)
