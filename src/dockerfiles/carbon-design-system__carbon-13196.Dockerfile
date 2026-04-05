
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

ENV NODE_VERSION 18.14.2
ENV NODE_PATH $NVM_DIR/v$NODE_VERSION/lib/node_modules
ENV PATH $NVM_DIR/versions/node/v$NODE_VERSION/bin:$PATH

RUN <<EOF_0730f8a849ef
#!/bin/bash
set -euxo pipefail
export NODE_VERSION=18.14.2
source $NVM_DIR/nvm.sh
nvm install $NODE_VERSION
nvm alias default $NODE_VERSION
nvm use default
add-apt-repository ppa:deadsnakes/ppa
apt-get update
apt-get install -y python3.9
ln -sf /usr/bin/python3.9 /usr/bin/python
apt-get install -y python2
echo "export NODE_PATH=$NVM_DIR/v18.14.2/lib/node_modules" >> /etc/environment
echo "export PATH=$NVM_DIR/versions/node/v18.14.2/bin:$PATH" >> /etc/environment
source $NVM_DIR/nvm.sh && node -v
source $NVM_DIR/nvm.sh && npm -v
python -V
python2 -V
EOF_0730f8a849ef


RUN <<EOF_f3fea9b41446
#!/bin/bash
set -euxo pipefail
git clone -o origin https://github.com/carbon-design-system/carbon /testbed
chmod -R 777 /testbed
cd /testbed
git reset --hard 07168bf0272678a04c92cd1e700ac60e66355a95
git remote remove origin
TARGET_EPOCH=$(git show -s --format=%ct 07168bf0272678a04c92cd1e700ac60e66355a95)
git tag -l | while read tag; do TAG_COMMIT=$(git rev-list -n 1 "$tag"); TAG_EPOCH=$(git show -s --format=%ct "$TAG_COMMIT"); if [ "$TAG_EPOCH" -gt "$TARGET_EPOCH" ]; then git tag -d "$tag"; fi; done
git branch -D $(git branch | grep -v "^\*") 2>/dev/null || true
git reflog expire --expire=now --all
cd - || true
cd /testbed
git clean -fdxq
source $NVM_DIR/nvm.sh
npm i -g yarn
yarn install
yarn build
wget -q https://registry.npmjs.org/nwsapi/-/nwsapi-2.2.7.tgz && tar xzf nwsapi-2.2.7.tgz -C node_modules/nwsapi --strip-components=1 && rm nwsapi-2.2.7.tgz
EOF_f3fea9b41446


RUN <<EOF_35cb2bf3f34f
#!/bin/bash
set -euxo pipefail
mkdir -p /swebench/image_assets
mkdir -p /swebench/image_assets/problem_statement
curl -fsSL -o '/swebench/image_assets/problem_statement/213830268-04bcd81d-e792-447a-aefa-f242978c8b67.png' 'https://user-images.githubusercontent.com/8657768/213830268-04bcd81d-e792-447a-aefa-f242978c8b67.png' || true
mkdir -p /swebench/image_assets/problem_statement
curl -fsSL -o '/swebench/image_assets/problem_statement/213830471-78a33a93-2f05-4590-bfe1-87a8061c35e9.png' 'https://user-images.githubusercontent.com/8657768/213830471-78a33a93-2f05-4590-bfe1-87a8061c35e9.png' || true
mkdir -p /swebench/image_assets/problem_statement
curl -fsSL -o '/swebench/image_assets/problem_statement/213831345-116a8a00-4083-487f-8292-a92bf3ce48ff.png' 'https://user-images.githubusercontent.com/8657768/213831345-116a8a00-4083-487f-8292-a92bf3ce48ff.png' || true
mkdir -p /swebench/image_assets/problem_statement
curl -fsSL -o '/swebench/image_assets/problem_statement/213831557-7f76370e-ab4d-4777-85a5-b541a4dc445a.png' 'https://user-images.githubusercontent.com/8657768/213831557-7f76370e-ab4d-4777-85a5-b541a4dc445a.png' || true
mkdir -p /swebench/image_assets/problem_statement
curl -fsSL -o '/swebench/image_assets/problem_statement/213831318-0114325c-cfcc-49b1-9a05-0b2c6fcd87b1.png' 'https://user-images.githubusercontent.com/8657768/213831318-0114325c-cfcc-49b1-9a05-0b2c6fcd87b1.png' || true
EOF_35cb2bf3f34f


WORKDIR /testbed
