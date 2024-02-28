# CHANGELOG



## v0.1.1 (2024-02-28)

### Fix

* fix: filtering the jerk measurments (#5) ([`66678d4`](https://github.com/iftahnaf/ccr_ncap/commit/66678d419f2e9f33a46218eb48f3d67cbe7999ae))


## v0.1.0 (2024-02-28)

### Ci

* ci: add semantic release (#4) ([`cd3be4a`](https://github.com/iftahnaf/ccr_ncap/commit/cd3be4a8bf792933645024b57f5703d3253096d8))

### Documentation

* docs: add readme (#3)

* docs: adding readme

* docs: adding readme

* docs: update readme

* docs: update readme

* docs: update readme

* docs: update readme ([`9440b36`](https://github.com/iftahnaf/ccr_ncap/commit/9440b3633e14c14fb54db9e84abcd46ca66ac77c))

### Feature

* feat: adding lane detector ([`0c8a39c`](https://github.com/iftahnaf/ccr_ncap/commit/0c8a39cb5614886875758281655c2e07ffab43b9))

* feat: adding test_2 ([`c9b13e6`](https://github.com/iftahnaf/ccr_ncap/commit/c9b13e6035f20852f04005d8ee74dd2ffc873dea))

* feat: add analysis ([`85264ce`](https://github.com/iftahnaf/ccr_ncap/commit/85264ce45b050934ef6fa80cb73f3fe625f6bacd))

* feat: adding sanity check notebook ([`3adbb93`](https://github.com/iftahnaf/ccr_ncap/commit/3adbb93e2e8791fae58854debb5ad6fbe0dc4f40))

* feat: adding controller ([`9b75bb6`](https://github.com/iftahnaf/ccr_ncap/commit/9b75bb6cd86f1df61da3a9363d36893e7d2b9140))

* feat: spawnning two vehicles in 100m range ([`6102d7a`](https://github.com/iftahnaf/ccr_ncap/commit/6102d7a50f29d1e53c4a0a496a706488a805a3e6))

### Fix

* fix: almost working with front point only ([`9d63b30`](https://github.com/iftahnaf/ccr_ncap/commit/9d63b305dca093721afaaa902eb363ec37b93544))

* fix: working with 20 lane points ([`51777f7`](https://github.com/iftahnaf/ccr_ncap/commit/51777f753fcdf5437c81c7f3c4139ea99e139cf3))

* fix: correct point in the 2D ([`0110903`](https://github.com/iftahnaf/ccr_ncap/commit/0110903ba59222ecef528be002b8a7c4f4159337))

* fix: minor code cleanup ([`6ae3f16`](https://github.com/iftahnaf/ccr_ncap/commit/6ae3f1662a3ae47d90109b12530b448f91a1fdde))

* fix: drawing the images in pygame istead of cv2 ([`1012115`](https://github.com/iftahnaf/ccr_ncap/commit/101211527368554abd40d80745f5c75c650ae96b))

* fix: retriving camera specs from CameraManager ([`fc7e346`](https://github.com/iftahnaf/ccr_ncap/commit/fc7e3466fdc55589ec5154664b2b875e6222683c))

* fix: return 0 when no lanes detected ([`95d45b2`](https://github.com/iftahnaf/ccr_ncap/commit/95d45b2d479fef7ff7053a43b87a1281e3f12a31))

* fix: getting lanes in 2d projection ([`952e85e`](https://github.com/iftahnaf/ccr_ncap/commit/952e85e0f2cc1fda74dbc266f3a47be2072ea07b))

* fix: getting lanes in world coordinates ([`795dc5f`](https://github.com/iftahnaf/ccr_ncap/commit/795dc5f37a0815a4831d672453c6e71c68a2a7c3))

* fix: lane detection using carla.Waypoint ([`309db83`](https://github.com/iftahnaf/ccr_ncap/commit/309db8310960b30f9685f70880919c9d22ed73ae))

* fix: trying to fix the lane detector ([`2da402e`](https://github.com/iftahnaf/ccr_ncap/commit/2da402e3914832c38040603eade0dbe1f99b9494))

* fix: correct relative distance in the bb ([`4b244ab`](https://github.com/iftahnaf/ccr_ncap/commit/4b244aba28ced5856ffc05d451539447f0b47280))

* fix: correct relative distance ([`f590a5e`](https://github.com/iftahnaf/ccr_ncap/commit/f590a5e8158286c03733531ee4e765c20e4c169f))

* fix: verdicts logging ([`37b3ca0`](https://github.com/iftahnaf/ccr_ncap/commit/37b3ca03843ef6ed02f2e075e5cfac5c8582f774))

* fix: working version of the bounding box ([`3a4295b`](https://github.com/iftahnaf/ccr_ncap/commit/3a4295ba5268f898150bd90b9d0666625a60931c))

* fix: trying to draw bounding box ([`bbc6a9c`](https://github.com/iftahnaf/ccr_ncap/commit/bbc6a9c91217aff225d4a3bc039767c19a4fc188))

* fix: correct camera position ([`9ba6aff`](https://github.com/iftahnaf/ccr_ncap/commit/9ba6aff120c53699ed7d50d68e5ce09c2e5e1ced))

* fix: adding visualizer class ([`bb2c523`](https://github.com/iftahnaf/ccr_ncap/commit/bb2c5233ab24267b83fae91302c1328cb9db021f))

* fix: fine tuning for the controllers ([`52d7402`](https://github.com/iftahnaf/ccr_ncap/commit/52d7402396d1e845229267fe15b1f45f70d8cb44))

### Refactor

* refactor: add test_2 adjustments (#2)

* fix: rearrange the lane detector

* fix: remove unused function

* fix: trying to use lane width to correct lane detection

* fix: minor cleanup

* fix: minor cleanup

* feat: add readme ([`2920c4d`](https://github.com/iftahnaf/ccr_ncap/commit/2920c4d6478c786978f04d0dc39cf1be7ec27bf5))

* refactor: arrange `test_1` folder (#1)

* fix: rename scene class

* feat: adding camera spawnner

* fix: adding information about dynamics functions

* fix: adding hints to the functions in the controller

* fix: removing pygame window

* fix: adding hints for all functions

* fix: printing with logging

* fix: remove video recorder

* fix: adding simulation assets

* fix: fixing data rows

* feat: add docstring to the dynamics

* fix: adding docstrings

* fix: remove unused data file ([`071fda8`](https://github.com/iftahnaf/ccr_ncap/commit/071fda8568077fbfd0a9005e52c102e47208d7cc))

### Unknown

* refacor: rearranging the project&#39;s folders ([`76810a5`](https://github.com/iftahnaf/ccr_ncap/commit/76810a5674493c5da7332e5748f31e21362175f7))

* first commit ([`eb22545`](https://github.com/iftahnaf/ccr_ncap/commit/eb22545a1107713091e7129ce77c90e27c7a2fb0))
