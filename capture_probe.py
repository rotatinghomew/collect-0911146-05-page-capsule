from playwright.sync_api import sync_playwright
from assets import AssetStore


def inspect_page(url, directory):
    store = AssetStore(directory)
    with sync_playwright() as runtime:
        browser = runtime.chromium.launch(args=['--no-sandbox'])
        try:
            page = browser.new_page()
            response = page.goto(url)
            page.locator('[data-ready="yes"]').wait_for()
            record = store.capture(response.url, response.body(), response.status,
                                   response.headers.get('content-type', 'application/octet-stream'))
            return {'title': page.title(), 'visible': page.locator('main').inner_text(),
                    'frames': len(page.frames), 'top_response': record}
        finally:
            browser.close()
