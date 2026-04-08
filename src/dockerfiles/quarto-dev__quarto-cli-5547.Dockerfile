
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

ENV NODE_VERSION 18.17.1
ENV NODE_PATH $NVM_DIR/v$NODE_VERSION/lib/node_modules
ENV PATH $NVM_DIR/versions/node/v$NODE_VERSION/bin:$PATH

RUN <<EOF_556a5970cd1f
#!/bin/bash
set -euxo pipefail
apt-get update
apt-get install -y libffi-dev zip unzip python3 python3-pip python3.10-distutils r-base-core poppler-utils libxml2-utils cmake
rm -rf /var/lib/apt/lists/*
export NODE_VERSION=18.17.1
source $NVM_DIR/nvm.sh
nvm install $NODE_VERSION
nvm alias default $NODE_VERSION
nvm use default
add-apt-repository ppa:deadsnakes/ppa
apt-get update
apt-get install -y python3.9
ln -sf /usr/bin/python3.9 /usr/bin/python
apt-get install -y python2
echo "export NODE_PATH=$NVM_DIR/v18.17.1/lib/node_modules" >> /etc/environment
echo "export PATH=$NVM_DIR/versions/node/v18.17.1/bin:$PATH" >> /etc/environment
source $NVM_DIR/nvm.sh && node -v
source $NVM_DIR/nvm.sh && npm -v
python -V
python2 -V
EOF_556a5970cd1f


RUN <<EOF_e3e02d4ec4f6
#!/bin/bash
set -euxo pipefail
wget https://julialang-s3.julialang.org/bin/linux/x64/1.9/julia-1.9.3-linux-x86_64.tar.gz
tar zxvf julia-1.9.3-linux-x86_64.tar.gz
mv julia-1.9.3/ /opt/
ln -s /opt/julia-1.9.3/bin/julia /usr/local/bin/julia
wget -qO- 'https://yihui.org/tinytex/install-bin-unix.sh' | sh && ln -sf $HOME/.TinyTeX/bin/x86_64-linux/* /usr/local/bin/
export PATH=$HOME/.TinyTeX/bin/x86_64-linux:$PATH && tlmgr install a4wide achemso adjustbox ae algorithmicx algorithms apacite appendix awesomebox babel-english babel-french bbm-macros beamer biblatex biber breakurl caption carlisle catoptions ccicons changepage charter chemgreek cite cleveref collectbox colorprofiles colortbl comment count1to courier crop csquotes currfile datetime dblfloatfix doclicense draftwatermark eepic endfloat endnotes enumitem environ epsf epstopdf-pkg eso-pic esvect etex-pkg eurosym everysel everyshi expex extsizes fancyhdr fancyvrb filemod float floatflt floatrow fmtcount fontawesome5 fontaxes fontspec footmisc forarray fp fpl framed gincltex grfext grffile hardwrap hyperxmp hyphen-english hyphen-french hyphenat ifmtarg jknapltx kastrup koma-script langsci lastpage latex-lab latexindent lettrine libertine lineno lipsum listings logreq ltxkeys ly1 lualatex-math makecell makecmds makeindex marginnote marvosym mathalpha mathpazo mathspec mathtools mdframed memoir metalogo mhchem microtype minifp mnras morefloats moreverb multirow multitoc mweights natbib ncntrsbk needspace newfloat newtx ntgclass oberdiek palatino paralist parskip pbox pdfcol pdflscape pdfmanagement-testphase pdfpages pdfsync pgf picinpar placeins polyglossia prelim2e preprint preview psfrag ragged2e realscripts revtex4-1 roboto rsfs sauerj sectsty selnolig seqsplit setspace sidecap sidenotes siunitx soul srcltx standalone stix stmaryrd sttools subfig subfigure svn-prov tabto-ltx tabu tcolorbox tex-gyre texcount textcase thmtools threeparttable threeparttablex thumbpdf tikzfill tipa titlesec totcount totpages translator trimspaces tufte-latex ucs ulem units upquote urlbst varwidth vmargin vruler wallpaper wrapfig xargs xifthen xltxtra xpatch xstring xwatermark xypic zapfchan
R -e "install.packages(c('rmarkdown', 'knitr', 'jsonlite'), repos='https://cloud.r-project.org', quiet=TRUE)"
pip3 install --user pipenv
pip3 install nbformat
pip3 install nbclient
pip3 install pandocfilters
pip3 install shiny
pip3 install pyyaml
pip3 install setuptools
pip3 install numpy
pip3 install seaborn
pip3 install matplotlib
pip3 install bokeh
pip3 install bokeh_sampledata
pip3 install ipyleaflet
pip3 install pandas
pip3 install itables
pip3 install pexpect
pip3 install ptyprocess
pip3 install appnope
pip3 install ipykernel
EOF_e3e02d4ec4f6


RUN <<EOF_863380811d96
#!/bin/bash
set -euxo pipefail
git clone -o origin https://github.com/quarto-dev/quarto-cli /testbed
cd /testbed
git reset --hard fa057a6f3648aedf995952287449be08fb3bbdee
git remote remove origin
TARGET_EPOCH=$(git show -s --format=%ct fa057a6f3648aedf995952287449be08fb3bbdee)
git tag -l | while read tag; do TAG_COMMIT=$(git rev-list -n 1 "$tag"); TAG_EPOCH=$(git show -s --format=%ct "$TAG_COMMIT"); if [ "$TAG_EPOCH" -gt "$TARGET_EPOCH" ]; then git tag -d "$tag"; fi; done
git branch -D $(git branch | grep -v "^\*") 2>/dev/null || true
git reflog expire --expire=now --all
cd - || true
chmod -R 777 /testbed
cd /testbed
git clean -fdxq
source $NVM_DIR/nvm.sh
ls .
[ -f configure.sh ] || ./configure-linux.sh
[ -f configure-linux.sh ] || ./configure.sh
cd tests
sed -i 's/quarto install.*tinytex/true/' configure-test-env.sh 2>/dev/null || true
./configure-test-env.sh || true
cd ..
EOF_863380811d96


COPY src/image_assets/quarto-dev__quarto-cli-5547/ /swebench/image_assets/

WORKDIR /testbed
