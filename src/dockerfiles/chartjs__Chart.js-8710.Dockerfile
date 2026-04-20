
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


RUN <<EOF_b4f20baaf575
#!/bin/bash
set -euxo pipefail
apt-get update && apt-get install -y libxtst6 && rm -rf /var/lib/apt/lists/*
wget -q https://commondatastorage.googleapis.com/chromium-browser-snapshots/Linux_x64/856583/chrome-linux.zip
unzip -q chrome-linux.zip -d /opt/
rm chrome-linux.zip
rm -f /usr/bin/google-chrome /usr/bin/google-chrome-stable
printf '#!/bin/bash\nexec /opt/chrome-linux/chrome --no-sandbox "$@"\n' > /usr/bin/google-chrome
chmod +x /usr/bin/google-chrome
cp /usr/bin/google-chrome /usr/bin/google-chrome-stable
EOF_b4f20baaf575


RUN <<EOF_ac555d5f093d
#!/bin/bash
set -euxo pipefail
git clone -o origin https://github.com/chartjs/Chart.js /testbed
cd /testbed
git reset --hard bbf298f4614c058e2ec86329566a56bfcd8bc685
git remote remove origin
git branch | grep -v '^\*' | xargs -r git branch -D || true
git tag -l | while read tag; do   git merge-base --is-ancestor "$tag" HEAD 2>/dev/null || git tag -d "$tag" >/dev/null; done
git reflog expire --expire=now --all
git gc --prune=now --aggressive
TARGET_EPOCH=$(git show -s --format=%ct bbf298f4614c058e2ec86329566a56bfcd8bc685)
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
npm install karma-json-reporter@1.2.1 --save-dev --legacy-peer-deps
sed -i -E "s#reporters: \['(spec|progress)'[^]]*\],#reporters: ['json'],\n        jsonReporter: { outputFile: '/testbed/karma-results.json' },#" karma.conf.js
sed -i "s/frameworks: \['jasmine'\],/frameworks: ['jasmine'],\n    captureTimeout: 180000,\n    browserDisconnectTimeout: 120000,\n    browserDisconnectTolerance: 3,\n    browserNoActivityTimeout: 180000,/" karma.conf.js
sed -i "s/--disable-renderer-backgrounding/--disable-renderer-backgrounding',\n          '--disable-dev-shm-usage/" karma.conf.js
EOF_ac555d5f093d


COPY src/image_assets/chartjs__Chart.js-8710/ /swebench/image_assets/

WORKDIR /testbed
