# Copyright (c) 2015 Nicolas JOUANIN
#
# See the file license.txt for copying permission.

from setuptools import setup, find_packages
from hbmqtt.version import get_version

setup(
    name="hbmqtt-master2.2",
    version=get_version(),
    description="MQTT client/broker using Python 3.6 asyncio library",
    author="Zhirui Wang",
    author_email='nico@beerfactory.org',
    url="https://github.com/beerfactory/hbmqtt",
    license='MIT',
    packages=find_packages(exclude=['tests']),
    include_package_data=True,
    platforms='all',
    install_requires=[
        'transitions',
        'websockets',
        'passlib',
        'docopt',
        'pyyaml'
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: POSIX',
        'Operating System :: MacOS',
        'Operating System :: Microsoft :: Windows',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Communications',
        'Topic :: Internet'
    ],
    entry_points={
        'hbmqtt.test.plugins': [
            'test_plugin = tests.plugins.test_manager:TestPlugin',
            'event_plugin = tests.plugins.test_manager:EventTestPlugin',
            'packet_logger_plugin = hbmqtt.plugins.logging:PacketLoggerPlugin',
        ],
        'hbmqtt.broker.plugins': [
            # 'event_logger_plugin = hbmqtt.plugins.logging:EventLoggerPlugin',
            'packet_logger_plugin = hbmqtt.plugins.logging:PacketLoggerPlugin',
            'auth_anonymous = hbmqtt.plugins.authentication:AnonymousAuthPlugin',
            'auth_file = hbmqtt.plugins.authentication:FileAuthPlugin',
            'topic_taboo = hbmqtt.plugins.topic_checking:TopicTabooPlugin',
            'topic_acl = hbmqtt.plugins.topic_checking:TopicAccessControlListPlugin',
            'broker_sys = hbmqtt.plugins.sys.broker:BrokerSysPlugin',
        ],
        'hbmqtt.client.plugins': [
            'packet_logger_plugin = hbmqtt.plugins.logging:PacketLoggerPlugin',
        ],
        'console_scripts': [
            'hbmqtt2 = scripts.broker:main',
            'hbmqtt_pub = scripts.publish:main',
            'hbmqtt_sub = scripts.subscribe:main',
        ]
    }
)
