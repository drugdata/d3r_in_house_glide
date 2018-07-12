import setuptools

setuptools.setup(
    name="internal_glide_contestant",
    version="0.1.0",
    url="https://github.com/drugdata/custom_celpp_contestant",

    author="Jeff Wagner",
    author_email="j5wagner@ucsd.edu",

    description="Internal glide contestant for D3R CELPP competition",
    long_description=open('README.rst').read(),

    packages=setuptools.find_packages(),

    install_requires=["d3r"],

    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
    ],
     scripts = ['internal_glide_contestant/internal_glide_runner_dock.py',
                'internal_glide_contestant/internal_glide_runner_ligand_prep.py', 
                'internal_glide_contestant/internal_glide_runner_protein_prep.py']
)
