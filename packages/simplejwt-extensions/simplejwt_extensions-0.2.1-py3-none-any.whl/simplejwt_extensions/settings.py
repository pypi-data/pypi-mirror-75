from rest_framework_simplejwt.settings import api_settings

api_settings.import_strings = (
    *api_settings.import_strings,
    'NEW_USER_CALLBACK',
)

api_settings.defaults = {
    **api_settings.defaults,
    'NEW_USER_CALLBACK': None,
}
