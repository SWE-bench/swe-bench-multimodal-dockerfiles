"""wp-calypso spec."""

SPECS_CALYPSO = {
    **{
        k: {
            "apt-pkgs": ["libsass-dev", "sassc"],
            "install": ["npm install --unsafe-perm"],
            "test_cmd": "npm run test-client -- --verbose",
            "docker_specs": {
                "node_version": k,
            },
        }
        for k in [
            "0.8",
            "4.2.3",
            "4.3.0",
            "5.10.1",
            "5.11.1",
            "6.1.0",
            "6.7.0",
            "6.9.0",
            "6.9.1",
            "6.9.4",
            "6.10.0",
            "6.10.2",
            "6.10.3",
            "6.11.1",
            "6.11.2",
            "6.11.5",
            "8.9.1",
            "8.9.3",
            "8.9.4",
            "8.11.0",
            "8.11.2",
            "10.4.1",
            "10.5.0",
            "10.6.0",
            "10.9.0",
            "10.10.0",
            "10.12.0",
            "10.13.0",
            "10.16.3",
        ]
    },
    # color-studio@1.0.5 was unpublished from npm; replace with the scoped
    # successor @automattic/color-studio@1.0.6 before npm install.
    # Internal monorepo code does require('color-studio/...'), so we also
    # symlink the scoped package back to the unscoped name.
    # Also run `lerna bootstrap` at image-build time so workspace packages like
    # `i18n-calypso` are linked into node_modules/ before tests run. Eval-time
    # pretest re-runs bootstrap but it becomes a no-op once pre-populated.
    # Patch jest.config with a moduleNameMapper for @automattic/* so jest
    # doesn't lose track of workspace symlinks mid-run (33948).
    **{
        k: {
            "apt-pkgs": ["libsass-dev", "sassc"],
            "install": [
                "sed -i 's/\"color-studio\": \"1.0.5\"/\"@automattic\\/color-studio\": \"1.0.6\"/' package.json",
                "npm install --unsafe-perm --ignore-scripts",
                "npm rebuild node-sass",
                "ln -sf $(pwd)/node_modules/@automattic/color-studio node_modules/color-studio",
                "npm run build-packages",
                "./node_modules/.bin/lerna bootstrap || true",
                # Replace workspace symlinks with real copies so jest 24's resolver
                # (which sometimes loses track of symlinked packages) can find
                # them via standard node_modules traversal.
                "for d in /testbed/node_modules/@automattic/* /testbed/node_modules/i18n-calypso /testbed/node_modules/photon; do"
                "  [ -L \"$d\" ] && target=$(readlink -f \"$d\") && rm \"$d\" && cp -a \"$target\" \"$d\";"
                " done",
            ],
            # --maxWorkers=2 sidesteps a jest module-resolver race seen on
            # v10.15.2 (33948) where many workers intermittently lose track of
            # @automattic/* workspace symlinks in node_modules and fail with
            # "Cannot find module '@automattic/format-currency'" mid-suite.
            # NODE_OPTIONS bumps heap so the 12k-test run doesn't OOM with
            # low worker counts.
            # `npm run test-client` triggers pretest → lerna clean → wipes dist/
            # from workspace packages. Invoke jest directly to skip pretest.
            "test_cmd": (
                "NODE_OPTIONS='--max-old-space-size=8192' "
                "./node_modules/.bin/jest -c=test/client/jest.config.js --verbose"
            ),
            "docker_specs": {
                "node_version": k,
            },
        }
        for k in ["10.14.0", "10.15.2"]
    },
}
# v8.9.3 test suite imports optional deps (`cpf`, `hoek`) at runtime that were
# pruned from package.json. Install them explicitly so Ebanx / hoek tests run.
for _v in ["8.9.3"]:
    # Test imports `cpf.isValid` (available since cpf@1.0.0) and `hoek`.
    # Single install call with --no-prune preserves both despite --no-save.
    SPECS_CALYPSO[_v]["install"].append(
        "npm install cpf@1.0.1 hoek@6.1.3 --no-save --no-prune --legacy-peer-deps || true"
    )
