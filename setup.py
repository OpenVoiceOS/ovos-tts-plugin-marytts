from setuptools import setup, find_packages

PLUGIN_ENTRY_POINT = 'ovos-tts-plugin-marytts = ovos_tts_plugin_marytts:MaryTTS'

setup(
    name='ovos-tts-plugin-marytts',
    version="0.0.1",
    description='A marytts plugin for OpenVoiceOS',
    url='https://github.com/OpenVoiceOS/ovos-tts-plugin-marytts',
    author='jarbasAi',
    author_email='jarbasai@mailfence.com',
    license='Apache2',
    packages=find_packages(),
    install_requires=["ovos-plugin-manager~=0.0"],
    zip_safe=True,
    classifiers=[
        'Intended Audience :: Developers',
        'Topic :: Text Processing :: Linguistic',
        'Programming Language :: Python :: 3.6',
    ],
    keywords='mycroft plugin tts',
    entry_points={'mycroft.plugin.tts': PLUGIN_ENTRY_POINT}
)
