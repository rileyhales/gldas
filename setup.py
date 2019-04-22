import os
from setuptools import setup, find_packages
from tethys_apps.app_installation import custom_develop_command, custom_install_command

# -- Apps Definition -- #
app_package = 'gldas'
release_package = 'tethysapp-' + app_package
app_class = 'gldas.app:Gldas'
app_package_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'tethysapp', app_package)

# -- Python Dependencies -- #
dependencies = ['netCDF4', 'numpy']

setup(
    name=release_package,
    version='2.0.0',
    tags='&quot;NASA&quot;, &quot;GLDAS&quot;, &quot;LDAS&quot;, &quot;charts&quot;, &quot;maps&quot;, &quot;teries&quot;',
    description='Visualizes GLDAS data through maps and charts',
    long_description='',
    keywords='GLDAS',
    author='Riley Hales',
    author_email='rileyhales1@gmail.com',
    url='rileyhales.com',
    license='Mozilla Public License Version 2.0',
    packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
    namespace_packages=['tethysapp', 'tethysapp.' + app_package],
    include_package_data=True,
    zip_safe=False,
    install_requires=dependencies,
    cmdclass={
        'install': custom_install_command(app_package, app_package_dir, dependencies),
        'develop': custom_develop_command(app_package, app_package_dir, dependencies)
    }
)
