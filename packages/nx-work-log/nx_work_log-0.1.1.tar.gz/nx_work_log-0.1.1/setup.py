from setuptools import setup
import pathlib

here = pathlib.Path(__file__).parent.resolve()

# Get the long description from the README file
long_description = (here / 'README.md').read_text(encoding='utf-8')

setup(
    name='nx_work_log',
    description='NX Solutions Work Log',
    long_description=long_description,
    long_description_content_type='text/markdown',

    url='https://github.com/xanderhendriks/nx-work-log',

    author='Xander Hendriks',
    author_email='xander.hendriks@nx-solutions.com',

    classifiers=[  # Optional
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Microsoft :: Windows",
        'Programming Language :: Python :: 3 :: Only',
    ],

    packages=['nx_work_log'],

    python_requires='>=3.6',
    install_requires=['pywin32'],
    setup_requires=[
        "setuptools_scm",
        "wheel",
    ],

    extras_require={
        'dev': ['check-manifest'],
        'test': ['pytest'],
    },

    package_data={
        'nx_work_log': ['nx_work_log.rc', 'SysTrayPaused.ico', 'SysTrayRunning.ico'],
    },

    entry_points={
        'gui_scripts': [
            'nxworklog=nx_work_log.win_app:main',
        ],
    },

    project_urls={
        'Bug Reports': 'https://github.com/xanderhendriks/nx-work-log/issues',
        'Source': 'https://github.com/xanderhendriks/nx-work-log',
    },

    use_scm_version={
        'relative_to': __file__,
        'version_scheme': 'post-release',
        'write_to': 'nx_work_log/version.py',
        'local_scheme': 'no-local-version'
    },
)
