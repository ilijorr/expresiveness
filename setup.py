"""
setup.py for ExpresiVeNess project
"""

from setuptools import setup, find_packages

setup(
    name="expressivenness",
    version="1.0.0",
    description="Graph management system with pattern implementations",
    author="Vuk Vićentić, Ilija Jordanovski, Miloš Milosavljević",
    packages=find_packages(),
    install_requires=[
        "flask>=2.0.0",
        "flask-cors>=3.0.0",
    ],
    python_requires=">=3.8",
    include_package_data=True,
    package_data={
        'src.web': [
            'templates/*.html',
            'static/css/*.css',
            'static/js/*.js',
        ]
    },
    entry_points={
        'console_scripts': [
            'src=src.web.app:create_app',
        ],
    },
)