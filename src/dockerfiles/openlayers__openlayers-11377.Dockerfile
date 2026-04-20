
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


RUN <<EOF_0e4ad7aac9eb
#!/bin/bash
set -euxo pipefail
git clone -o origin https://github.com/openlayers/openlayers /testbed
cd /testbed
git reset --hard 302bc662af22bc353c87ae1a3700c6958c69b8e9
git remote remove origin
git branch | grep -v '^\*' | xargs -r git branch -D || true
git tag -l | while read tag; do   git merge-base --is-ancestor "$tag" HEAD 2>/dev/null || git tag -d "$tag" >/dev/null; done
git reflog expire --expire=now --all
git gc --prune=now --aggressive
TARGET_EPOCH=$(git show -s --format=%ct 302bc662af22bc353c87ae1a3700c6958c69b8e9)
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
mkdir -p node_modules/puppeteer/.local-chromium/linux-782078 && wget -q https://commondatastorage.googleapis.com/chromium-browser-snapshots/Linux_x64/782078/chrome-linux.zip -O /tmp/chrome.zip && unzip -q /tmp/chrome.zip -d node_modules/puppeteer/.local-chromium/linux-782078/ && rm /tmp/chrome.zip && chmod -R 755 node_modules/puppeteer/.local-chromium/linux-782078
mkdir -p node_modules/puppeteer/.local-chromium/linux-800071 && wget -q https://commondatastorage.googleapis.com/chromium-browser-snapshots/Linux_x64/800071/chrome-linux.zip -O /tmp/chrome.zip && unzip -q /tmp/chrome.zip -d node_modules/puppeteer/.local-chromium/linux-800071/ && rm /tmp/chrome.zip && chmod -R 755 node_modules/puppeteer/.local-chromium/linux-800071
grep -q 'process.env.CHROME_BIN' test/karma.config.js || echo "process.env.CHROME_BIN = require('puppeteer').executablePath();" >> test/karma.config.js
npm install karma-json-reporter@1.2.1 --no-save --legacy-peer-deps
sed -i "s/reporters: \['dots', 'coverage-istanbul'\]/reporters: ['json'],\n        jsonReporter: { stdout: true }/" test/karma.config.js ; sed -i "s/reporters: \['dots'\]/reporters: ['json'],\n        jsonReporter: { stdout: true }/" test/karma.config.js ; sed -i "s/reporters: \['progress'\]/reporters: ['json'],\n        jsonReporter: { stdout: true }/" test/karma.config.js
sed -i "s/browsers: \[process.env.CI ? 'ChromeHeadless' : 'Chrome'\]/customLaunchers: { ChromeNoSandbox: { base: 'ChromeHeadless', flags: ['--no-sandbox'] } },\n    browsers: ['ChromeNoSandbox']/; s/browsers: \['ChromeHeadless'\]/customLaunchers: { ChromeNoSandbox: { base: 'ChromeHeadless', flags: ['--no-sandbox'] } },\n    browsers: ['ChromeNoSandbox']/; s/browsers: \['Chrome'\]/customLaunchers: { ChromeNoSandbox: { base: 'ChromeHeadless', flags: ['--no-sandbox'] } },\n    browsers: ['ChromeNoSandbox']/; s/flags: \['--headless=new'\]/flags: ['--headless=new', '--no-sandbox']/" test/karma.config.js
if grep -q 'resolve:' test/karma.config.js; then sed -i '0,/resolve:[[:space:]]*{/s|resolve:[[:space:]]*{|resolve: { alias: { ol: require(\"path\").resolve(__dirname, \"../../src/ol\") },|' test/karma.config.js; else sed -i '/webpack:[[:space:]]*{/a\    resolve: { alias: { ol: require(\"path\").resolve(__dirname, \"../../src/ol\") }, },' test/karma.config.js; fi
EOF_0e4ad7aac9eb


COPY src/image_assets/openlayers__openlayers-11377/ /swebench/image_assets/

WORKDIR /testbed
