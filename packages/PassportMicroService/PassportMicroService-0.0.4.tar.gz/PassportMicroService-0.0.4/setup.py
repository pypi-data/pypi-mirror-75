from setuptools import setup, find_packages

setup(
    name='PassportMicroService',
    version='0.0.4',
    description=(
      'passport-micro-service'
    ),
    author='NoahWang',
    author_email='234082230@qq.com',
    maintainer='noahwang',
    maintainer_email='234082230@qq.com',
    license='',
    install_requires=['passportsdk'],
    packages=find_packages(
        'src'
    ),
    package_dir={'': 'src'},
    include_package_data=True,
    zip_safe=False
)
