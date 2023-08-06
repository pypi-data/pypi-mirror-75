import setuptools

print(setuptools.find_packages())

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
     name='anexo2',
     version='0.107',
     license='MIT',
     author="Andres Vazquez",
     author_email="andres@data99.com.ar",
     description="Generacion de HTML para impresion de Anexo II",
     long_description=long_description,
     long_description_content_type="text/markdown",
     url="https://github.com/cluster311/Anexo2",
     install_requires=[
        'cerberus>=1.3',
        'jinja2'
     ],
     include_package_data=True,  # for html file
     packages=['anexo2'],  # setuptools.find_packages(),
     
     classifiers=[
         'Programming Language :: Python :: 3',
         'Programming Language :: Python :: 3.6',
         'License :: OSI Approved :: MIT License',
         'Operating System :: OS Independent',
         'Intended Audience :: Developers', 
     ],
     python_requires='>=3.6',
 )