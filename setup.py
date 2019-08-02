import os
from setuptools import setup, find_packages
from tethys_apps.app_installation import custom_develop_command, custom_install_command

# -- Apps Definition -- #
app_package = 'gldas'
release_package = 'tethysapp-' + app_package
app_class = 'gldas.app:Gldas'
app_package_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'tethysapp', app_package)

# -- Python Dependencies -- #
dependencies = ['netCDF4', 'numpy', 'pandas', 'rasterstats', 'rasterio']

setup(
    name=release_package,
    version='3',
    tags='NASA, GLDAS, LDAS, charts, maps, timeseries',
    description='Visualizes GLDAS data through maps and charts',
    long_description='Shows time-animated maps and timeseries plots of monthly average, 1/4 degree resolution, '
                     'GLDAS data sets from NASA LDAS and LIS.',
    keywords='GLDAS',
    author='Riley Hales',
    author_email='',
    url='',
    license='BSD 3-Clause',
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
