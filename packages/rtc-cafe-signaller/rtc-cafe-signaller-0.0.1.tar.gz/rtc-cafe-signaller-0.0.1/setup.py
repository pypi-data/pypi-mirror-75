try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


setup(
    name='rtc-cafe-signaller',
    version='v0.0.1',
    url='https://gitlab.com/rtc-cafe/rtc-cafe-signaller',
    description='rtc-cafe signaller',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    keywords='rtc-cafe flask-socketio socketio webrtc',
    packages=[
        'rtc_cafe_signaller',
    ],
)
