import setuptools

setuptools.setup(
    name='mandala',
    version='1.0.2',
    description='A RBAC auth framework for django', 
    long_description='Easy to use for not only developers but also normal user&admin.',
    # long_description_content_type="text/markdown",
    keywords='django rbac auth framework',
    install_requires=['django>=2.2.4'],
    python_requires=">=3.6",
    packages=setuptools.find_packages(),
    author='Tom Tsong',
    author_email='congdaxia@126.com',
    url='https://github.com/TomTsong/mandala',
    classifiers=[
        # 'Development Status :: 1 - Planning',
        # 'Development Status :: 2 - Pre-Alpha',
        # 'Development Status :: 3 - Alpha',
        # 'Development Status :: 4 - Beta',
        # 'Development Status :: 5 - Production/Stable'
        'Development Status :: 5 - Production/Stable',  # 当前开发进度等级（测试版，正式版等）
        'Intended Audience :: Developers',  # 模块适用人群
        'Topic :: Software Development :: Code Generators',  # 给模块加话题标签
        'License :: OSI Approved :: MIT License',  # 模块的license

        # 'Programming Language :: Python :: 3',
        # 'Programming Language :: Python :: 3.4',
        # 'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        # 'Programming Language :: Python :: 3.7',
    ]
)