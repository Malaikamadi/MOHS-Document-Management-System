from django.utils.translation import ugettext_lazy as _

from mayan.apps.common.apps import MayanAppConfig


class MohsApp(MayanAppConfig):
    app_namespace = 'mohs'
    app_url = None
    has_rest_api = False
    has_tests = False
    name = 'mayan.apps.mohs'
    verbose_name = _('MoHS (Sierra Leone) configuration')
