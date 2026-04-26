
FROM --platform=linux/amd64 ubuntu:jammy

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
# Fonts + dbus bits previously piggy-backed onto the google-chrome-stable
# install. CJK fonts are required for pixel-diff rendering tests that compare
# against pre-rendered PNGs containing non-Latin glyphs. Each repo that needs
# a browser pins its own Chromium via chromium_preinstall or analogous
# pre_install step (bpmn-js, next, lighthouse, p5.js, openlayers, chart.js).
RUN apt-get update && apt-get install -y \
    fonts-ipafont-gothic fonts-wqy-zenhei fonts-thai-tlwg \
    fonts-khmeros fonts-kacst fonts-freefont-ttf \
    libxss1 dbus-x11 \
    --no-install-recommends \
    && rm -rf /var/lib/apt/lists/*

ENV NVM_DIR /usr/local/nvm

RUN mkdir -p $NVM_DIR
RUN curl --silent -o- https://raw.githubusercontent.com/creationix/nvm/v0.39.3/install.sh | bash
RUN apt-get update && apt-get install -y \
    procps \
    libasound2 libatk-bridge2.0-0 libatk1.0-0 libcups2 libdrm2 \
    libgbm1 libgconf-2-4 libgdk-pixbuf2.0-0 libgtk-3-0 libnspr4 \
    libnss3 libpango-1.0-0 libpangocairo-1.0-0 libxcomposite1 \
    libxdamage1 libxfixes3 libxkbcommon0 libxrandr2 libxss1 libxshmfence1 libglu1 \
    && apt-get -y autoclean \
    && rm -rf /var/lib/apt/lists/*

RUN mkdir -p /run/dbus

ENV DBUS_SESSION_BUS_ADDRESS="unix:path=/run/dbus/system_bus_socket"

RUN dbus-daemon --system --fork

ENV PUPPETEER_SKIP_CHROMIUM_DOWNLOAD=true
ENV PUPPETEER_SKIP_DOWNLOAD=true
ENV OPENSSL_CONF /etc/ssl

RUN useradd -m chromeuser

USER chromeuser

WORKDIR /home/chromeuser

USER root

ENV NODE_VERSION 16.20.2
ENV NODE_PATH $NVM_DIR/v$NODE_VERSION/lib/node_modules
ENV PATH $NVM_DIR/versions/node/v$NODE_VERSION/bin:$PATH

RUN <<EOF_34e7d255ba3f
#!/bin/bash
set -euxo pipefail
export NODE_VERSION=16.20.2
source $NVM_DIR/nvm.sh
nvm install $NODE_VERSION
nvm alias default $NODE_VERSION
nvm use default
add-apt-repository ppa:deadsnakes/ppa
apt-get update
apt-get install -y python3.9
ln -sf /usr/bin/python3.9 /usr/bin/python
apt-get install -y python2
echo "export NODE_PATH=$NVM_DIR/v16.20.2/lib/node_modules" >> /etc/environment
echo "export PATH=$NVM_DIR/versions/node/v16.20.2/bin:$PATH" >> /etc/environment
source $NVM_DIR/nvm.sh && node -v
source $NVM_DIR/nvm.sh && npm -v
python -V
python2 -V
EOF_34e7d255ba3f


RUN <<EOF_3f6d2762320e
#!/bin/bash
set -euxo pipefail
apt-get update && apt-get install -y libxtst6 && rm -rf /var/lib/apt/lists/*
wget -q https://commondatastorage.googleapis.com/chromium-browser-snapshots/Linux_x64/672088/chrome-linux.zip -O /tmp/chromium.zip
unzip -q /tmp/chromium.zip -d /opt/chromium-pinned/
rm /tmp/chromium.zip
mkdir -p /opt/chromium
ln -sf /opt/chromium-pinned/chrome-linux/chrome /opt/chromium/chrome-bin
VER=$(/opt/chromium/chrome-bin --no-sandbox --version 2>&1 | grep -oE '[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+')
printf '#!/bin/bash\nif [ "$1" = "--version" ]; then echo "Google Chrome '"$VER"'"; exit 0; fi\nexec /opt/chromium/chrome-bin --no-sandbox --disable-dev-shm-usage "$@"\n' > /opt/chromium/chrome
chmod +x /opt/chromium/chrome
chmod -R 755 /opt/chromium-pinned
ln -sf /opt/chromium/chrome /usr/bin/google-chrome
ln -sf /opt/chromium/chrome /usr/bin/google-chrome-stable
cat > /usr/local/bin/pretty-karma-json <<'PYEOF'
#!/usr/bin/env python3
import re, json, sys
if len(sys.argv) < 2:
    print('usage: pretty-karma-json <log_file>', file=sys.stderr); sys.exit(2)
with open(sys.argv[1], errors='replace') as f:
    c = f.read()
m = re.search(r'\{\s*"browsers"', c)
# Pass-through any non-JSON preamble lines
for line in c.split('\n'):
    if m and line.lstrip().startswith('{"browsers"'):
        continue
    print(line)
if m:
    try:
        data, _ = json.JSONDecoder().raw_decode(c[m.start():])
        print(json.dumps(data, indent=2))
    except Exception as e:
        print(f'# pretty-karma-json: {e}', file=sys.stderr)
        print(c[m.start():m.start()+200], file=sys.stderr)
PYEOF
chmod +x /usr/local/bin/pretty-karma-json
EOF_3f6d2762320e


RUN <<EOF_f629b355cc1c
#!/bin/bash
set -euxo pipefail
git clone -o origin https://github.com/bpmn-io/bpmn-js /testbed
cd /testbed
git reset --hard 36e4f6113c5fc1e826894244c6da39636b75861c
git remote remove origin
git branch | grep -v '^\*' | xargs -r git branch -D || true
git tag -l | while read tag; do   git merge-base --is-ancestor "$tag" HEAD 2>/dev/null || git tag -d "$tag" >/dev/null; done
git reflog expire --expire=now --all
git gc --prune=now --aggressive
TARGET_EPOCH=$(git show -s --format=%ct 36e4f6113c5fc1e826894244c6da39636b75861c)
AFTER_EPOCH=$((TARGET_EPOCH + 1))
AFTER_TIMESTAMP=$(date -u -d "@$AFTER_EPOCH" "+%Y-%m-%d %H:%M:%S")
COMMIT_COUNT=$(git log --oneline --all --since="$AFTER_TIMESTAMP" | wc -l)
[ "$COMMIT_COUNT" -eq 0 ] || exit 1
cd - || true
chmod -R 777 /testbed
cd /testbed
git clean -fdxq
source $NVM_DIR/nvm.sh
npm install
npm install karma-json-reporter@1.2.1 --no-save --legacy-peer-deps
EOF_f629b355cc1c


COPY src/image_assets/bpmn-io__bpmn-js-1348/ /swebench/image_assets/

WORKDIR /testbed
