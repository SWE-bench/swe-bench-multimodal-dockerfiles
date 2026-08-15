
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
RUN apt-get update \
    && apt-get install -y fonts-ipafont-gothic fonts-wqy-zenhei fonts-thai-tlwg \
        fonts-khmeros fonts-kacst fonts-freefont-ttf libxss1 dbus dbus-x11 \
        --no-install-recommends \
    && rm -rf /var/lib/apt/lists/*
# Pin Chrome. The apt repo only ever serves the current stable, so an unpinned install
# silently changes version on every rebuild -- Chrome 151 broke openlayers' WebGL and
# Cypress's browser connection that way. Chrome for Testing archives every build, so this
# stays reproducible. Keep both binary names: 160 eval scripts reference one or the other.
RUN wget -q https://storage.googleapis.com/chrome-for-testing-public/151.0.7922.137/linux64/chrome-linux64.zip -O /tmp/chrome.zip \
    && unzip -q /tmp/chrome.zip -d /opt/chrome-pinned \
    && rm /tmp/chrome.zip \
    && printf '#!/bin/bash\nexec /opt/chrome-pinned/chrome-linux64/chrome "$@"\n' > /usr/bin/google-chrome \
    && chmod +x /usr/bin/google-chrome \
    && cp /usr/bin/google-chrome /usr/bin/google-chrome-stable

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

ENV CHROME_BIN /usr/bin/google-chrome
RUN echo "CHROME_BIN=$CHROME_BIN" >> /etc/environment
RUN mkdir -p /run/dbus

ENV DBUS_SESSION_BUS_ADDRESS="unix:path=/run/dbus/system_bus_socket"

RUN dbus-daemon --system --fork

ENV PUPPETEER_SKIP_CHROMIUM_DOWNLOAD=true
# puppeteer v20+ renamed the variable; without it install.mjs hangs fetching Chrome
ENV PUPPETEER_SKIP_DOWNLOAD=true
ENV OPENSSL_CONF /etc/ssl

RUN useradd -m chromeuser

USER chromeuser

WORKDIR /home/chromeuser

USER root

ENV NODE_VERSION 18.20.4
ENV NODE_PATH $NVM_DIR/v$NODE_VERSION/lib/node_modules
ENV PATH $NVM_DIR/versions/node/v$NODE_VERSION/bin:$PATH

RUN <<EOF_a32284fbdcc9
#!/bin/bash
set -euxo pipefail
apt-get update
apt-get install -y pkg-config build-essential libpixman-1-0 libpixman-1-dev libcairo2-dev libpango1.0-dev libjpeg-dev libgif-dev librsvg2-dev libx11-xcb1 libxcomposite1 libxcursor1 libxdamage1 libxi6 libxtst6 libnss3 libcups2 libxss1 libxrandr2 libasound2 libatk1.0-0 libgtk-3-0 x11-utils
rm -rf /var/lib/apt/lists/*
export NODE_VERSION=18.20.4
source $NVM_DIR/nvm.sh
nvm install $NODE_VERSION
nvm alias default $NODE_VERSION
nvm use default
add-apt-repository ppa:deadsnakes/ppa
apt-get update
apt-get install -y python3.9
ln -sf /usr/bin/python3.9 /usr/bin/python
apt-get install -y python2
echo "export NODE_PATH=$NVM_DIR/v18.20.4/lib/node_modules" >> /etc/environment
echo "export PATH=$NVM_DIR/versions/node/v18.20.4/bin:$PATH" >> /etc/environment
source $NVM_DIR/nvm.sh && node -v
source $NVM_DIR/nvm.sh && npm -v
python -V
python2 -V
EOF_a32284fbdcc9


RUN <<EOF_3b15f29f7a2b
#!/bin/bash
set -euxo pipefail
(mkdir -p /testbed && cd /testbed && git init -q . && git remote add origin https://github.com/diegomura/react-pdf && git fetch -q --depth 1 origin bef5d6e39ee877fb0ca6957652984dda09e1cb71 && git reset -q --hard FETCH_HEAD) || (rm -rf /testbed && git clone -o origin https://github.com/diegomura/react-pdf /testbed)
cd /testbed
git reset --hard bef5d6e39ee877fb0ca6957652984dda09e1cb71
git remote remove origin
TARGET_TIMESTAMP=$(git show -s --format=%ci bef5d6e39ee877fb0ca6957652984dda09e1cb71)
TARGET_EPOCH=$(git show -s --format=%ct bef5d6e39ee877fb0ca6957652984dda09e1cb71)
for tag in $(git tag -l); do TAG_EPOCH=$(git log -1 --format=%ct "$tag" 2>/dev/null || echo 0); if [ "${TAG_EPOCH:-0}" -gt "$TARGET_EPOCH" ]; then git tag -d "$tag" >/dev/null 2>&1 || true; fi; done
git branch | grep -v '^\*' | xargs -r git branch -D || true
git reflog expire --expire=now --all
git gc --prune=now --aggressive
AFTER_TIMESTAMP=$(date -d "$TARGET_TIMESTAMP + 1 second" '+%Y-%m-%d %H:%M:%S')
COMMIT_COUNT=$(git log --oneline --all --since="$AFTER_TIMESTAMP" | wc -l)
[ "$COMMIT_COUNT" -eq 0 ] || exit 1
chmod -R 777 /testbed
cd - || true
cd /testbed
git clean -fdxq
source $NVM_DIR/nvm.sh
npm i -g yarn
yarn install
chmod -R 777 /testbed
EOF_3b15f29f7a2b


RUN <<EOF_56cfbff49a5f
#!/bin/bash
set -euxo pipefail
mkdir -p /swebench/image_assets
mkdir -p /swebench/image_assets/problem_statement
curl -fsSL -o '/swebench/image_assets/problem_statement/133747387-36b0979e-13ca-46a8-88f9-d5f814b744fc.png' 'https://user-images.githubusercontent.com/6726016/133747387-36b0979e-13ca-46a8-88f9-d5f814b744fc.png' || true
mkdir -p /swebench/image_assets/problem_statement
curl -fsSL -o '/swebench/image_assets/problem_statement/133747413-879dda20-3a50-4163-ad6f-1f4d0a8a879b.png' 'https://user-images.githubusercontent.com/6726016/133747413-879dda20-3a50-4163-ad6f-1f4d0a8a879b.png' || true
EOF_56cfbff49a5f


WORKDIR /testbed
