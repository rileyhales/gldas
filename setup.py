from setuptools import setup, find_namespace_packages
from tethys_apps.app_installation import find_resource_files

# -- Apps Definition -- #
app_package = 'gldas'
release_package = 'tethysapp-' + app_package

# -- Python Dependencies -- #
dependencies = ['netCDF4', 'numpy', 'pandas', 'rasterstats', 'rasterio', 'requests']

# -- Get Resource File -- #
resource_files = find_resource_files('tethysapp/' + app_package + '/templates', 'tethysapp/' + app_package)
resource_files += find_resource_files('tethysapp/' + app_package + '/public', 'tethysapp/' + app_package)

setup(
    name=release_package,
    version='4',
    description='Visualizes GLDAS data through maps and charts',
    long_description='Shows time-animated maps and timeseries plots of monthly average, 1/4 degree resolution, '
                     'GLDAS data sets from NASA LDAS and LIS.',
    keywords='GLDAS',
    author='Riley Hales',
    author_email='',
    url='',
    license='BSD 3-Clause',
    packages=find_namespace_packages(),
    package_data={'': resource_files},
    include_package_data=True,
    zip_safe=False,
    install_requires=dependencies,
)
