
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

ENV NODE_VERSION 8.17.0
ENV NODE_PATH $NVM_DIR/v$NODE_VERSION/lib/node_modules
ENV PATH $NVM_DIR/versions/node/v$NODE_VERSION/bin:$PATH

RUN <<EOF_4d2410c5ce08
#!/bin/bash
set -euxo pipefail
apt-get update
apt-get install -y python3 python3-pip xvfb x11-xkb-utils xfonts-100dpi xfonts-75dpi xfonts-scalable xfonts-cyrillic x11-apps firefox libsass-dev sassc libsass-dev sassc libsass-dev sassc libsass-dev sassc libsass-dev sassc libsass-dev sassc libsass-dev sassc libsass-dev sassc
rm -rf /var/lib/apt/lists/*
export NODE_VERSION=8.17.0
source $NVM_DIR/nvm.sh
nvm install $NODE_VERSION
nvm alias default $NODE_VERSION
nvm use default
add-apt-repository ppa:deadsnakes/ppa
apt-get update
apt-get install -y python3.9
ln -sf /usr/bin/python3.9 /usr/bin/python
apt-get install -y python2
echo "export NODE_PATH=$NVM_DIR/v8.17.0/lib/node_modules" >> /etc/environment
echo "export PATH=$NVM_DIR/versions/node/v8.17.0/bin:$PATH" >> /etc/environment
source $NVM_DIR/nvm.sh && node -v
source $NVM_DIR/nvm.sh && npm -v
python -V
python2 -V
EOF_4d2410c5ce08


RUN <<EOF_e6ef623bcde6
#!/bin/bash
set -euxo pipefail
git clone -o origin https://github.com/alibaba-fusion/next /testbed
chmod -R 777 /testbed
cd /testbed
git reset --hard 42555dd1b1b7e25da8b049aac17ad4157c99870f
git remote remove origin
TARGET_EPOCH=$(git show -s --format=%ct 42555dd1b1b7e25da8b049aac17ad4157c99870f)
git tag -l | while read tag; do TAG_COMMIT=$(git rev-list -n 1 "$tag"); TAG_EPOCH=$(git show -s --format=%ct "$TAG_COMMIT"); if [ "$TAG_EPOCH" -gt "$TARGET_EPOCH" ]; then git tag -d "$tag"; fi; done
git branch -D $(git branch | grep -v "^\*") 2>/dev/null || true
git reflog expire --expire=now --all
cd - || true
cd /testbed
git clean -fdxq
source $NVM_DIR/nvm.sh
su chromeuser -c 'npm install'
npm install babel-preset-es2015
npm install cheerio@1.0.0-rc.3
npm i sass@1.36.0 --save-exact
npm show cheerio
npm install react@16.7.0 react-dom@16.7.0 enzyme@3.8.0 enzyme-adapter-react-16@1.7.1 --save-exact
EOF_e6ef623bcde6


RUN <<EOF_a57cb9a890f1
#!/bin/bash
set -euxo pipefail
mkdir -p /swebench/image_assets
mkdir -p /swebench/image_assets/problem_statement
curl -fsSL -o '/swebench/image_assets/problem_statement/63851563-00c48780-c9c9-11e9-9006-074098cdc711.png' 'https://user-images.githubusercontent.com/10049465/63851563-00c48780-c9c9-11e9-9006-074098cdc711.png' || true
EOF_a57cb9a890f1


WORKDIR /testbed
