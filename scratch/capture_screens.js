const http = require('http');
const fs = require('fs');
const path = require('path');
const { spawn } = require('child_process');

const EDGE_PATH = "C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe";
const OUT_DIR = path.join(__dirname, "..", "docs", "images");

if (!fs.existsSync(OUT_DIR)) {
  fs.mkdirSync(OUT_DIR, { recursive: true });
}

async function sleep(ms) {
  return new Promise(res => setTimeout(res, ms));
}

function getJson(url) {
  return new Promise((resolve, reject) => {
    http.get(url, res => {
      let data = '';
      res.on('data', chunk => data += chunk);
      res.on('end', () => resolve(JSON.parse(data)));
    }).on('error', reject);
  });
}

class CDPClient {
  constructor(wsUrl) {
    this.ws = new WebSocket(wsUrl);
    this.id = 0;
    this.callbacks = new Map();
  }

  async connect() {
    return new Promise(resolve => {
      this.ws.onopen = () => {
        this.ws.onmessage = (event) => {
          const msg = JSON.parse(event.data);
          if (msg.id && this.callbacks.has(msg.id)) {
            const cb = this.callbacks.get(msg.id);
            this.callbacks.delete(msg.id);
            cb(msg.result);
          }
        };
        resolve();
      };
    });
  }

  send(method, params = {}) {
    return new Promise((resolve) => {
      const id = ++this.id;
      this.callbacks.set(id, resolve);
      this.ws.send(JSON.stringify({ id, method, params }));
    });
  }

  async navigate(url) {
    await this.send("Page.navigate", { url });
    await sleep(2500);
  }

  async evaluate(expression) {
    return await this.send("Runtime.evaluate", { expression, returnByValue: true });
  }

  async screenshot(filePath) {
    const res = await this.send("Page.captureScreenshot", { format: "png", quality: 90 });
    if (res && res.data) {
      fs.writeFileSync(filePath, Buffer.from(res.data, 'base64'));
      console.log(`Saved screenshot: ${filePath}`);
    }
  }

  close() {
    this.ws.close();
  }
}

async function main() {
  const edgeProc = spawn(EDGE_PATH, [
    "--headless",
    "--disable-gpu",
    "--window-size=1280,820",
    "--remote-debugging-port=9333",
    "--user-data-dir=" + path.join(__dirname, "temp_profile")
  ]);

  await sleep(2500);

  try {
    const targets = await getJson("http://127.0.0.1:9333/json");
    let pageTarget = targets.find(t => t.type === 'page');
    if (!pageTarget) {
      await getJson("http://127.0.0.1:9333/json/new");
      const newTargets = await getJson("http://127.0.0.1:9333/json");
      pageTarget = newTargets.find(t => t.type === 'page');
    }

    const cdp = new CDPClient(pageTarget.webSocketDebuggerUrl);
    await cdp.connect();
    await cdp.send("Page.enable");

    console.log("Navigating to http://127.0.0.1:5173/");
    await cdp.navigate("http://127.0.0.1:5173/");

    // 1. Landing / Social Feed
    await cdp.screenshot(path.join(OUT_DIR, "fig4_1_about.png"));

    // 2. Open Auth Modal
    await cdp.evaluate(`
      const btn = Array.from(document.querySelectorAll('button')).find(b => b.textContent.includes('Login') || b.textContent.includes('Sign In'));
      if (btn) btn.click();
    `);
    await sleep(1000);
    await cdp.screenshot(path.join(OUT_DIR, "fig4_2_login.png"));

    // Close Auth modal
    await cdp.evaluate(`
      const closeBtn = document.querySelector('button[aria-label="Close"]') || Array.from(document.querySelectorAll('button')).find(b => b.textContent.includes('Cancel') || b.innerHTML.includes('svg'));
      if (closeBtn) closeBtn.click();
    `);
    await sleep(600);

    // 3. Feed page
    await cdp.screenshot(path.join(OUT_DIR, "fig4_3_feed.png"));

    // 4. Navigate to Live Check Tab
    await cdp.evaluate(`
      const tab = Array.from(document.querySelectorAll('button')).find(b => b.textContent.includes('Live Check') || b.textContent.includes('Toxicity Analyzer'));
      if (tab) tab.click();
    `);
    await sleep(1500);
    await cdp.screenshot(path.join(OUT_DIR, "fig4_4_live_check.png"));

    // 5. Enter text in Live Check and run inference
    await cdp.evaluate(`
      const input = document.querySelector('textarea') || document.querySelector('input[type="text"]');
      if (input) {
        input.value = "You are an absolute idiot and I hope you get banned right now!";
        input.dispatchEvent(new Event('input', { bubbles: true }));
      }
      const testBtn = Array.from(document.querySelectorAll('button')).find(b => b.textContent.includes('Analyze') || b.textContent.includes('Predict') || b.textContent.includes('Check'));
      if (testBtn) testBtn.click();
    `);
    await sleep(2000);
    await cdp.screenshot(path.join(OUT_DIR, "fig4_5_live_prediction.png"));

    // Set admin auth in localStorage to view Admin Dashboard
    await cdp.evaluate(`
      localStorage.setItem('toxic_user', JSON.stringify({
        id: 1,
        username: 'admin',
        email: 'admin@toxicguard.local',
        role: 'admin',
        token: 'admin-preview-token'
      }));
      window.location.reload();
    `);
    await sleep(2500);

    // 6. Admin Moderation Queue
    await cdp.evaluate(`
      const tab = Array.from(document.querySelectorAll('button')).find(b => b.textContent.includes('Admin') || b.textContent.includes('Dashboard'));
      if (tab) tab.click();
    `);
    await sleep(1500);
    await cdp.screenshot(path.join(OUT_DIR, "fig4_6_admin_queue.png"));

    // 7. Scroll down or click Analytics tab
    await cdp.evaluate(`
      const tab = Array.from(document.querySelectorAll('button')).find(b => b.textContent.includes('Analytics') || b.textContent.includes('Trends'));
      if (tab) tab.click();
      window.scrollBy(0, 300);
    `);
    await sleep(1500);
    await cdp.screenshot(path.join(OUT_DIR, "fig4_7_analytics_trends.png"));

    // 8. Scroll further down
    await cdp.evaluate(`
      window.scrollBy(0, 450);
    `);
    await sleep(1000);
    await cdp.screenshot(path.join(OUT_DIR, "fig4_8_analytics_distribution.png"));

    // 9. Model Performance Hub
    await cdp.evaluate(`
      window.scrollTo(0, 0);
      const tab = Array.from(document.querySelectorAll('button')).find(b => b.textContent.includes('Performance') || b.textContent.includes('Models'));
      if (tab) tab.click();
    `);
    await sleep(2000);
    await cdp.screenshot(path.join(OUT_DIR, "fig4_9_model_performance.png"));

    // 10. Swagger Docs
    await cdp.navigate("http://127.0.0.1:8000/docs");
    await sleep(2000);
    await cdp.screenshot(path.join(OUT_DIR, "fig4_10_swagger_docs.png"));

    console.log("All 10 UI screenshots captured successfully!");
    cdp.close();
  } catch (err) {
    console.error("Error capturing screenshots:", err);
  } finally {
    edgeProc.kill();
  }
}

main();
