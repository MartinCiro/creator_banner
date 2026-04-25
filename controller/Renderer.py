from playwright.sync_api import sync_playwright
from playwright.async_api import async_playwright


class Renderer:

    def __init__(self, config):
        self.config = config

    def _render(self, html: str):
        """Método privado que retorna la página renderizada"""
        playwright = sync_playwright().start()
        browser = playwright.chromium.launch()
        page = browser.new_page(
            viewport={
                "width": self.config.render.width,
                "height": self.config.render.height
            }
        )
        page.set_content(html)
        page.wait_for_timeout(300)
        return page, browser, playwright

    def html_to_png(self, html: str, output_path: str):
        """Guarda la imagen en disco"""
        page, browser, playwright = self._render(html)
        page.screenshot(path=output_path, full_page=True)
        browser.close()
        playwright.stop()

    def html_to_png_bytes(self, html: str) -> bytes:
        """Retorna los bytes de la imagen"""
        page, browser, playwright = self._render(html)
        screenshot_bytes = page.screenshot(full_page=True)
        browser.close()
        playwright.stop()
        return screenshot_bytes
    
    async def html_to_png_bytes_async(self, html: str) -> bytes:
        """Versión asíncrona para usar dentro de endpoints async"""
        async with async_playwright() as p:
            browser = await p.chromium.launch()
            page = await browser.new_page(
                viewport={
                    "width": self.config.render.width,
                    "height": self.config.render.height
                }
            )
            await page.set_content(html)
            await page.wait_for_timeout(300)
            screenshot_bytes = await page.screenshot(full_page=True)
            await browser.close()
            return screenshot_bytes