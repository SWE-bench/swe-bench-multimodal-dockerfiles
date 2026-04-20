"""
Repo-version-to-spec mapping for the SWE-bench Multimodal generator.

The 7 multilingual JS repos (babel, vuejs, docusaurus, immutable-js, three.js,
preact, axios) live in `swe-bench-multilingual-dockerfiles` and are intentionally
omitted here.
"""

from sb_dockerfile_gen.specs.bpmn_js import SPECS_BPMN_JS
from sb_dockerfile_gen.specs.carbon import SPECS_CARBON
from sb_dockerfile_gen.specs.chartjs import SPECS_CHART_JS
from sb_dockerfile_gen.specs.eslint import SPECS_ESLINT
from sb_dockerfile_gen.specs.grommet import SPECS_GROMMET
from sb_dockerfile_gen.specs.highlightjs import SPECS_HIGHLIGHTJS
from sb_dockerfile_gen.specs.lighthouse import SPECS_LIGHTHOUSE
from sb_dockerfile_gen.specs.marked import SPECS_MARKED
from sb_dockerfile_gen.specs.next import SPECS_NEXT
from sb_dockerfile_gen.specs.openlayers import SPECS_OPENLAYERS
from sb_dockerfile_gen.specs.p5_js import SPECS_P5_JS
from sb_dockerfile_gen.specs.prettier import SPECS_PRETTIER
from sb_dockerfile_gen.specs.prism import SPECS_PRISM
from sb_dockerfile_gen.specs.quartocli import SPECS_QUARTOCLI
from sb_dockerfile_gen.specs.react_pdf import SPECS_REACT_PDF
from sb_dockerfile_gen.specs.scratch import SPECS_SCRATCH
from sb_dockerfile_gen.specs.wp_calypso import SPECS_CALYPSO

MAP_REPO_VERSION_TO_SPECS_JS = {
    # Dev split
    "Automattic/wp-calypso": SPECS_CALYPSO,
    "chartjs/Chart.js": SPECS_CHART_JS,
    "markedjs/marked": SPECS_MARKED,
    "processing/p5.js": SPECS_P5_JS,
    "diegomura/react-pdf": SPECS_REACT_PDF,
    # Test split
    "alibaba-fusion/next": SPECS_NEXT,
    "bpmn-io/bpmn-js": SPECS_BPMN_JS,
    "carbon-design-system/carbon": SPECS_CARBON,
    "eslint/eslint": SPECS_ESLINT,
    "GoogleChrome/lighthouse": SPECS_LIGHTHOUSE,
    "grommet/grommet": SPECS_GROMMET,
    "highlightjs/highlight.js": SPECS_HIGHLIGHTJS,
    "openlayers/openlayers": SPECS_OPENLAYERS,
    "prettier/prettier": SPECS_PRETTIER,
    "PrismJS/prism": SPECS_PRISM,
    "quarto-dev/quarto-cli": SPECS_QUARTOCLI,
    "scratchfoundation/scratch-gui": SPECS_SCRATCH,
}
