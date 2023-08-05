###
# Author : Betacodings
# Author : info@betacodings.com
# Maintainer By: Emmanuel Martins
# Maintainer Email: emmamartinscm@gmail.com
# Created by Betacodings on 2019.
###


import sys

VERSION = (1, 0, 'a', 1)

if VERSION[2] and VERSION[3]:
    VERSION_TEXT = '{0}.{1}.{2}{3}'.format(*VERSION)
else:
    VERSION_TEXT = '{0}.{1}'.format(*VERSION[0:1])

VERSION_EXTRA = ''
LICENSE = 'GPL3'
EDITION = ''  # Added in package names, after the version
KEYWORDS = "flash message, boostrap flash, bootstrap pytonik,  mvc, oop, module, python, framework, flash, message, web, app, pytonik, web development"

PYVERSION_MA = sys.version_info.major
PYVERSION_MI = sys.version_info.minor

AUTHOR = "Emmanuel Essien"
ORG = "Pytonik"
URL = "https://github.com/emmamartins/FlashBootstrap"
NAME = "FlashBootstrap"
