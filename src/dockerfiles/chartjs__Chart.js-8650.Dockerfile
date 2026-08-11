
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

ENV NODE_VERSION 21.6.2
ENV NODE_PATH $NVM_DIR/v$NODE_VERSION/lib/node_modules
ENV PATH $NVM_DIR/versions/node/v$NODE_VERSION/bin:$PATH

RUN <<EOF_55f960f4ac15
#!/bin/bash
set -euxo pipefail
apt-get update
apt-get install -y python3 python3-pip xvfb x11-xkb-utils xfonts-100dpi xfonts-75dpi xfonts-scalable xfonts-cyrillic x11-apps firefox libsass-dev sassc libsass-dev sassc libsass-dev sassc libsass-dev sassc libsass-dev sassc libsass-dev sassc libsass-dev sassc libsass-dev sassc
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
EOF_55f960f4ac15


RUN <<EOF_2d7993114b46
#!/bin/bash
set -euxo pipefail
(mkdir -p /testbed && cd /testbed && git init -q . && git remote add origin https://github.com/chartjs/Chart.js && git fetch -q --depth 1 origin 420aa027b305c91380d96d05e39db2767ec1333a && git reset -q --hard FETCH_HEAD) || (rm -rf /testbed && git clone -o origin https://github.com/chartjs/Chart.js /testbed)
chmod -R 777 /testbed
cd /testbed
git reset --hard 420aa027b305c91380d96d05e39db2767ec1333a
git remote remove origin
TARGET_EPOCH=$(git show -s --format=%ct 420aa027b305c91380d96d05e39db2767ec1333a)
git tag -l | while read tag; do TAG_COMMIT=$(git rev-list -n 1 "$tag"); TAG_EPOCH=$(git show -s --format=%ct "$TAG_COMMIT"); if [ "$TAG_EPOCH" -gt "$TARGET_EPOCH" ]; then git tag -d "$tag"; fi; done
git branch -D $(git branch | grep -v "^\*") 2>/dev/null || true
git reflog expire --expire=now --all
cd - || true
cd /testbed
git clean -fdxq
source $NVM_DIR/nvm.sh
npm install
EOF_2d7993114b46


RUN <<EOF_793198e6251a
#!/bin/bash
set -euxo pipefail
mkdir -p /swebench/image_assets
mkdir -p $(dirname '/swebench/image_assets/test_patch/test/fixtures/controller.line/clip/default-y-max.png')
curl -fsSL -o '/swebench/image_assets/test_patch/test/fixtures/controller.line/clip/default-y-max.png' 'https://raw.githubusercontent.com/chartjs/Chart.js/a7d909e3e0721895e0f9c12a0154e6c2fc42da12/test/fixtures/controller.line/clip/default-y-max.png' || true
mkdir -p $(dirname '/swebench/image_assets/test_patch/test/fixtures/controller.line/clip/default-y.png')
curl -fsSL -o '/swebench/image_assets/test_patch/test/fixtures/controller.line/clip/default-y.png' 'https://raw.githubusercontent.com/chartjs/Chart.js/a7d909e3e0721895e0f9c12a0154e6c2fc42da12/test/fixtures/controller.line/clip/default-y.png' || true
mkdir -p $(dirname '/swebench/image_assets/test_patch/test/fixtures/controller.line/non-numeric-y.png')
curl -fsSL -o '/swebench/image_assets/test_patch/test/fixtures/controller.line/non-numeric-y.png' 'https://raw.githubusercontent.com/chartjs/Chart.js/a7d909e3e0721895e0f9c12a0154e6c2fc42da12/test/fixtures/controller.line/non-numeric-y.png' || true
mkdir -p $(dirname '/swebench/image_assets/test_patch/test/fixtures/controller.line/point-style-offscreen-canvas.png')
curl -fsSL -o '/swebench/image_assets/test_patch/test/fixtures/controller.line/point-style-offscreen-canvas.png' 'https://raw.githubusercontent.com/chartjs/Chart.js/a7d909e3e0721895e0f9c12a0154e6c2fc42da12/test/fixtures/controller.line/point-style-offscreen-canvas.png' || true
mkdir -p $(dirname '/swebench/image_assets/test_patch/test/fixtures/controller.line/point-style.png')
curl -fsSL -o '/swebench/image_assets/test_patch/test/fixtures/controller.line/point-style.png' 'https://raw.githubusercontent.com/chartjs/Chart.js/a7d909e3e0721895e0f9c12a0154e6c2fc42da12/test/fixtures/controller.line/point-style.png' || true
mkdir -p $(dirname '/swebench/image_assets/test_patch/test/fixtures/controller.line/pointBackgroundColor/indexable.png')
curl -fsSL -o '/swebench/image_assets/test_patch/test/fixtures/controller.line/pointBackgroundColor/indexable.png' 'https://raw.githubusercontent.com/chartjs/Chart.js/a7d909e3e0721895e0f9c12a0154e6c2fc42da12/test/fixtures/controller.line/pointBackgroundColor/indexable.png' || true
mkdir -p $(dirname '/swebench/image_assets/test_patch/test/fixtures/controller.line/pointBackgroundColor/scriptable.png')
curl -fsSL -o '/swebench/image_assets/test_patch/test/fixtures/controller.line/pointBackgroundColor/scriptable.png' 'https://raw.githubusercontent.com/chartjs/Chart.js/a7d909e3e0721895e0f9c12a0154e6c2fc42da12/test/fixtures/controller.line/pointBackgroundColor/scriptable.png' || true
mkdir -p $(dirname '/swebench/image_assets/test_patch/test/fixtures/controller.line/pointBackgroundColor/value.png')
curl -fsSL -o '/swebench/image_assets/test_patch/test/fixtures/controller.line/pointBackgroundColor/value.png' 'https://raw.githubusercontent.com/chartjs/Chart.js/a7d909e3e0721895e0f9c12a0154e6c2fc42da12/test/fixtures/controller.line/pointBackgroundColor/value.png' || true
mkdir -p $(dirname '/swebench/image_assets/test_patch/test/fixtures/controller.line/pointBorderColor/indexable.png')
curl -fsSL -o '/swebench/image_assets/test_patch/test/fixtures/controller.line/pointBorderColor/indexable.png' 'https://raw.githubusercontent.com/chartjs/Chart.js/a7d909e3e0721895e0f9c12a0154e6c2fc42da12/test/fixtures/controller.line/pointBorderColor/indexable.png' || true
mkdir -p $(dirname '/swebench/image_assets/test_patch/test/fixtures/controller.line/pointBorderColor/scriptable.png')
curl -fsSL -o '/swebench/image_assets/test_patch/test/fixtures/controller.line/pointBorderColor/scriptable.png' 'https://raw.githubusercontent.com/chartjs/Chart.js/a7d909e3e0721895e0f9c12a0154e6c2fc42da12/test/fixtures/controller.line/pointBorderColor/scriptable.png' || true
mkdir -p $(dirname '/swebench/image_assets/test_patch/test/fixtures/controller.line/pointBorderColor/value.png')
curl -fsSL -o '/swebench/image_assets/test_patch/test/fixtures/controller.line/pointBorderColor/value.png' 'https://raw.githubusercontent.com/chartjs/Chart.js/a7d909e3e0721895e0f9c12a0154e6c2fc42da12/test/fixtures/controller.line/pointBorderColor/value.png' || true
mkdir -p $(dirname '/swebench/image_assets/test_patch/test/fixtures/controller.line/pointBorderWidth/indexable.png')
curl -fsSL -o '/swebench/image_assets/test_patch/test/fixtures/controller.line/pointBorderWidth/indexable.png' 'https://raw.githubusercontent.com/chartjs/Chart.js/a7d909e3e0721895e0f9c12a0154e6c2fc42da12/test/fixtures/controller.line/pointBorderWidth/indexable.png' || true
mkdir -p $(dirname '/swebench/image_assets/test_patch/test/fixtures/controller.line/pointBorderWidth/scriptable.png')
curl -fsSL -o '/swebench/image_assets/test_patch/test/fixtures/controller.line/pointBorderWidth/scriptable.png' 'https://raw.githubusercontent.com/chartjs/Chart.js/a7d909e3e0721895e0f9c12a0154e6c2fc42da12/test/fixtures/controller.line/pointBorderWidth/scriptable.png' || true
mkdir -p $(dirname '/swebench/image_assets/test_patch/test/fixtures/controller.line/pointBorderWidth/value.png')
curl -fsSL -o '/swebench/image_assets/test_patch/test/fixtures/controller.line/pointBorderWidth/value.png' 'https://raw.githubusercontent.com/chartjs/Chart.js/a7d909e3e0721895e0f9c12a0154e6c2fc42da12/test/fixtures/controller.line/pointBorderWidth/value.png' || true
mkdir -p $(dirname '/swebench/image_assets/test_patch/test/fixtures/controller.line/pointStyle/indexable.png')
curl -fsSL -o '/swebench/image_assets/test_patch/test/fixtures/controller.line/pointStyle/indexable.png' 'https://raw.githubusercontent.com/chartjs/Chart.js/a7d909e3e0721895e0f9c12a0154e6c2fc42da12/test/fixtures/controller.line/pointStyle/indexable.png' || true
mkdir -p $(dirname '/swebench/image_assets/test_patch/test/fixtures/controller.line/pointStyle/scriptable.png')
curl -fsSL -o '/swebench/image_assets/test_patch/test/fixtures/controller.line/pointStyle/scriptable.png' 'https://raw.githubusercontent.com/chartjs/Chart.js/a7d909e3e0721895e0f9c12a0154e6c2fc42da12/test/fixtures/controller.line/pointStyle/scriptable.png' || true
mkdir -p $(dirname '/swebench/image_assets/test_patch/test/fixtures/controller.line/pointStyle/value.png')
curl -fsSL -o '/swebench/image_assets/test_patch/test/fixtures/controller.line/pointStyle/value.png' 'https://raw.githubusercontent.com/chartjs/Chart.js/a7d909e3e0721895e0f9c12a0154e6c2fc42da12/test/fixtures/controller.line/pointStyle/value.png' || true
mkdir -p $(dirname '/swebench/image_assets/test_patch/test/fixtures/controller.line/radius/indexable.png')
curl -fsSL -o '/swebench/image_assets/test_patch/test/fixtures/controller.line/radius/indexable.png' 'https://raw.githubusercontent.com/chartjs/Chart.js/a7d909e3e0721895e0f9c12a0154e6c2fc42da12/test/fixtures/controller.line/radius/indexable.png' || true
mkdir -p $(dirname '/swebench/image_assets/test_patch/test/fixtures/controller.line/radius/scriptable.png')
curl -fsSL -o '/swebench/image_assets/test_patch/test/fixtures/controller.line/radius/scriptable.png' 'https://raw.githubusercontent.com/chartjs/Chart.js/a7d909e3e0721895e0f9c12a0154e6c2fc42da12/test/fixtures/controller.line/radius/scriptable.png' || true
mkdir -p $(dirname '/swebench/image_assets/test_patch/test/fixtures/controller.line/radius/value.png')
curl -fsSL -o '/swebench/image_assets/test_patch/test/fixtures/controller.line/radius/value.png' 'https://raw.githubusercontent.com/chartjs/Chart.js/a7d909e3e0721895e0f9c12a0154e6c2fc42da12/test/fixtures/controller.line/radius/value.png' || true
mkdir -p $(dirname '/swebench/image_assets/test_patch/test/fixtures/controller.line/rotation/indexable.png')
curl -fsSL -o '/swebench/image_assets/test_patch/test/fixtures/controller.line/rotation/indexable.png' 'https://raw.githubusercontent.com/chartjs/Chart.js/a7d909e3e0721895e0f9c12a0154e6c2fc42da12/test/fixtures/controller.line/rotation/indexable.png' || true
mkdir -p $(dirname '/swebench/image_assets/test_patch/test/fixtures/controller.line/rotation/scriptable.png')
curl -fsSL -o '/swebench/image_assets/test_patch/test/fixtures/controller.line/rotation/scriptable.png' 'https://raw.githubusercontent.com/chartjs/Chart.js/a7d909e3e0721895e0f9c12a0154e6c2fc42da12/test/fixtures/controller.line/rotation/scriptable.png' || true
mkdir -p $(dirname '/swebench/image_assets/test_patch/test/fixtures/controller.line/rotation/value.png')
curl -fsSL -o '/swebench/image_assets/test_patch/test/fixtures/controller.line/rotation/value.png' 'https://raw.githubusercontent.com/chartjs/Chart.js/a7d909e3e0721895e0f9c12a0154e6c2fc42da12/test/fixtures/controller.line/rotation/value.png' || true
mkdir -p $(dirname '/swebench/image_assets/test_patch/test/fixtures/controller.line/showLine/false.png')
curl -fsSL -o '/swebench/image_assets/test_patch/test/fixtures/controller.line/showLine/false.png' 'https://raw.githubusercontent.com/chartjs/Chart.js/a7d909e3e0721895e0f9c12a0154e6c2fc42da12/test/fixtures/controller.line/showLine/false.png' || true
mkdir -p $(dirname '/swebench/image_assets/test_patch/test/fixtures/controller.line/stacking/stacked-scatter.png')
curl -fsSL -o '/swebench/image_assets/test_patch/test/fixtures/controller.line/stacking/stacked-scatter.png' 'https://raw.githubusercontent.com/chartjs/Chart.js/a7d909e3e0721895e0f9c12a0154e6c2fc42da12/test/fixtures/controller.line/stacking/stacked-scatter.png' || true
mkdir -p $(dirname '/swebench/image_assets/test_patch/test/fixtures/controller.scatter/showLine/true.png')
curl -fsSL -o '/swebench/image_assets/test_patch/test/fixtures/controller.scatter/showLine/true.png' 'https://raw.githubusercontent.com/chartjs/Chart.js/a7d909e3e0721895e0f9c12a0154e6c2fc42da12/test/fixtures/controller.scatter/showLine/true.png' || true
mkdir -p $(dirname '/swebench/image_assets/test_patch/test/fixtures/controller.scatter/showLine/undefined.png')
curl -fsSL -o '/swebench/image_assets/test_patch/test/fixtures/controller.scatter/showLine/undefined.png' 'https://raw.githubusercontent.com/chartjs/Chart.js/a7d909e3e0721895e0f9c12a0154e6c2fc42da12/test/fixtures/controller.scatter/showLine/undefined.png' || true
mkdir -p $(dirname '/swebench/image_assets/test_patch/test/fixtures/core.layouts/hidden-vertical-boxes.png')
curl -fsSL -o '/swebench/image_assets/test_patch/test/fixtures/core.layouts/hidden-vertical-boxes.png' 'https://raw.githubusercontent.com/chartjs/Chart.js/a7d909e3e0721895e0f9c12a0154e6c2fc42da12/test/fixtures/core.layouts/hidden-vertical-boxes.png' || true
mkdir -p $(dirname '/swebench/image_assets/test_patch/test/fixtures/core.layouts/no-boxes-all-padding.png')
curl -fsSL -o '/swebench/image_assets/test_patch/test/fixtures/core.layouts/no-boxes-all-padding.png' 'https://raw.githubusercontent.com/chartjs/Chart.js/a7d909e3e0721895e0f9c12a0154e6c2fc42da12/test/fixtures/core.layouts/no-boxes-all-padding.png' || true
mkdir -p $(dirname '/swebench/image_assets/test_patch/test/fixtures/core.layouts/refit-vertical-boxes.png')
curl -fsSL -o '/swebench/image_assets/test_patch/test/fixtures/core.layouts/refit-vertical-boxes.png' 'https://raw.githubusercontent.com/chartjs/Chart.js/a7d909e3e0721895e0f9c12a0154e6c2fc42da12/test/fixtures/core.layouts/refit-vertical-boxes.png' || true
mkdir -p $(dirname '/swebench/image_assets/test_patch/test/fixtures/core.scale/autoSkip/fit-after.png')
curl -fsSL -o '/swebench/image_assets/test_patch/test/fixtures/core.scale/autoSkip/fit-after.png' 'https://raw.githubusercontent.com/chartjs/Chart.js/a7d909e3e0721895e0f9c12a0154e6c2fc42da12/test/fixtures/core.scale/autoSkip/fit-after.png' || true
mkdir -p $(dirname '/swebench/image_assets/test_patch/test/fixtures/core.scale/cartesian-axis-border-settings.png')
curl -fsSL -o '/swebench/image_assets/test_patch/test/fixtures/core.scale/cartesian-axis-border-settings.png' 'https://raw.githubusercontent.com/chartjs/Chart.js/a7d909e3e0721895e0f9c12a0154e6c2fc42da12/test/fixtures/core.scale/cartesian-axis-border-settings.png' || true
mkdir -p $(dirname '/swebench/image_assets/test_patch/test/fixtures/core.scale/label-align-end.png')
curl -fsSL -o '/swebench/image_assets/test_patch/test/fixtures/core.scale/label-align-end.png' 'https://raw.githubusercontent.com/chartjs/Chart.js/a7d909e3e0721895e0f9c12a0154e6c2fc42da12/test/fixtures/core.scale/label-align-end.png' || true
mkdir -p $(dirname '/swebench/image_assets/test_patch/test/fixtures/core.scale/label-align-start.png')
curl -fsSL -o '/swebench/image_assets/test_patch/test/fixtures/core.scale/label-align-start.png' 'https://raw.githubusercontent.com/chartjs/Chart.js/a7d909e3e0721895e0f9c12a0154e6c2fc42da12/test/fixtures/core.scale/label-align-start.png' || true
mkdir -p $(dirname '/swebench/image_assets/test_patch/test/fixtures/core.scale/x-axis-position-dynamic.png')
curl -fsSL -o '/swebench/image_assets/test_patch/test/fixtures/core.scale/x-axis-position-dynamic.png' 'https://raw.githubusercontent.com/chartjs/Chart.js/a7d909e3e0721895e0f9c12a0154e6c2fc42da12/test/fixtures/core.scale/x-axis-position-dynamic.png' || true
mkdir -p $(dirname '/swebench/image_assets/test_patch/test/fixtures/element.line/default.png')
curl -fsSL -o '/swebench/image_assets/test_patch/test/fixtures/element.line/default.png' 'https://raw.githubusercontent.com/chartjs/Chart.js/a7d909e3e0721895e0f9c12a0154e6c2fc42da12/test/fixtures/element.line/default.png' || true
mkdir -p $(dirname '/swebench/image_assets/test_patch/test/fixtures/element.line/skip/first-span.png')
curl -fsSL -o '/swebench/image_assets/test_patch/test/fixtures/element.line/skip/first-span.png' 'https://raw.githubusercontent.com/chartjs/Chart.js/a7d909e3e0721895e0f9c12a0154e6c2fc42da12/test/fixtures/element.line/skip/first-span.png' || true
mkdir -p $(dirname '/swebench/image_assets/test_patch/test/fixtures/element.line/skip/first.png')
curl -fsSL -o '/swebench/image_assets/test_patch/test/fixtures/element.line/skip/first.png' 'https://raw.githubusercontent.com/chartjs/Chart.js/a7d909e3e0721895e0f9c12a0154e6c2fc42da12/test/fixtures/element.line/skip/first.png' || true
mkdir -p $(dirname '/swebench/image_assets/test_patch/test/fixtures/element.line/skip/last-span.png')
curl -fsSL -o '/swebench/image_assets/test_patch/test/fixtures/element.line/skip/last-span.png' 'https://raw.githubusercontent.com/chartjs/Chart.js/a7d909e3e0721895e0f9c12a0154e6c2fc42da12/test/fixtures/element.line/skip/last-span.png' || true
mkdir -p $(dirname '/swebench/image_assets/test_patch/test/fixtures/element.line/skip/last.png')
curl -fsSL -o '/swebench/image_assets/test_patch/test/fixtures/element.line/skip/last.png' 'https://raw.githubusercontent.com/chartjs/Chart.js/a7d909e3e0721895e0f9c12a0154e6c2fc42da12/test/fixtures/element.line/skip/last.png' || true
mkdir -p $(dirname '/swebench/image_assets/test_patch/test/fixtures/element.line/stepped/after.png')
curl -fsSL -o '/swebench/image_assets/test_patch/test/fixtures/element.line/stepped/after.png' 'https://raw.githubusercontent.com/chartjs/Chart.js/a7d909e3e0721895e0f9c12a0154e6c2fc42da12/test/fixtures/element.line/stepped/after.png' || true
mkdir -p $(dirname '/swebench/image_assets/test_patch/test/fixtures/element.line/stepped/before.png')
curl -fsSL -o '/swebench/image_assets/test_patch/test/fixtures/element.line/stepped/before.png' 'https://raw.githubusercontent.com/chartjs/Chart.js/a7d909e3e0721895e0f9c12a0154e6c2fc42da12/test/fixtures/element.line/stepped/before.png' || true
mkdir -p $(dirname '/swebench/image_assets/test_patch/test/fixtures/element.line/stepped/default.png')
curl -fsSL -o '/swebench/image_assets/test_patch/test/fixtures/element.line/stepped/default.png' 'https://raw.githubusercontent.com/chartjs/Chart.js/a7d909e3e0721895e0f9c12a0154e6c2fc42da12/test/fixtures/element.line/stepped/default.png' || true
mkdir -p $(dirname '/swebench/image_assets/test_patch/test/fixtures/element.line/stepped/middle.png')
curl -fsSL -o '/swebench/image_assets/test_patch/test/fixtures/element.line/stepped/middle.png' 'https://raw.githubusercontent.com/chartjs/Chart.js/a7d909e3e0721895e0f9c12a0154e6c2fc42da12/test/fixtures/element.line/stepped/middle.png' || true
mkdir -p $(dirname '/swebench/image_assets/test_patch/test/fixtures/element.line/tension/default.png')
curl -fsSL -o '/swebench/image_assets/test_patch/test/fixtures/element.line/tension/default.png' 'https://raw.githubusercontent.com/chartjs/Chart.js/a7d909e3e0721895e0f9c12a0154e6c2fc42da12/test/fixtures/element.line/tension/default.png' || true
mkdir -p $(dirname '/swebench/image_assets/test_patch/test/fixtures/element.line/tension/one.png')
curl -fsSL -o '/swebench/image_assets/test_patch/test/fixtures/element.line/tension/one.png' 'https://raw.githubusercontent.com/chartjs/Chart.js/a7d909e3e0721895e0f9c12a0154e6c2fc42da12/test/fixtures/element.line/tension/one.png' || true
mkdir -p $(dirname '/swebench/image_assets/test_patch/test/fixtures/element.line/tension/zero.png')
curl -fsSL -o '/swebench/image_assets/test_patch/test/fixtures/element.line/tension/zero.png' 'https://raw.githubusercontent.com/chartjs/Chart.js/a7d909e3e0721895e0f9c12a0154e6c2fc42da12/test/fixtures/element.line/tension/zero.png' || true
mkdir -p $(dirname '/swebench/image_assets/test_patch/test/fixtures/plugin.filler/fill-line-dataset-interpolated.png')
curl -fsSL -o '/swebench/image_assets/test_patch/test/fixtures/plugin.filler/fill-line-dataset-interpolated.png' 'https://raw.githubusercontent.com/chartjs/Chart.js/a7d909e3e0721895e0f9c12a0154e6c2fc42da12/test/fixtures/plugin.filler/fill-line-dataset-interpolated.png' || true
mkdir -p $(dirname '/swebench/image_assets/test_patch/test/fixtures/plugin.tooltip/positioning.png')
curl -fsSL -o '/swebench/image_assets/test_patch/test/fixtures/plugin.tooltip/positioning.png' 'https://raw.githubusercontent.com/chartjs/Chart.js/a7d909e3e0721895e0f9c12a0154e6c2fc42da12/test/fixtures/plugin.tooltip/positioning.png' || true
mkdir -p $(dirname '/swebench/image_assets/test_patch/test/fixtures/scale.time/autoskip-major.png')
curl -fsSL -o '/swebench/image_assets/test_patch/test/fixtures/scale.time/autoskip-major.png' 'https://raw.githubusercontent.com/chartjs/Chart.js/a7d909e3e0721895e0f9c12a0154e6c2fc42da12/test/fixtures/scale.time/autoskip-major.png' || true
mkdir -p $(dirname '/swebench/image_assets/test_patch/test/fixtures/scale.time/custom-parser.png')
curl -fsSL -o '/swebench/image_assets/test_patch/test/fixtures/scale.time/custom-parser.png' 'https://raw.githubusercontent.com/chartjs/Chart.js/a7d909e3e0721895e0f9c12a0154e6c2fc42da12/test/fixtures/scale.time/custom-parser.png' || true
mkdir -p $(dirname '/swebench/image_assets/test_patch/test/fixtures/scale.time/data-ty.png')
curl -fsSL -o '/swebench/image_assets/test_patch/test/fixtures/scale.time/data-ty.png' 'https://raw.githubusercontent.com/chartjs/Chart.js/a7d909e3e0721895e0f9c12a0154e6c2fc42da12/test/fixtures/scale.time/data-ty.png' || true
mkdir -p $(dirname '/swebench/image_assets/test_patch/test/fixtures/scale.time/data-xy.png')
curl -fsSL -o '/swebench/image_assets/test_patch/test/fixtures/scale.time/data-xy.png' 'https://raw.githubusercontent.com/chartjs/Chart.js/a7d909e3e0721895e0f9c12a0154e6c2fc42da12/test/fixtures/scale.time/data-xy.png' || true
mkdir -p $(dirname '/swebench/image_assets/test_patch/test/fixtures/scale.time/negative-times.png')
curl -fsSL -o '/swebench/image_assets/test_patch/test/fixtures/scale.time/negative-times.png' 'https://raw.githubusercontent.com/chartjs/Chart.js/a7d909e3e0721895e0f9c12a0154e6c2fc42da12/test/fixtures/scale.time/negative-times.png' || true
mkdir -p $(dirname '/swebench/image_assets/test_patch/test/fixtures/scale.time/source-auto-linear.png')
curl -fsSL -o '/swebench/image_assets/test_patch/test/fixtures/scale.time/source-auto-linear.png' 'https://raw.githubusercontent.com/chartjs/Chart.js/a7d909e3e0721895e0f9c12a0154e6c2fc42da12/test/fixtures/scale.time/source-auto-linear.png' || true
mkdir -p $(dirname '/swebench/image_assets/test_patch/test/fixtures/scale.time/source-data-linear.png')
curl -fsSL -o '/swebench/image_assets/test_patch/test/fixtures/scale.time/source-data-linear.png' 'https://raw.githubusercontent.com/chartjs/Chart.js/a7d909e3e0721895e0f9c12a0154e6c2fc42da12/test/fixtures/scale.time/source-data-linear.png' || true
mkdir -p $(dirname '/swebench/image_assets/test_patch/test/fixtures/scale.time/source-labels-linear-offset-min-max.png')
curl -fsSL -o '/swebench/image_assets/test_patch/test/fixtures/scale.time/source-labels-linear-offset-min-max.png' 'https://raw.githubusercontent.com/chartjs/Chart.js/a7d909e3e0721895e0f9c12a0154e6c2fc42da12/test/fixtures/scale.time/source-labels-linear-offset-min-max.png' || true
mkdir -p $(dirname '/swebench/image_assets/test_patch/test/fixtures/scale.time/source-labels-linear.png')
curl -fsSL -o '/swebench/image_assets/test_patch/test/fixtures/scale.time/source-labels-linear.png' 'https://raw.githubusercontent.com/chartjs/Chart.js/a7d909e3e0721895e0f9c12a0154e6c2fc42da12/test/fixtures/scale.time/source-labels-linear.png' || true
mkdir -p $(dirname '/swebench/image_assets/test_patch/test/fixtures/scale.time/ticks-reverse-linear-min-max.png')
curl -fsSL -o '/swebench/image_assets/test_patch/test/fixtures/scale.time/ticks-reverse-linear-min-max.png' 'https://raw.githubusercontent.com/chartjs/Chart.js/a7d909e3e0721895e0f9c12a0154e6c2fc42da12/test/fixtures/scale.time/ticks-reverse-linear-min-max.png' || true
mkdir -p $(dirname '/swebench/image_assets/test_patch/test/fixtures/scale.time/ticks-reverse-linear.png')
curl -fsSL -o '/swebench/image_assets/test_patch/test/fixtures/scale.time/ticks-reverse-linear.png' 'https://raw.githubusercontent.com/chartjs/Chart.js/a7d909e3e0721895e0f9c12a0154e6c2fc42da12/test/fixtures/scale.time/ticks-reverse-linear.png' || true
mkdir -p $(dirname '/swebench/image_assets/test_patch/test/fixtures/scale.time/ticks-reverse-offset.png')
curl -fsSL -o '/swebench/image_assets/test_patch/test/fixtures/scale.time/ticks-reverse-offset.png' 'https://raw.githubusercontent.com/chartjs/Chart.js/a7d909e3e0721895e0f9c12a0154e6c2fc42da12/test/fixtures/scale.time/ticks-reverse-offset.png' || true
mkdir -p $(dirname '/swebench/image_assets/test_patch/test/fixtures/scale.time/ticks-reverse.png')
curl -fsSL -o '/swebench/image_assets/test_patch/test/fixtures/scale.time/ticks-reverse.png' 'https://raw.githubusercontent.com/chartjs/Chart.js/a7d909e3e0721895e0f9c12a0154e6c2fc42da12/test/fixtures/scale.time/ticks-reverse.png' || true
mkdir -p $(dirname '/swebench/image_assets/test_patch/test/fixtures/scale.timeseries/normalize.png')
curl -fsSL -o '/swebench/image_assets/test_patch/test/fixtures/scale.timeseries/normalize.png' 'https://raw.githubusercontent.com/chartjs/Chart.js/a7d909e3e0721895e0f9c12a0154e6c2fc42da12/test/fixtures/scale.timeseries/normalize.png' || true
mkdir -p $(dirname '/swebench/image_assets/test_patch/test/fixtures/scale.timeseries/source-auto.png')
curl -fsSL -o '/swebench/image_assets/test_patch/test/fixtures/scale.timeseries/source-auto.png' 'https://raw.githubusercontent.com/chartjs/Chart.js/a7d909e3e0721895e0f9c12a0154e6c2fc42da12/test/fixtures/scale.timeseries/source-auto.png' || true
mkdir -p $(dirname '/swebench/image_assets/test_patch/test/fixtures/scale.timeseries/source-data-offset-min-max.png')
curl -fsSL -o '/swebench/image_assets/test_patch/test/fixtures/scale.timeseries/source-data-offset-min-max.png' 'https://raw.githubusercontent.com/chartjs/Chart.js/a7d909e3e0721895e0f9c12a0154e6c2fc42da12/test/fixtures/scale.timeseries/source-data-offset-min-max.png' || true
mkdir -p $(dirname '/swebench/image_assets/test_patch/test/fixtures/scale.timeseries/source-data.png')
curl -fsSL -o '/swebench/image_assets/test_patch/test/fixtures/scale.timeseries/source-data.png' 'https://raw.githubusercontent.com/chartjs/Chart.js/a7d909e3e0721895e0f9c12a0154e6c2fc42da12/test/fixtures/scale.timeseries/source-data.png' || true
mkdir -p $(dirname '/swebench/image_assets/test_patch/test/fixtures/scale.timeseries/source-labels-offset-min-max.png')
curl -fsSL -o '/swebench/image_assets/test_patch/test/fixtures/scale.timeseries/source-labels-offset-min-max.png' 'https://raw.githubusercontent.com/chartjs/Chart.js/a7d909e3e0721895e0f9c12a0154e6c2fc42da12/test/fixtures/scale.timeseries/source-labels-offset-min-max.png' || true
mkdir -p $(dirname '/swebench/image_assets/test_patch/test/fixtures/scale.timeseries/source-labels.png')
curl -fsSL -o '/swebench/image_assets/test_patch/test/fixtures/scale.timeseries/source-labels.png' 'https://raw.githubusercontent.com/chartjs/Chart.js/a7d909e3e0721895e0f9c12a0154e6c2fc42da12/test/fixtures/scale.timeseries/source-labels.png' || true
mkdir -p $(dirname '/swebench/image_assets/test_patch/test/fixtures/scale.timeseries/ticks-reverse-max.png')
curl -fsSL -o '/swebench/image_assets/test_patch/test/fixtures/scale.timeseries/ticks-reverse-max.png' 'https://raw.githubusercontent.com/chartjs/Chart.js/a7d909e3e0721895e0f9c12a0154e6c2fc42da12/test/fixtures/scale.timeseries/ticks-reverse-max.png' || true
mkdir -p $(dirname '/swebench/image_assets/test_patch/test/fixtures/scale.timeseries/ticks-reverse-min-max.png')
curl -fsSL -o '/swebench/image_assets/test_patch/test/fixtures/scale.timeseries/ticks-reverse-min-max.png' 'https://raw.githubusercontent.com/chartjs/Chart.js/a7d909e3e0721895e0f9c12a0154e6c2fc42da12/test/fixtures/scale.timeseries/ticks-reverse-min-max.png' || true
mkdir -p $(dirname '/swebench/image_assets/test_patch/test/fixtures/scale.timeseries/ticks-reverse-min.png')
curl -fsSL -o '/swebench/image_assets/test_patch/test/fixtures/scale.timeseries/ticks-reverse-min.png' 'https://raw.githubusercontent.com/chartjs/Chart.js/a7d909e3e0721895e0f9c12a0154e6c2fc42da12/test/fixtures/scale.timeseries/ticks-reverse-min.png' || true
mkdir -p $(dirname '/swebench/image_assets/test_patch/test/fixtures/scale.timeseries/ticks-reverse.png')
curl -fsSL -o '/swebench/image_assets/test_patch/test/fixtures/scale.timeseries/ticks-reverse.png' 'https://raw.githubusercontent.com/chartjs/Chart.js/a7d909e3e0721895e0f9c12a0154e6c2fc42da12/test/fixtures/scale.timeseries/ticks-reverse.png' || true
mkdir -p /swebench/image_assets/problem_statement
curl -fsSL -o '/swebench/image_assets/problem_statement/62070777-17918600-b233-11e9-8f0a-fcfb41ff6fd8.png' 'https://user-images.githubusercontent.com/35506344/62070777-17918600-b233-11e9-8f0a-fcfb41ff6fd8.png' || true
EOF_793198e6251a


WORKDIR /testbed
