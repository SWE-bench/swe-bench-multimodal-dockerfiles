
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


RUN <<EOF_71683d3e4e95
#!/bin/bash
set -euxo pipefail
apt-get update && apt-get install -y libxtst6 && rm -rf /var/lib/apt/lists/*
wget -q https://commondatastorage.googleapis.com/chromium-browser-snapshots/Linux_x64/793478/chrome-linux.zip
unzip -q chrome-linux.zip -d /opt/
rm chrome-linux.zip
rm -f /usr/bin/google-chrome /usr/bin/google-chrome-stable
printf '#!/bin/bash\nexec /opt/chrome-linux/chrome --no-sandbox "$@"\n' > /usr/bin/google-chrome
chmod +x /usr/bin/google-chrome
cp /usr/bin/google-chrome /usr/bin/google-chrome-stable
EOF_71683d3e4e95


RUN <<EOF_67998d438b7d
#!/bin/bash
set -euxo pipefail
git clone -o origin https://github.com/bpmn-io/bpmn-js /testbed
cd /testbed
git reset --hard 4706a407c0b139682c4d9b36db323095d38681d0
git remote remove origin
TARGET_EPOCH=$(git show -s --format=%ct 4706a407c0b139682c4d9b36db323095d38681d0)
git tag -l | while read tag; do TAG_COMMIT=$(git rev-list -n 1 "$tag"); TAG_EPOCH=$(git show -s --format=%ct "$TAG_COMMIT"); if [ "$TAG_EPOCH" -gt "$TARGET_EPOCH" ]; then git tag -d "$tag"; fi; done
git branch -D $(git branch | grep -v "^\*") 2>/dev/null || true
git reflog expire --expire=now --all
cd - || true
chmod -R 777 /testbed
cd /testbed
git clean -fdxq
source $NVM_DIR/nvm.sh
npm install
npm install karma-json-reporter@1.2.1 --no-save
sed -i "s/reporters: \[ 'progress' \].concat(coverage ? 'coverage' : \[\])/reporters: ['json'],\n        jsonReporter: { stdout: true }/" test/config/karma.unit.js
EOF_67998d438b7d


WORKDIR /testbed
