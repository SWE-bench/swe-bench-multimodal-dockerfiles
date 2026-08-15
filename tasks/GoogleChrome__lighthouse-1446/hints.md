If you want to try the devtools patch out, you can try it via the new fancy devtools contrib workflow:

``` sh
# clone the standalone devtools frontend repo
git clone https://github.com/ChromeDevTools/devtools-frontend/
cd devtools-frontend
git checkout -b metrikz

# grab the unified patch of CL 2283793005
wget https://codereview.chromium.org/download/issue2283793005_1.diff
# adjust the paths, as our git clone is a subtree..
sed -i -e "s/third_party\/WebKit\/Source\/devtools\///" issue2283793005_1.diff
# apply the diff to working folder
git apply issue2283793005_1.diff

# start the _new_ devtools hacker webserver
npm run server
# open the standalone devtools (don't really need to debug a page)
open "http://localhost:8090/front_end/inspector.html?experiments=true"

# and now drag in a metrics-adorned trace into Timeline panel. 
# Profit!
```

_Attached: A zip of the trace I screenshotted above:_ [www.theverge.trace.json.zip](https://github.com/GoogleChrome/lighthouse/files/440468/www.theverge.com_2016-08-27T03-12-00.842Z0.trace.json.zip)

This works **really nice** using the above workflow. Took just a few mins to setup.

![screen shot 2016-08-26 at 10 09 05 pm](https://cloud.githubusercontent.com/assets/110953/18025277/cb0032f2-6bd9-11e6-97d7-50ff4275ec32.jpg)

Paul wins all the internet 🌟 🌟 🌟 today.

New, improved implementation (on the [exportmetricstotrace branch](https://github.com/GoogleChrome/lighthouse/tree/exportmetricstotrace)). Just using straight up measures means no devtools-side changes. :)

![image](https://cloud.githubusercontent.com/assets/39191/19011259/a3696d4e-8745-11e6-853d-dfad1eff8ae8.png)

Damn, that's slick. You're grouping them in to user timings? Just as useful as the other view :)
