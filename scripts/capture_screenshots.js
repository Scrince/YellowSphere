import { createReadStream } from 'node:fs';
import { mkdir } from 'node:fs/promises';
import { createServer } from 'node:http';
import { createRequire } from 'node:module';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const require = createRequire(import.meta.url);
const { chromium } = require(process.env.PLAYWRIGHT_PACKAGE || 'playwright');

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const OUT_DIR = path.join(ROOT, 'docs', 'screenshots');
const APP_FILE = 'YellowSphere.html';
const MNEMONIC = 'abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon about';

const MIME_TYPES = new Map([
  ['.html', 'text/html; charset=utf-8'],
  ['.js', 'text/javascript; charset=utf-8'],
  ['.css', 'text/css; charset=utf-8'],
  ['.png', 'image/png'],
  ['.ico', 'image/x-icon'],
]);

function startServer() {
  const server = createServer((request, response) => {
    const requestUrl = new URL(request.url || '/', 'http://127.0.0.1');
    const pathname = requestUrl.pathname === '/' ? `/${APP_FILE}` : requestUrl.pathname;
    const filePath = path.resolve(ROOT, `.${decodeURIComponent(pathname)}`);

    if (!filePath.startsWith(ROOT + path.sep)) {
      response.writeHead(403);
      response.end('Forbidden');
      return;
    }

    try {
      response.writeHead(200, {
        'Content-Type': MIME_TYPES.get(path.extname(filePath)) || 'application/octet-stream',
      });
      createReadStream(filePath).pipe(response);
    } catch {
      response.writeHead(404);
      response.end('Not found');
    }
  });

  return new Promise((resolve) => {
    server.listen(0, '127.0.0.1', () => {
      const address = server.address();
      resolve({ server, url: `http:
    });
  });
}

async function closeServer(server) {
  await new Promise((resolve, reject) => {
    server.close((error) => error ? reject(error) : resolve());
    server.closeIdleConnections?.();
    server.closeAllConnections?.();
  });
}

async function newPage(browser, url, theme = 'light') {
  const context = await browser.newContext({
    viewport: { width: 1440, height: 900 },
    deviceScaleFactor: 2,
    reducedMotion: 'reduce',
  });
  await context.addInitScript((themeMode) => {
    localStorage.setItem('yellowsphereTheme', themeMode);
    localStorage.setItem('yellowsphereVisibilityGrace', '1');
    localStorage.setItem('yellowsphereSessionTimeout', '0');
  }, theme);
  const page = await context.newPage();
  page.on('pageerror', (error) => {
    throw error;
  });
  await page.goto(url, { waitUntil: 'domcontentloaded' });
  await page.locator('#status').waitFor({ state: 'visible' });
  await page.addStyleTag({
    content: `
      *, *::before, *::after { animation-duration: 0s !important; transition-duration: 0s !important; caret-color: transparent !important; }
      body { overflow-anchor: none !important; }
    `,
  });
  return page;
}

async function setMnemonicState(page) {
  await page.locator('#mnemonic').fill(MNEMONIC);
  await page.locator('#count').fill('3');
  await page.locator('#validateBtn').click();
  await page.locator('#status').filter({ hasText: 'Mnemonic is valid BIP39' }).waitFor();
}

async function derive(page) {
  await page.locator('#deriveBtn').click();
  await page.locator('#status').filter({ hasText: 'Derivation complete.' }).waitFor({ timeout: 15000 });
}

async function capture(page, filename) {
  await page.screenshot({ path: path.join(OUT_DIR, filename), fullPage: false });
}

async function captureTheme(browser, url, theme, filename) {
  const page = await newPage(browser, url, theme);
  await setMnemonicState(page);
  await capture(page, filename);
  await page.context().close();
}

async function main() {
  await mkdir(OUT_DIR, { recursive: true });
  const { server, url } = await startServer();
  const browser = await chromium.launch();

  try {
    const mainPage = await newPage(browser, url, 'light');
    await setMnemonicState(mainPage);
    await capture(mainPage, 'yellowsphere-main-recovery.png');
    await capture(mainPage, 'yellowsphere-light.png');

    await derive(mainPage);
    await capture(mainPage, 'yellowsphere-derived-output.png');

    await mainPage.locator('#qrAddressesBtn').click();
    await mainPage.locator('#qrModal[open]').waitFor();
    await mainPage.locator('#qrAddressInput').fill('bc1qw508d6qejxtdg4y5r3zarvary0c5xw7kygt080');
    await mainPage.locator('#qrGenerateBtn').click();
    await mainPage.locator('#qrCanvas').waitFor({ state: 'visible' });
    await capture(mainPage, 'yellowsphere-qr-export.png');
    await mainPage.keyboard.press('Escape');

    await mainPage.locator('#settingsBtn').click();
    await mainPage.locator('#settingsDialog[open]').waitFor();
    await capture(mainPage, 'yellowsphere-settings.png');
    await mainPage.context().close();

    await captureTheme(browser, url, 'dark', 'yellowsphere-dark.png');
    await captureTheme(browser, url, 'dark-plus', 'yellowsphere-dark-plus.png');
    await captureTheme(browser, url, 'terminal', 'yellowsphere-terminal.png');
  } finally {
    await browser.close();
    await closeServer(server);
  }

  console.log(`Captured YellowSphere screenshots in ${OUT_DIR}`);
}

main().catch((error) => {
  console.error(error);
  process.exit(1);
});
