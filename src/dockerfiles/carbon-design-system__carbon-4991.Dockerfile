
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
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - \
    && echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list \
    && apt-get update \
    && apt-get install -y google-chrome-stable fonts-ipafont-gothic fonts-wqy-zenhei fonts-thai-tlwg \
        fonts-khmeros fonts-kacst fonts-freefont-ttf libxss1 dbus dbus-x11 \
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

ENV CHROME_BIN /usr/bin/google-chrome
RUN echo "CHROME_BIN=$CHROME_BIN" >> /etc/environment
RUN mkdir -p /run/dbus

ENV DBUS_SESSION_BUS_ADDRESS="unix:path=/run/dbus/system_bus_socket"

RUN dbus-daemon --system --fork

ENV PUPPETEER_SKIP_CHROMIUM_DOWNLOAD=true
ENV OPENSSL_CONF /etc/ssl

RUN useradd -m chromeuser

USER chromeuser

WORKDIR /home/chromeuser

USER root

ENV NODE_VERSION 10.24.1
ENV NODE_PATH $NVM_DIR/v$NODE_VERSION/lib/node_modules
ENV PATH $NVM_DIR/versions/node/v$NODE_VERSION/bin:$PATH

RUN <<EOF_31553638dfda
#!/bin/bash
set -euxo pipefail
export NODE_VERSION=10.24.1
source $NVM_DIR/nvm.sh
nvm install $NODE_VERSION
nvm alias default $NODE_VERSION
nvm use default
add-apt-repository ppa:deadsnakes/ppa
apt-get update
apt-get install -y python3.9
ln -sf /usr/bin/python3.9 /usr/bin/python
apt-get install -y python2
echo "export NODE_PATH=$NVM_DIR/v10.24.1/lib/node_modules" >> /etc/environment
echo "export PATH=$NVM_DIR/versions/node/v10.24.1/bin:$PATH" >> /etc/environment
source $NVM_DIR/nvm.sh && node -v
source $NVM_DIR/nvm.sh && npm -v
python -V
python2 -V
EOF_31553638dfda


RUN <<EOF_6c874aa10408
#!/bin/bash
set -euxo pipefail
(mkdir -p /testbed && cd /testbed && git init -q . && git remote add origin https://github.com/carbon-design-system/carbon && git fetch -q --depth 1 origin 3de43bb36c9d643cd66d5c8115a1f81737e449bb && git reset -q --hard FETCH_HEAD) || (rm -rf /testbed && git clone -o origin https://github.com/carbon-design-system/carbon /testbed)
chmod -R 777 /testbed
cd /testbed
git reset --hard 3de43bb36c9d643cd66d5c8115a1f81737e449bb
git remote remove origin
TARGET_TIMESTAMP=$(git show -s --format=%ci 3de43bb36c9d643cd66d5c8115a1f81737e449bb)
git branch | grep -v '^\*' | xargs -r git branch -D || true
git tag -l | xargs -r git tag -d
git reflog expire --expire=now --all
git gc --prune=now --aggressive
AFTER_TIMESTAMP=$(date -d "$TARGET_TIMESTAMP + 1 second" '+%Y-%m-%d %H:%M:%S')
COMMIT_COUNT=$(git log --oneline --all --since="$AFTER_TIMESTAMP" | wc -l)
[ "$COMMIT_COUNT" -eq 0 ] || exit 1
cd - || true
cd /testbed
git clean -fdxq
source $NVM_DIR/nvm.sh
npm i -g yarn
yarn install
yarn build
wget -q https://registry.npmjs.org/nwsapi/-/nwsapi-2.2.7.tgz && tar xzf nwsapi-2.2.7.tgz -C node_modules/nwsapi --strip-components=1 && rm nwsapi-2.2.7.tgz
echo 'ruleArchive: 07Oct2020' > .achecker.yml
EOF_6c874aa10408


RUN <<EOF_875fd4884e00
#!/bin/bash
set -euxo pipefail
mkdir -p /swebench/image_assets
mkdir -p /swebench/image_assets/problem_statement
curl -fsSL -o '/swebench/image_assets/problem_statement/64991861-4c67a400-d898-11e9-8953-003058112467.png' 'https://user-images.githubusercontent.com/21676914/64991861-4c67a400-d898-11e9-8953-003058112467.png' || true
mkdir -p /swebench/image_assets/problem_statement
curl -fsSL -o '/swebench/image_assets/problem_statement/64992426-7ec5d100-d899-11e9-91a3-03296e4c5753.png' 'https://user-images.githubusercontent.com/21676914/64992426-7ec5d100-d899-11e9-91a3-03296e4c5753.png' || true
mkdir -p /swebench/image_assets/problem_statement
curl -fsSL -o '/swebench/image_assets/problem_statement/64992519-aa48bb80-d899-11e9-9297-b9c07461ef50.png' 'https://user-images.githubusercontent.com/21676914/64992519-aa48bb80-d899-11e9-9297-b9c07461ef50.png' || true
EOF_875fd4884e00


WORKDIR /testbed
