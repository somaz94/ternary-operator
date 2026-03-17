# Changelog

All notable changes to this project will be documented in this file.

## [v1.4.1](https://github.com/somaz94/ternary-operator/compare/v1.4.0...v1.4.1) (2026-03-17)

### Bug Fixes

- apache license -> mit license ([6c853a1](https://github.com/somaz94/ternary-operator/commit/6c853a137491e06db3b0d2fa00dec4a57a9574fa))
- skip major version tag deletion on first release ([b5c9c1c](https://github.com/somaz94/ternary-operator/commit/b5c9c1c1cfe4405c5e89da4912b196ee22875835))

### Code Refactoring

- improve code quality with method extraction, specific exceptions, and recursion guard ([b5257d9](https://github.com/somaz94/ternary-operator/commit/b5257d95acbd6d78363aa657db793d6ec2bec134))

### Documentation

- update CLAUDE.md with commit guidelines and language ([af5ddbd](https://github.com/somaz94/ternary-operator/commit/af5ddbd9d5543a3035e5ca8988a7026ef4dd8e04))
- update changelog ([ac6ab47](https://github.com/somaz94/ternary-operator/commit/ac6ab47b735e6a7e8cd6cbdb01485e99badfddb1))

### Continuous Integration

- use somaz94/contributors-action@v1 for contributors generation ([80097ff](https://github.com/somaz94/ternary-operator/commit/80097ff8f69aa6f784e19ef927cb6312701cf95e))
- use major-tag-action for version tag updates ([f6441b9](https://github.com/somaz94/ternary-operator/commit/f6441b9bce1d6b0b92108856242df9f223db4a65))
- migrate changelog generator to go-changelog-action ([d34b3f5](https://github.com/somaz94/ternary-operator/commit/d34b3f5ba52406245c5bc10c70ae2967734889bb))
- add dependabot auto-merge workflow ([71089e9](https://github.com/somaz94/ternary-operator/commit/71089e9563a8653d9feab97f26f2562eb8b498be))
- unify changelog-generator with flexible tag pattern ([2893798](https://github.com/somaz94/ternary-operator/commit/289379839dd473b0f66a43df1598a60257ede071))
- use conventional commit message in changelog-generator workflow ([24c33a7](https://github.com/somaz94/ternary-operator/commit/24c33a793d97b0101147a871a424ae8dd934cd50))

### Chores

- update .gitignore and .dockerignore for Python project ([7b2cffa](https://github.com/somaz94/ternary-operator/commit/7b2cffac112b8cf68ca4522aeef9a164c24f0b94))
- change license from MIT to Apache 2.0 ([450e4f4](https://github.com/somaz94/ternary-operator/commit/450e4f44038cf816c3342a50802d2c8106222176))

### Contributors

- somaz

<br/>

## [v1.4.0](https://github.com/somaz94/ternary-operator/compare/v1.3.2...v1.4.0) (2026-03-10)

### Bug Fixes

- **ci:** use python runner for local tests and add Makefile ([232c03f](https://github.com/somaz94/ternary-operator/commit/232c03fa99228483cee8cf5b9776864c117f24d1))
- **ci:** add pytest installation step to unit-test job ([535b9a8](https://github.com/somaz94/ternary-operator/commit/535b9a82662d6efc18ba797b9dc1b27184852909))

### Documentation

- update test counts to reflect new unit tests (73→89, 36→52) ([c941d8f](https://github.com/somaz94/ternary-operator/commit/c941d8f4ca6af535e9d1fe81592a5cba02ab20a5))
- update documentation to reflect current project state ([e9b3114](https://github.com/somaz94/ternary-operator/commit/e9b31140729bfb2a29d2ecb9934c9366d9d2a857))
- update README, docs, and action.yml to reflect current project state ([1f8dc9b](https://github.com/somaz94/ternary-operator/commit/1f8dc9bb500a65c55f27273d527a8c70e66178e8))
- add CLAUDE.md, CONTRIBUTORS.md, release.yml and update dockerignore ([a211e71](https://github.com/somaz94/ternary-operator/commit/a211e7149817629b4db2c9aad5389099ba3d8f24))
- add CLAUDE.md and update tests/README.md ([90c90ba](https://github.com/somaz94/ternary-operator/commit/90c90ba9bf47ae1cec7a3bfa9784540ca740b0c4))

### Tests

- add unit tests for _is_numeric and _parse_comparison methods ([4775922](https://github.com/somaz94/ternary-operator/commit/4775922773eb9bbad0aaea61fa78917a2036b6a9))
- add pytest unit tests with 91% coverage and remove emojis ([df0e2bf](https://github.com/somaz94/ternary-operator/commit/df0e2bf4e77e6640f13336f43826383498f8617f))

### Builds

- **deps:** bump docker/build-push-action from 6 to 7 ([6c450fb](https://github.com/somaz94/ternary-operator/commit/6c450fb5ba6991de976e899fd91d5acdedff4a2f))
- **deps:** bump docker/setup-buildx-action from 3 to 4 ([ec90993](https://github.com/somaz94/ternary-operator/commit/ec909932b0d76602288c31da4eb554a3a2e18fca))
- **deps:** bump actions/checkout from 5 to 6 ([d7e2e76](https://github.com/somaz94/ternary-operator/commit/d7e2e76ff07041af0d88a5fc33e80491536ebdd7))

### Continuous Integration

- refactor workflows to match project conventions ([5f3555f](https://github.com/somaz94/ternary-operator/commit/5f3555f40d9b318c8dc8052694f5b3dcaf912e00))

### Chores

- remove linter workflow and config files ([89c4e76](https://github.com/somaz94/ternary-operator/commit/89c4e76c11590cdcebce7e1cba9b824dc15d40f5))
- update prettier devcontainer feature reference ([3fd333c](https://github.com/somaz94/ternary-operator/commit/3fd333cdbbf964686e94f4c58559243b36dc209f))
- stale-issues, issue-greeting ([fc1440f](https://github.com/somaz94/ternary-operator/commit/fc1440f3a4c62785d563a265347687e504ccbf08))
- dockerignore ([7d8e231](https://github.com/somaz94/ternary-operator/commit/7d8e23151d03221b2c1646c0f7ab0086a3076857))
- release.yml ([ff50706](https://github.com/somaz94/ternary-operator/commit/ff50706c31dabad61da65e81e98cf1bc0d41b114))
- workflows ([e9845cb](https://github.com/somaz94/ternary-operator/commit/e9845cb80f78341fbae6e169f35fcf441181c655))
- changelog-generator.yml ([01003c2](https://github.com/somaz94/ternary-operator/commit/01003c2bc698c88f6008ed70e7cdd5e4309f6375))
- changelog-generator.yml ([b5017ac](https://github.com/somaz94/ternary-operator/commit/b5017acbc73fdb497b6367317582a474d733b43b))

### Security

- replace eval() with safe operator comparison in evaluator ([2cad2f1](https://github.com/somaz94/ternary-operator/commit/2cad2f16fc01a978857afb4f02715f524bd38068))

### Contributors

- somaz

<br/>

## [v1.3.2](https://github.com/somaz94/ternary-operator/compare/v1.3.1...v1.3.2) (2025-10-29)

### Code Refactoring

- src ([d5c3315](https://github.com/somaz94/ternary-operator/commit/d5c33150591f4de5ea3553d0d373dab1346ea3aa))

### Contributors

- somaz

<br/>

## [v1.3.1](https://github.com/somaz94/ternary-operator/compare/v1.3.0...v1.3.1) (2025-10-29)

### Code Refactoring

- Dockerfile, src ([c20678f](https://github.com/somaz94/ternary-operator/commit/c20678fe7e80d6df6e4d61bbc3718abbb0c0530c))

### Documentation

- docs/development.md ([dc2d6f1](https://github.com/somaz94/ternary-operator/commit/dc2d6f1533ec7b1bfcaa31d94313067dc019952c))

### Contributors

- somaz

<br/>

## [v1.3.0](https://github.com/somaz94/ternary-operator/compare/v1.2.0...v1.3.0) (2025-10-29)

### Code Refactoring

- entrypoint.py ([e830dbd](https://github.com/somaz94/ternary-operator/commit/e830dbd1f38f9d80846383f2cf61c396ef1aff07))
- entrypoint.py, ci.yml ([aeacf53](https://github.com/somaz94/ternary-operator/commit/aeacf53086f8daf964b5b1c9134f438239745076))

### Contributors

- somaz

<br/>

## [v1.2.0](https://github.com/somaz94/ternary-operator/compare/v1.1.0...v1.2.0) (2025-10-29)

### Bug Fixes

- backup/* ([041dd40](https://github.com/somaz94/ternary-operator/commit/041dd4090a46b4c9aa81d20adce020b9976dfc8f))
- changelog-generator.yml ([cecc6cd](https://github.com/somaz94/ternary-operator/commit/cecc6cd17c3a55314404e3455c2b0aad5916253c))
- backup/entrypoint.sh.bak ([9ec80f5](https://github.com/somaz94/ternary-operator/commit/9ec80f5b07a80a11e6c52e70838a8e874523d93a))
- ci.yml ([0395fa3](https://github.com/somaz94/ternary-operator/commit/0395fa3a75515651df05b655ef6c8b1bd11bbc42))

### Code Refactoring

- entrypoint.py, ci.yml,  add: tests ([d25647a](https://github.com/somaz94/ternary-operator/commit/d25647a9bfa1be71c60a6865c8ac204f974ca258))
- bash -> python ([8d8427c](https://github.com/somaz94/ternary-operator/commit/8d8427c2b429b27f26536a840740297017e19eb4))

### Builds

- **deps:** bump actions/checkout from 4 to 5 ([9f303fd](https://github.com/somaz94/ternary-operator/commit/9f303fdac6a9729325cf71b46cff8ccc72102fa4))
- **deps:** bump super-linter/super-linter from 7 to 8 ([71c9588](https://github.com/somaz94/ternary-operator/commit/71c9588c007fbf72e703f8e7772bc0c01e910e71))
- **deps:** bump alpine from 3.21 to 3.22 in the docker-minor group ([0fb718c](https://github.com/somaz94/ternary-operator/commit/0fb718c24abd04a8fb700a142ae1a0e6bd156d53))

### Chores

- entrypoint.py ([c17ab57](https://github.com/somaz94/ternary-operator/commit/c17ab5786cb62c41d230db6908c509271968ff31))
- entrypoint.py ([d85920a](https://github.com/somaz94/ternary-operator/commit/d85920a2c7253baed6afafd36bf92c3b2ba97f9e))
- entrypoint.py ([3a2d519](https://github.com/somaz94/ternary-operator/commit/3a2d5199a69d1b46f13d5f9981429290c6cb44e6))
- entrypoint.py ([74d3d76](https://github.com/somaz94/ternary-operator/commit/74d3d76062e18da4f0b8827c1cc33e28b14a4841))
- ci.yml, entrypoint.py ([329c6e8](https://github.com/somaz94/ternary-operator/commit/329c6e88bf130b306e01c0c018aacb5fe5c12465))
- entrypoint.py ([d60e245](https://github.com/somaz94/ternary-operator/commit/d60e245a22770f076cd3bdba25f62bf5706f8d3d))
- entrypoint.py ([b27514e](https://github.com/somaz94/ternary-operator/commit/b27514e9970ab0555a69321eb8d1b0f24d66e512))

### Add

- docs, & docs: README.md, chore: .gitignore, use-action.yml ([3652df3](https://github.com/somaz94/ternary-operator/commit/3652df3ca2f36ebf4c3b8efd36b522868419e1f5))
- gitlab-mirror.yml ([9321b42](https://github.com/somaz94/ternary-operator/commit/9321b42f3619e9cb8292cc3c5e2b50d62becb08a))

### Contributors

- somaz

<br/>

## [v1.1.0](https://github.com/somaz94/ternary-operator/compare/v1.0.4...v1.1.0) (2025-02-17)

### Bug Fixes

- entrypoint.sh ([67b67ca](https://github.com/somaz94/ternary-operator/commit/67b67cab54977286b86245a3b1df511a086a8850))
- changelog-generator.yml ([9c8e74a](https://github.com/somaz94/ternary-operator/commit/9c8e74aa4c2d28f9a61ab954e5cb1a389381ecb1))

### Add

- debug_mode ([b8d9547](https://github.com/somaz94/ternary-operator/commit/b8d9547ee0a46638ee57f5faee3e675e81bb5a7c))

### Contributors

- somaz

<br/>

## [v1.0.4](https://github.com/somaz94/ternary-operator/compare/v1.0.3...v1.0.4) (2025-02-14)

### Bug Fixes

- use-action.yml ([0f3792a](https://github.com/somaz94/ternary-operator/commit/0f3792ae9a51e76ce0dcc79cc68a04d562e4a0e5))
- ci.yml ([673a077](https://github.com/somaz94/ternary-operator/commit/673a07752bf16707db3763870487179dd488d1a0))
- ci.yml , action.yml, entrypoint.sh ([46a6997](https://github.com/somaz94/ternary-operator/commit/46a69976f6ee24646dfb578885af7a8954a193a3))
- ci.yml & use-action.yml ([84d2491](https://github.com/somaz94/ternary-operator/commit/84d2491bb2a66db60a834c195004e91fb652b091))

### Documentation

- README.md ([e4c4208](https://github.com/somaz94/ternary-operator/commit/e4c420856a8d7fcc10a493a5a72c19608f21ed42))

### Contributors

- somaz

<br/>

## [v1.0.3](https://github.com/somaz94/ternary-operator/compare/v1.0.2...v1.0.3) (2025-02-07)

### Bug Fixes

- github/workflows, docs: README.md ([f39abf8](https://github.com/somaz94/ternary-operator/commit/f39abf8283f05fed9fd555e63242c149f39fead3))

### Contributors

- somaz

<br/>

## [v1.0.2](https://github.com/somaz94/ternary-operator/compare/v1.0.1...v1.0.2) (2025-02-07)

### Features

- prettier ([3d78fa4](https://github.com/somaz94/ternary-operator/commit/3d78fa43c5107ebb1b2de67c721a678e74c93fab))
- fix linters ([057e855](https://github.com/somaz94/ternary-operator/commit/057e855cd8b137dea2971ab3617b97f6101b9ced))

### Bug Fixes

- entrypoint.sh ([0b98e4d](https://github.com/somaz94/ternary-operator/commit/0b98e4d4435b24958aa9ef4b640ef8046b32f867))
- entrypoint.sh ([c73d57b](https://github.com/somaz94/ternary-operator/commit/c73d57be06936ee3e4f4f6598c1f56ffadee8c87))
- entrypoint.sh ([c39377f](https://github.com/somaz94/ternary-operator/commit/c39377fb759b40f4a24938c8c67c803164514de3))
- entrypoint.sh ([b7eedde](https://github.com/somaz94/ternary-operator/commit/b7eedde559be362cec3c42127685892eba437491))
- github/workflows/* , entrypoint.sh ([a31588f](https://github.com/somaz94/ternary-operator/commit/a31588f3e46850e07110dd6270dd72b8df052160))
- .env.test ([9cca2c1](https://github.com/somaz94/ternary-operator/commit/9cca2c136e99ea3289a45aa9b4c95c39ed4e2550))

### Documentation

- README.md ([91fad35](https://github.com/somaz94/ternary-operator/commit/91fad356238d971a87e6c688fef0d24c635d8273))
- CODEOWNERS ([66e06c4](https://github.com/somaz94/ternary-operator/commit/66e06c41b312f4602c9cf1d23b5b00cf731263ce))
- README.md ([78ad5f5](https://github.com/somaz94/ternary-operator/commit/78ad5f5d6e6a26531a4fb7ae42aca8ea6b9d1d5e))
- README.md ([7668b62](https://github.com/somaz94/ternary-operator/commit/7668b62165a0f1ec628b71a6b608ceff54623713))
- README.md ([5b787bf](https://github.com/somaz94/ternary-operator/commit/5b787bf0ac6a2b0bc29ea4a04786f42e239fbab4))
- README.md ([36e4543](https://github.com/somaz94/ternary-operator/commit/36e4543b891c5808924ce52339bed2ace3ce77ea))

### Builds

- **deps:** bump janheinrichmerker/action-github-changelog-generator ([8988ab0](https://github.com/somaz94/ternary-operator/commit/8988ab051826cce3ee251bf61f0dbaab7767215d))
- **deps:** bump alpine from 3.20 to 3.21 in the docker-minor group ([dfc6c9c](https://github.com/somaz94/ternary-operator/commit/dfc6c9c2c76873e93a99274a05696b41f6977f59))
- **deps:** bump super-linter/super-linter from 6 to 7 ([8c0edd1](https://github.com/somaz94/ternary-operator/commit/8c0edd1c24258f8ee8d018cfd0b307ae363abecb))

### Chores

- fix changelog-generator.yml ([6f35705](https://github.com/somaz94/ternary-operator/commit/6f357058ecf4ea236d44c2827a1924bf7b6bca5c))
- fix Dokerfile ([dc748e1](https://github.com/somaz94/ternary-operator/commit/dc748e13fe41029c04ab297a4d6b81374df9066b))
- fix changelog workflow ([9d6e7d1](https://github.com/somaz94/ternary-operator/commit/9d6e7d12fcfb541da976b10eb222c25005395869))
- add changelog-gnerator workflow ([b7680a8](https://github.com/somaz94/ternary-operator/commit/b7680a8d8b1ccae35b07200e46ec786a86f9c8f4))
- fix Dockerfile pacakge version ([846902e](https://github.com/somaz94/ternary-operator/commit/846902eb8d7f6a614691bca5fda9319ccaad7e4f))

### Contributors

- somaz

<br/>

## [v1.0.1](https://github.com/somaz94/ternary-operator/compare/v1.0.0...v1.0.1) (2024-06-24)

### Bug Fixes

- use-action.yml ([2eb3bf9](https://github.com/somaz94/ternary-operator/commit/2eb3bf91b3ef543a357ec985ea45efe0d06788ca))
- entrypoint.sh ([c6cc9ba](https://github.com/somaz94/ternary-operator/commit/c6cc9ba985097be1b2791172ca00c1e46b64921f))
- entrypoint.sh ([41aa6dd](https://github.com/somaz94/ternary-operator/commit/41aa6dd8b845e7d65f220f4bae841211189ec598))
- entrypoint.sh ([f75d5b8](https://github.com/somaz94/ternary-operator/commit/f75d5b8d0831f8037fb21d00eb07cc24a5801a92))
- entrypoint.sh ([43684a0](https://github.com/somaz94/ternary-operator/commit/43684a0c4d193531fb81b3faa69bec5052fa954c))
- ci.yml ([e04d0e6](https://github.com/somaz94/ternary-operator/commit/e04d0e620be39e1be9c6fac57b03e999a5ea7cc6))
- ci.yml ([c862b23](https://github.com/somaz94/ternary-operator/commit/c862b23bc16880eabb64ced634594a441838985f))
- ci.yml & entrypoint.sh ([05f6fb7](https://github.com/somaz94/ternary-operator/commit/05f6fb7e0a047648acb6ba97882ae713f144e5ff))
- entrypoint.sh ([54366cd](https://github.com/somaz94/ternary-operator/commit/54366cd6ac582adff74bdf841ea27aea1fd56956))
- entrypoint.sh ([9e4546c](https://github.com/somaz94/ternary-operator/commit/9e4546ca756b560b4b2dc546b73b0e7a6db2c30d))
- entrypoint.sh ([9eda354](https://github.com/somaz94/ternary-operator/commit/9eda3543c3f7dbc6514802ae5c5e0d37cb6a49ba))
- entrypoint.sh ([5d36d9c](https://github.com/somaz94/ternary-operator/commit/5d36d9ce9bcdcff3241668ec47b4d51c73d1cf07))
- ci.yml & add: use-action.yml ([9532e52](https://github.com/somaz94/ternary-operator/commit/9532e529c2cd17f1ef4f4aa5d73d22b0b1f1caac))
- ci.yml & add: use-action.yml ([89001a1](https://github.com/somaz94/ternary-operator/commit/89001a16c98fbd48ec34591b4b02255db6dc64a6))
- action.yml ([b3c6778](https://github.com/somaz94/ternary-operator/commit/b3c67789a74ef642a99cda404899dda8e8c29ad2))
- ci.yml ([1e117b4](https://github.com/somaz94/ternary-operator/commit/1e117b4d040bcf63885ccbc780a67c4160cdd4f6))
- ci.yml ([ba33538](https://github.com/somaz94/ternary-operator/commit/ba335386da6bf98c1431df1bf4ba58e633743428))
- ci.yml ([d5465b9](https://github.com/somaz94/ternary-operator/commit/d5465b97633070601e6a6a8ed3d2d998d58b99a5))
- ci.yml & action.yml ([4becade](https://github.com/somaz94/ternary-operator/commit/4becadeb2e4df09d5fbc45a348894e7534d8d6c3))
- ci.yml ([3f7d37e](https://github.com/somaz94/ternary-operator/commit/3f7d37e36c96bc2fda7d229dc74f8ecb628f9c79))
- ci.yml & entrypoint.sh ([3501020](https://github.com/somaz94/ternary-operator/commit/350102089d569592ffb1f477cb2dc852daaa2e7f))
- entrypoint.sh ([7221adf](https://github.com/somaz94/ternary-operator/commit/7221adf7b1bb9af9fd2d0ea3725f90bcd40df3c2))
- ci.yml ([2b3011b](https://github.com/somaz94/ternary-operator/commit/2b3011b6ee90a00e68fb29ae1118ba6bdcbf0bc9))
- ci.yml ([4beb509](https://github.com/somaz94/ternary-operator/commit/4beb509dbe649120343f7678c030d264160cb4db))
- ci.yml ([acb5947](https://github.com/somaz94/ternary-operator/commit/acb5947e2229f65096966c753ec404ce4cdb241b))
- entrypoint.sh & ci.yml ([009cd75](https://github.com/somaz94/ternary-operator/commit/009cd756bcf30603921d322d7a00645503372da9))
- entrypoint.sh & ci.yml ([ca92035](https://github.com/somaz94/ternary-operator/commit/ca9203566699ef96f8bde9b9b4ce1b52047e79ad))
- entrypoint.sh & ci.yml ([d8d5b43](https://github.com/somaz94/ternary-operator/commit/d8d5b4336833fda4ae103e93122bab649bdd5e4b))
- entrypoint.sh & ci.yml ([aa790f3](https://github.com/somaz94/ternary-operator/commit/aa790f3a4d892a3844b9988582069e42ad1b0ce4))
- ci.yml & entrypoint.sh ([fceba7a](https://github.com/somaz94/ternary-operator/commit/fceba7a74a9de45de96454a0e64bbbec4bad5b16))

### Documentation

- README.md ([5bf67f4](https://github.com/somaz94/ternary-operator/commit/5bf67f4bd1383ff653bd41be5e77857a465522c4))
- README.md ([3a644d2](https://github.com/somaz94/ternary-operator/commit/3a644d2c98d5ccde8dd87b6a7cfa820521b1a7ce))
- README.md ([344e3b6](https://github.com/somaz94/ternary-operator/commit/344e3b6ec448830799ecbd912f905be13cf898ef))

### Contributors

- somaz

<br/>

## [v1.0.0](https://github.com/somaz94/ternary-operator/releases/tag/v1.0.0) (2024-06-20)

### Contributors

- somaz

<br/>

