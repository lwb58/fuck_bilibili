import os
from setuptools import setup, find_packages

package_name = os.path.basename(os.path.dirname(os.path.abspath(__file__)))
#  打包
setup(
    name=package_name,
    version="1.0.0",
    packages=find_packages(),
    include_package_data=True,
    package_data = {
        #  "toolpy": [
        #     'template/*/*',
        # ],
    },
    description='b站接口，视频下载、投稿、点赞、回复等',
    author='Tu Weifeng',
    author_email='907391489@qq.com',
    url='https://github.com/tuweifeng',
    platforms="any",
    license='MIT',
    entry_points = {
        # 'console_scripts': [
        #     'toolpy = toolpy.main:main',
        # ]
    },
    install_requires=[
        "requests>=2.24.0"
    ],
    python_requires='>=3.5',
)
