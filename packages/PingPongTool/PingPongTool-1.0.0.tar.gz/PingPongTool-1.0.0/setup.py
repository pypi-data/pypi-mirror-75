from setuptools import setup, find_packages

setup(name='PingPongTool', 
    version='1.0.0', 
    url='https://github.com/minibox724/PingPongTool', 
    author='Minibox', 
    author_email='minibox724@gmail.com', 
    description='쉬운 핑퐁빌더 사용을 위한 모듈', 
    packages=find_packages(exclude=['Example']), 
    long_description=open('README.md', encoding="UTF8").read(), 
    long_description_content_type='text/markdown', 
    install_requires=['cython', 'aiohttp'],
    zip_safe=False
)