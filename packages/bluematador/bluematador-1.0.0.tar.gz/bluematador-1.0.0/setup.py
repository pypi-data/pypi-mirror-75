from distutils.core import setup

setup(
    name='bluematador',
    version='1.0.0',
    packages=['bluematador'],
    license='MIT',
    description='Send StatsD-style custom metrics to your Blue Matador account.',
    url='https://github.com/bluematador/bluematador-metrics-client-python',
    download_url='https://github.com/bluematador/bluematador-metrics-client-python/archive/v1.0.0.tar.gz',
    author='Blue Matador Dev',
    author_email='dev@bluematador.com',
    keywords=['bluematador'],
    install_requires=[
        'statsd-telegraf',
    ],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ]
)
