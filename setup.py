from setuptools import setup, find_packages


setup(
    name='remove_actions_opennebula',
    version='1.0.0',
    author='Jiri Novotny',
    author_email='jiri.novotny@img.cas.cz',
    license='MIT',
    url='',
    packages=find_packages(),
    description='Command-line tool for removing VM actions from OpenNebula.',
    long_description='Command-line tool for removing VM actions from OpenNebula.',
    keywords='opennebula vm',
    zip_safe=False,
    entry_points={'console_scripts': ['remove_actions_opennebula = remove_actions_opennebula:cli']},
    install_requires=['selenium'],
    classifiers=[],
)
