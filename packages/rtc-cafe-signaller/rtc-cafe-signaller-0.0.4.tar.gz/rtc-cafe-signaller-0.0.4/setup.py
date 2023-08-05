from setuptools import setup

setup(
    name='rtc-cafe-signaller',
    version='v0.0.4',
    url='https://gitlab.com/rtc-cafe/rtc-cafe-signaller',
    description='rtc-cafe signaller',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    keywords='rtc-cafe flask-socketio socketio webrtc',
    install_requires=[
        'flask',
        'flask-socketio',
    ],
    packages=[
        'rtc_cafe_signaller',
    ],
)
