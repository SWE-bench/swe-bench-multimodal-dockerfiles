
FROM --platform=linux/amd64 ubuntu:20.04

ARG DEBIAN_FRONTEND=noninteractive

ENV TZ=Etc/UTC

RUN rm /bin/sh && ln -s /bin/bash /bin/sh
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    git \
    libssl-dev \
    software-properties-common \
    wget \
    gnupg \
    jq \
    ca-certificates \
    dbus \
    ffmpeg \
    imagemagick \
    unzip \
    && apt-get -y autoclean \
    && rm -rf /var/lib/apt/lists/*

ENV NVM_DIR /usr/local/nvm

RUN mkdir -p $NVM_DIR
RUN curl --silent -o- https://raw.githubusercontent.com/creationix/nvm/v0.39.3/install.sh | bash
RUN apt-get update && apt-get install -y \
    procps \
    xvfb x11-xkb-utils xfonts-100dpi xfonts-75dpi xfonts-scalable \
    xfonts-cyrillic x11-apps \
    libasound2 libatk-bridge2.0-0 libatk1.0-0 libcups2 libdrm2 \
    libgbm1 libgconf-2-4 libgdk-pixbuf2.0-0 libgtk-3-0 libnspr4 \
    libnss3 libpango-1.0-0 libpangocairo-1.0-0 libxcomposite1 \
    libxdamage1 libxfixes3 libxkbcommon0 libxrandr2 libxss1 libxshmfence1 libglu1 \
    libgl1-mesa-dri libegl1-mesa libxtst6 \
    fonts-ipafont-gothic fonts-wqy-zenhei fonts-thai-tlwg \
    fonts-khmeros fonts-kacst fonts-freefont-ttf \
    && apt-get -y autoclean \
    && rm -rf /var/lib/apt/lists/*

RUN mkdir -p /run/dbus

ENV DBUS_SESSION_BUS_ADDRESS="unix:path=/run/dbus/system_bus_socket"

RUN dbus-daemon --system --fork

ENV OPENSSL_CONF /etc/ssl

# Puppeteer 19.7+ caches its bundled Chromium in $PUPPETEER_CACHE_DIR (defaults
# to ~/.cache/puppeteer). Pin it to a shared, world-readable location so karma
# (running as chromeuser) can use the same binary that npm install (root)
# downloaded — without copying the cache across users.
ENV PUPPETEER_CACHE_DIR=/opt/puppeteer-cache
RUN mkdir -p /opt/puppeteer-cache && chmod 0777 /opt/puppeteer-cache

RUN useradd -m chromeuser

USER chromeuser

WORKDIR /home/chromeuser

USER root

ENV NODE_VERSION 21.6.2
ENV NODE_PATH $NVM_DIR/v$NODE_VERSION/lib/node_modules
ENV PATH $NVM_DIR/versions/node/v$NODE_VERSION/bin:$PATH

RUN <<EOF_cc508ad98ca6
#!/bin/bash
set -euxo pipefail
apt-get update
apt-get install -y python3 python3-pip xvfb x11-xkb-utils xfonts-100dpi xfonts-75dpi xfonts-scalable xfonts-cyrillic x11-apps libsass-dev sassc libsass-dev sassc libsass-dev sassc libsass-dev sassc libsass-dev sassc libsass-dev sassc libsass-dev sassc libsass-dev sassc
rm -rf /var/lib/apt/lists/*
export NODE_VERSION=21.6.2
source $NVM_DIR/nvm.sh
nvm install $NODE_VERSION
nvm alias default $NODE_VERSION
nvm use default
add-apt-repository ppa:deadsnakes/ppa
apt-get update
apt-get install -y python3.9
ln -sf /usr/bin/python3.9 /usr/bin/python
apt-get install -y python2
echo "export NODE_PATH=$NVM_DIR/v21.6.2/lib/node_modules" >> /etc/environment
echo "export PATH=$NVM_DIR/versions/node/v21.6.2/bin:$PATH" >> /etc/environment
source $NVM_DIR/nvm.sh && node -v
source $NVM_DIR/nvm.sh && npm -v
python -V
python2 -V
EOF_cc508ad98ca6


RUN <<EOF_8bd7452bf2c6
#!/bin/bash
set -euxo pipefail
git clone -o origin https://github.com/openlayers/openlayers /testbed
cd /testbed
git reset --hard 7a88544d0f02253088bedaf8c0adf3a73d24739b
git remote remove origin
git branch | grep -v '^\*' | xargs -r git branch -D || true
git tag -l | while read tag; do   git merge-base --is-ancestor "$tag" HEAD 2>/dev/null || git tag -d "$tag" >/dev/null; done
git reflog expire --expire=now --all
git gc --prune=now --aggressive
TARGET_EPOCH=$(git show -s --format=%ct 7a88544d0f02253088bedaf8c0adf3a73d24739b)
AFTER_EPOCH=$((TARGET_EPOCH + 1))
AFTER_TIMESTAMP=$(date -u -d "@$AFTER_EPOCH" "+%Y-%m-%d %H:%M:%S")
COMMIT_COUNT=$(git log --oneline --all --since="$AFTER_TIMESTAMP" | wc -l)
[ "$COMMIT_COUNT" -eq 0 ] || exit 1
cd - || true
chmod -R 777 /testbed
cd /testbed
git clean -fdxq
source $NVM_DIR/nvm.sh
npm install --ignore-scripts
mkdir -p /opt/puppeteer-cache/chrome/linux-122.0.6261.128 && wget -q https://storage.googleapis.com/chrome-for-testing-public/122.0.6261.128/linux64/chrome-linux64.zip -O /tmp/chrome.zip && unzip -q /tmp/chrome.zip -d /opt/puppeteer-cache/chrome/linux-122.0.6261.128/ && rm /tmp/chrome.zip && chmod -R 755 /opt/puppeteer-cache/chrome/linux-122.0.6261.128
mkdir -p /opt/puppeteer-cache/chrome/linux-123.0.6312.58 && wget -q https://storage.googleapis.com/chrome-for-testing-public/123.0.6312.58/linux64/chrome-linux64.zip -O /tmp/chrome.zip && unzip -q /tmp/chrome.zip -d /opt/puppeteer-cache/chrome/linux-123.0.6312.58/ && rm /tmp/chrome.zip && chmod -R 755 /opt/puppeteer-cache/chrome/linux-123.0.6312.58
mkdir -p /opt/puppeteer-cache/chrome/linux-123.0.6312.122 && wget -q https://storage.googleapis.com/chrome-for-testing-public/123.0.6312.122/linux64/chrome-linux64.zip -O /tmp/chrome.zip && unzip -q /tmp/chrome.zip -d /opt/puppeteer-cache/chrome/linux-123.0.6312.122/ && rm /tmp/chrome.zip && chmod -R 755 /opt/puppeteer-cache/chrome/linux-123.0.6312.122
mkdir -p /opt/puppeteer-cache/chrome/linux-124.0.6367.78 && wget -q https://storage.googleapis.com/chrome-for-testing-public/124.0.6367.78/linux64/chrome-linux64.zip -O /tmp/chrome.zip && unzip -q /tmp/chrome.zip -d /opt/puppeteer-cache/chrome/linux-124.0.6367.78/ && rm /tmp/chrome.zip && chmod -R 755 /opt/puppeteer-cache/chrome/linux-124.0.6367.78
mkdir -p /opt/puppeteer-cache/chrome/linux-124.0.6367.91 && wget -q https://storage.googleapis.com/chrome-for-testing-public/124.0.6367.91/linux64/chrome-linux64.zip -O /tmp/chrome.zip && unzip -q /tmp/chrome.zip -d /opt/puppeteer-cache/chrome/linux-124.0.6367.91/ && rm /tmp/chrome.zip && chmod -R 755 /opt/puppeteer-cache/chrome/linux-124.0.6367.91
python3 - <<'PYEOF'
import re
f = 'test/rendering/test.js'
s = open(f).read()
new_fn = '''async function renderEach(_unused, entries, options) {\n  let fail = false;\n  for (const entry of entries) {\n    const browser = await puppeteer.launch({\n      args: options.puppeteerArgs,\n      headless: options.headless ? "new" : false,\n    });\n    const page = await browser.newPage();\n    page.on("error", (err) => { options.log.error("page crash", err); });\n    page.on("pageerror", (err) => { options.log.error("uncaught exception", err); });\n    page.on("console", (m) => { const t = m.type(); if (options.log[t]) options.log[t](`console: ${m.text()}`); });\n    page.setDefaultNavigationTimeout(options.timeout);\n    await exposeRender(page);\n    await page.setViewport({width: 256, height: 256});\n    try {\n      const {tolerance = 0.005, message = ""} = await renderPage(page, entry, options);\n      if (options.fix) { await copyActualToExpected(entry); continue; }\n      const {error, mismatch} = await getScreenshotsMismatch(entry);\n      if (error) { options.log.error(error); fail = true; continue; }\n      let detail = `case ${entry}`;\n      if (message) detail = `${detail} (${message})`;\n      if (mismatch > tolerance) { options.log.error(`${detail}\\x27: mismatch ${mismatch}`); fail = true; }\n      else { options.log.info(`${detail}\\x27: ok`); await touch(getPassFilePath(entry)); }\n    } finally {\n      await browser.close();\n    }\n  }\n  return fail;\n}\n'''
s = re.sub(r'    const page = await browser\.newPage\(\);.*?fail = await renderEach\(page, entries, options\);',
           '    fail = await renderEach(browser, entries, options);', s, count=1, flags=re.DOTALL)
m = re.search(r'async function renderEach\(page, entries, options\)[^{]*\{.*?  return fail;\n\}\n', s, re.DOTALL)
if not m: raise SystemExit('renderEach not found')
open(f, 'w').write(s[:m.start()] + new_fn + s[m.end():])
PYEOF
npm install karma-json-reporter@1.2.1 --no-save --legacy-peer-deps
sed -i "s|reporters: \['dots', 'coverage-istanbul'\]|reporters: ['json'],\n        jsonReporter: { outputFile: '/testbed/karma-results.json', stdout: false }|" test/browser/karma.config.cjs ; sed -i "s|reporters: \['dots'\]|reporters: ['json'],\n        jsonReporter: { outputFile: '/testbed/karma-results.json', stdout: false }|" test/browser/karma.config.cjs ; sed -i "s|reporters: \['progress'\]|reporters: ['json'],\n        jsonReporter: { outputFile: '/testbed/karma-results.json', stdout: false }|" test/browser/karma.config.cjs
sed -i "s/browsers: \[process.env.CI ? 'ChromeHeadless' : 'Chrome'\]/customLaunchers: { ChromeNoSandbox: { base: 'ChromeHeadless', flags: ['--no-sandbox', '--disable-dev-shm-usage'] } },\n    browsers: ['ChromeNoSandbox']/; s/browsers: \['ChromeHeadless'\]/customLaunchers: { ChromeNoSandbox: { base: 'ChromeHeadless', flags: ['--no-sandbox', '--disable-dev-shm-usage'] } },\n    browsers: ['ChromeNoSandbox']/; s/browsers: \['Chrome'\]/customLaunchers: { ChromeNoSandbox: { base: 'ChromeHeadless', flags: ['--no-sandbox', '--disable-dev-shm-usage'] } },\n    browsers: ['ChromeNoSandbox']/; s/flags: \['--headless=new'\]/flags: ['--headless=new', '--no-sandbox', '--disable-dev-shm-usage']/" test/browser/karma.config.cjs
if grep -q 'resolve:' test/browser/karma.config.cjs; then sed -i '0,/resolve:[[:space:]]*{/s|resolve:[[:space:]]*{|resolve: { alias: { ol: require(\"path\").resolve(__dirname, \"../../src/ol\") },|' test/browser/karma.config.cjs; else sed -i '/webpack:[[:space:]]*{/a\    resolve: { alias: { ol: require(\"path\").resolve(__dirname, \"../../src/ol\") }, },' test/browser/karma.config.cjs; fi
EOF_8bd7452bf2c6


COPY src/image_assets/openlayers__openlayers-15685/ /swebench/image_assets/

WORKDIR /testbed
