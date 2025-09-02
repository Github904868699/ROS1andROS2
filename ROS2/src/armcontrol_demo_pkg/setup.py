from setuptools import find_packages, setup

package_name = 'armcontrol_demo_pkg'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='dudu',
    maintainer_email='dudu@todo.todo',
    description='Demo node for joint state publishing with dynamic parameters.',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'armcontrol_demo_node = armcontrol_demo_pkg.armcontrol_demo_node:main'
        ],
    },
)
