import json
import tempfile
from fixture_course import AssetOrigin, Course
from local_http import serve
from capture_probe import inspect_page


def main():
    with tempfile.TemporaryDirectory() as directory, serve(AssetOrigin()) as assets:
        with serve(Course(assets)) as course:
            print(json.dumps(inspect_page(course, directory), ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
