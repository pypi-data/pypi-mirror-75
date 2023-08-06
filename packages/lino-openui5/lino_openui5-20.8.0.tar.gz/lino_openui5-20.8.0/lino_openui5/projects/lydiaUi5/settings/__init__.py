from lino_tera.lib.tera.settings import *

class Site(Site):

    verbose_name = "Lino Tera for Lydia"
    demo_fixtures = 'std minimal_ledger demo demo_bookings payments demo2'.split()

    default_ui = 'lino_openui5.openui5'
    project_name = "openui5_lydia6"
    title = "Lydia Lino Open ui5 demo"

    languages = ['en', 'fr', 'de']
