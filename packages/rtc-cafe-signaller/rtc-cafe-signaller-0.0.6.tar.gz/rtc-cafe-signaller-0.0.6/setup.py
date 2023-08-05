try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


setup(
    name='rtc-cafe-signaller',
    version='v0.0.6',
    url='https://gitlab.com/rtc-cafe/rtc-cafe-signaller',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    packages=[
        'rtc_cafe_signaller',
        'rtc_cafe_signaller.wrappers',
    ],
)
