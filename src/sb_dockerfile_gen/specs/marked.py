"""marked spec."""

# Jasmine's default reporter only emits dots for passing tests. Install a
# tiny custom reporter that logs `JASMINE_TEST: <status> :: <fullName>` per
# spec so the parser can detect passes (not just failures).
MARKED_JASMINE_REPORTER_SETUP = (
    "mkdir -p test/helpers && "
    "printf '%s\\n' "
    "\"jasmine.getEnv().addReporter({ specDone: function(r){ "
    "console.log('JASMINE_TEST: ' + r.status + ' :: ' + r.fullName); } });\" "
    "> test/helpers/jasmine_names.js && "
    "python3 -c \"import json; p='jasmine.json'; d=json.load(open(p)); "
    "h=d.get('helpers', []); "
    "(h.append('helpers/jasmine_names.js') if 'helpers/jasmine_names.js' not in h else None); "
    "d['helpers']=h; json.dump(d, open(p,'w'), indent=2)\""
)
SPECS_MARKED = {
    **{
        k: {
            "install": ["npm install", MARKED_JASMINE_REPORTER_SETUP],
            "test_cmd": "./node_modules/.bin/jasmine --no-color --config=jasmine.json",
            "docker_specs": {
                "node_version": "12.22.12",
            },
        }
        for k in [
            "0.3",
            "0.5",
            "0.6",
            "0.7",
            "1.0",
            "1.1",
            "1.2",
            "2.0",
            "3.9",
            "4.0",
            "4.1",
            "5.0",
        ]
    }
}
for v in ["4.0", "4.1", "5.0"]:
    SPECS_MARKED[v]["docker_specs"]["node_version"] = "20.16.0"
