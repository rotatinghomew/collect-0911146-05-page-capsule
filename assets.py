from evidence import EvidenceStore


class AssetStore:
    def __init__(self, directory):
        self.evidence = EvidenceStore(directory)

    def capture(self, url, body, status, content_type):
        digest = self.evidence.put(body)
        record = {'kind': 'response', 'url': url, 'blob': digest,
                  'status': status, 'content_type': content_type}
        self.evidence.record(record)
        return record

    def records(self):
        return self.evidence.events()
