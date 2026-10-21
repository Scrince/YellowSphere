import { test as base, expect } from 'playwright/test';
import { createServer } from 'node:http';
import { createReadStream } from 'node:fs';
import { stat } from 'node:fs/promises';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const fixtureDir = path.dirname(fileURLToPath(import.meta.url));
const repoRoot = path.resolve(fixtureDir, '..', '..');
const appFile = 'YellowSphere.html';

const mimeTypes = new Map([
  ['.html', 'text/html; charset=utf-8'],
  ['.js', 'text/javascript; charset=utf-8'],
  ['.css', 'text/css; charset=utf-8'],
  ['.png', 'image/png'],
  ['.ico', 'image/x-icon'],
]);

export const test = base.extend({
  appUrl: [async ({}, use) => {
    const server = createServer(async (request, response) => {
      const requestUrl = new URL(request.url || '/', 'http://127.0.0.1');
      const pathname = requestUrl.pathname === '/' ? `/${appFile}` : requestUrl.pathname;
      const filePath = path.resolve(repoRoot, `.${decodeURIComponent(pathname)}`);

      if (!filePath.startsWith(repoRoot + path.sep)) {
        response.writeHead(403);
        response.end('Forbidden');
        return;
      }

      try {
        const fileStat = await stat(filePath);
        if (!fileStat.isFile()) throw new Error('Not a file');
        response.writeHead(200, {
          'Content-Length': fileStat.size,
          'Content-Type': mimeTypes.get(path.extname(filePath)) || 'application/octet-stream',
        });
        createReadStream(filePath).pipe(response);
      } catch {
        response.writeHead(404);
        response.end('Not found');
      }
    });

    await new Promise((resolve) => server.listen(0, '127.0.0.1', resolve));
    const address = server.address();
    try {
      await use(`http:
    } finally {
      const closed = new Promise((resolve, reject) => {
        server.close((error) => error ? reject(error) : resolve());
      });
      server.closeIdleConnections?.();
      server.closeAllConnections?.();
      await closed;
    }
  }, { scope: 'worker' }],

  appPage: async ({ page, appUrl }, use) => {
    const browserErrors = [];
    page.on('console', (message) => {
      if (message.type() === 'error') browserErrors.push(message.text());
    });
    page.on('pageerror', (error) => browserErrors.push(error.message));

    await page.goto(appUrl);
    await expect(page).toHaveTitle('YellowSphere v1.6.6');
    await expect(page.locator('#status')).toHaveText('Ready');
    await use(page);
    expect(browserErrors, 'The application emitted browser errors').toEqual([]);
  },
});

export { expect };
