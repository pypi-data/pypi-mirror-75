from setuptools import setup, find_packages


try:
    long_description = open('README.md', encoding='utf8').read()
except Exception as e:
    long_description = ''


setup(
    name='tisdk',
    version='0.0.33',
    description='python sdk of taiqiyun',
    long_description=long_description,
    long_description_content_type='text/markdown',
    install_requires=[
        'requests>=2.22.0',
        # 'pycrypto>=2.6.1',
    ],
    # py_modules=['tisdk'],
    packages=find_packages(),
    entry_points={
        'console_scripts': ['tireq=tisdk:main'],
    },
    include_package_data=True,
)
