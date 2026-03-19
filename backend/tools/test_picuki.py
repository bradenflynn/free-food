import asyncio
from playwright.async_api import async_playwright

async def run():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.goto("https://www.picuki.com/profile/usdbas", wait_until="networkidle")
        await page.wait_for_timeout(3000)
        await page.screenshot(path="debug_picuki.jpg")
        posts = await page.query_selector_all('ul.box-photos > li img')
        for i, post in enumerate(posts[:3]):
            url = await post.get_attribute('src')
            print(f"Picuki post {i}: {url}")
        await browser.close()
asyncio.run(run())
