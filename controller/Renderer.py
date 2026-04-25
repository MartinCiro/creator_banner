from playwright.async_api import async_playwright

from logging import basicConfig, getLogger, INFO

# Configurar logging
basicConfig(level=INFO)
logger = getLogger(__name__)

class Renderer:

    def __init__(self, config):
        self.config = config

    async def _render(self, html: str):
        """Método privado que retorna la página renderizada"""
        playwright = await async_playwright().start()
        browser = await playwright.chromium.launch()
        page = await browser.new_page(
            viewport={
                "width": self.config.render.width,
                "height": self.config.render.height
            }
        )
        page.set_content(html)
        page.wait_for_timeout(300)
        return page, browser, playwright

    async def html_to_png(self, html: str, output_path: str):
        """Guarda la imagen en disco"""
        page, browser, playwright = await self._render(html)
        await page.screenshot(path=output_path)
        await browser.close()
        await playwright.stop()

    async def html_to_png_bytes(self, html: str) -> bytes:
        """Retorna los bytes de la imagen"""
        page, browser, playwright = await self._render(html)
        screenshot_bytes = await page.screenshot()
        await browser.close()
        await playwright.stop()
        return screenshot_bytes
    
    async def html_to_png_bytes_async(self, html: str) -> bytes:
        async with async_playwright() as p:
            browser = await p.chromium.launch(
                headless=True,
                args=[
                    '--disable-gpu',              
                    '--no-sandbox',               
                    '--disable-dev-shm-usage',    
                    '--disable-setuid-sandbox',   
                    '--font-render-hinting=none', 
                    '--disable-font-subpixel-positioning',  
                    '--disable-lcd-text',         
                    '--disable-skia-runtime-opts',
                ]
            )

            page = await browser.new_page(
                viewport={
                    "width": self.config.render.width,   # 920
                    "height": self.config.render.height  # 380
                }
            )
            
            await page.set_content(html, wait_until='networkidle')
            
            try:
                await page.wait_for_function('document.fonts.ready', timeout=5000)
            except Exception:
                logger.warning("⚠️ document.fonts.ready timeout, continuando...")
            
            await page.wait_for_timeout(1000)
            
            screenshot_bytes = await page.screenshot(
                full_page=True,
                omit_background=False 
            )
            
            await browser.close()
            return screenshot_bytes

    async def html_to_png_async(self, html: str, output_path: str):
        async with async_playwright() as p:
            browser = await p.chromium.launch()
            page = await browser.new_page(
                viewport={
                    "width": self.config.render.width,
                    "height": self.config.render.height
                }
            )
            await page.set_content(html, wait_until='networkidle')
            try:
                await page.wait_for_selector('.titulo', state='visible', timeout=5000)
            except Exception as e:
                logger.warning(f"⚠️ .titulo no visible inmediatamente: {e}")
            await page.wait_for_timeout(300) 
            
            await page.screenshot(path=output_path)
            await browser.close()