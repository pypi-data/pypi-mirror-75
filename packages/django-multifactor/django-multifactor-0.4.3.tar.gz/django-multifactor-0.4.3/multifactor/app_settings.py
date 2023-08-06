from django.conf import settings

mf_settings = getattr(settings, 'MULTIFACTOR', {})

mf_settings['LOGIN_CALLBACK'] = mf_settings.get('LOGIN_CALLBACK', False)
mf_settings['RECHECK'] = mf_settings.get('RECHECK', True)
mf_settings['RECHECK_MIN'] = mf_settings.get('RECHECK_MIN', 60 * 60 * 3)
mf_settings['RECHECK_MAX'] = mf_settings.get('RECHECK_MAX', 60 * 60 * 6)

mf_settings['FIDO_SERVER_ID'] = mf_settings.get('FIDO_SERVER_ID', 'example.com')
mf_settings['FIDO_SERVER_NAME'] = mf_settings.get('FIDO_SERVER_NAME', 'Django App')
mf_settings['FIDO_SERVER_ICON'] = mf_settings.get('FIDO_SERVER_ICON', None)
mf_settings['TOKEN_ISSUER_NAME'] = mf_settings.get('TOKEN_ISSUER_NAME', 'Django App')
mf_settings['U2F_APPID'] = mf_settings.get('U2F_APPID', 'https://example.com')

mf_settings['FACTORS'] = mf_settings.get('FACTORS', ['FIDO2', 'U2F', 'TOTP'])

mf_settings['FALLBACKS'] = mf_settings.get('FALLBACKS', {
    'email': (lambda user: user.email, 'multifactor.factors.fallback.send_email'),
})
