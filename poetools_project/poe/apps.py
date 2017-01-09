from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _ # for signals


class PoeConfig(AppConfig):
    name = 'poe'
    


class ProfilesConfig(AppConfig):
    name = 'cmdbox.profiles'
    verbose_name = _('profiles')

    def ready(self):
        import cmdbox.profiles.signals  # noqa
