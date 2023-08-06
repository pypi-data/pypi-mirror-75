# -*- coding: UTF-8 -*-
# Copyright 2015-2018 Rumma & Ko Ltd
# License: BSD (see file COPYING for details)

import datetime

from lino_noi.lib.noi.settings import *


class Site(Site):

    default_ui = 'lino_openui5.openui5'
    project_name = "openui5_teamUi5"
    title = "Lino Noi Open Ui5 demo"

    the_demo_date = datetime.date(2020, 5, 23)

    languages = "en de fr"
    # readonly = True
    # catch_layout_exceptions = False

    # use_linod = True
    # use_ipdict = True
    # use_websockets = True
    # use_experimental_features = True
    # default_ui = 'lino_extjs6.extjs6'
    # default_ui = 'lino.modlib.bootstrap3'
    # default_ui = 'lino_openui5.openui5'
    # default_ui = 'lino_react.react'
