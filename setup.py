import os

from setuptools import setup

PLUGIN_ENTRY_POINT = 'ovos-tts-plugin-marytts = ovos_tts_plugin_marytts:MaryTTS'
SAMPLE_CONFIGS = 'ovos-tts-plugin-marytts.config = ' \
                 'ovos_tts_plugin_marytts:MaryTTSPluginConfig'
BASEDIR = os.path.abspath(os.path.dirname(__file__))


def package_files(directory):
    paths = []
    for (path, directories, filenames) in os.walk(directory):
        for filename in filenames:
            paths.append(os.path.join('..', path, filename))
    return paths

def get_version():
    """ Find the version of the package"""
    version = None
    version_file = os.path.join(BASEDIR, 'ovos_tts_plugin_marytts', 'version.py')
    major, minor, build, alpha = (None, None, None, None)
    with open(version_file) as f:
        for line in f:
            if 'VERSION_MAJOR' in line:
                major = line.split('=')[1].strip()
            elif 'VERSION_MINOR' in line:
                minor = line.split('=')[1].strip()
            elif 'VERSION_BUILD' in line:
                build = line.split('=')[1].strip()
            elif 'VERSION_ALPHA' in line:
                alpha = line.split('=')[1].strip()

            if ((major and minor and build and alpha) or
                    '# END_VERSION_BLOCK' in line):
                break
    version = f"{major}.{minor}.{build}"
    if alpha and int(alpha) > 0:
        version += f"a{alpha}"
    return version

def required(requirements_file):
    """ Read requirements file and remove comments and empty lines. """
    with open(os.path.join(BASEDIR, requirements_file), 'r') as f:
        requirements = f.read().splitlines()
        if 'MYCROFT_LOOSE_REQUIREMENTS' in os.environ:
            print('USING LOOSE REQUIREMENTS!')
            requirements = [r.replace('==', '>=').replace('~=', '>=') for r in requirements]
        return [pkg for pkg in requirements
                if pkg.strip() and not pkg.startswith("#")]
    
setup(
    name='ovos_tts_plugin_marytts',
    version=get_version(),
    description='A marytts plugin for OpenVoiceOS',
    url='https://github.com/OpenVoiceOS/ovos-tts-plugin-marytts',
    author='jarbasAi',
    author_email='jarbasai@mailfence.com',
    license='Apache2',
    packages=['ovos_tts_plugin_marytts'],
    install_requires=required("requirements/requirements.txt"),
    package_data={'': package_files('ovos_tts_plugin_marytts')},
    zip_safe=True,
    classifiers=[
        'Intended Audience :: Developers',
        'Topic :: Text Processing :: Linguistic',
        'Programming Language :: Python :: 3.6',
    ],
    keywords='mycroft plugin tts',
    entry_points={'mycroft.plugin.tts': PLUGIN_ENTRY_POINT,
                  'mycroft.plugin.tts.config': SAMPLE_CONFIGS}
)
