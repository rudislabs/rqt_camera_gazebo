from setuptools import setup

package_name = 'rqt_camera_gazebo'

setup(
    name=package_name,
    version='0.0.1',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    author='Benjamin Perseghetti',
    author_email='bperseghetti@rudislabs.com',
    maintainer='Benjamin Perseghetti',
    maintainer_email='bperseghetti@rudislabs.com',
    description='rqt_camera_gazebo',
    license='Apache License, Version 2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            "rqt_camera_gazebo = rqt_camera_gazebo.rqt_camera_gazebo:main"
        ],
    },
)
