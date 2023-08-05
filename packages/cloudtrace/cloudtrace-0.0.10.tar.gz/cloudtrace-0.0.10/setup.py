from setuptools import setup, find_packages
from setuptools.extension import Extension
from Cython.Build import cythonize

try:
    from Cython.Distutils import build_ext
except ImportError:
    use_cython = False
else:
    use_cython = True

print(use_cython)

ext = '.pyx' if use_cython else '.c'

extensions_names = {
    'cloudtrace.utils': ['cloudtrace/utils' + ext],
    'cloudtrace.probe': ['cloudtrace/probe' + ext],
    'cloudtrace.fasttrace': ['cloudtrace/fasttrace.py']
}

extensions = [Extension(k, v) for k, v in extensions_names.items()]
package_data = {k: ['*.pxd'] for k in extensions_names}

if use_cython:
    from Cython.Build import cythonize
    extensions = cythonize(
        extensions,
        compiler_directives={'language_level': '3', 'embedsignature': True},
        annotate=True,
        gdb_debug=True
    )


setup(
    name="cloudtrace",
    version='0.0.10',
    author='Alex Marder',
    # author_email='notlisted',
    description="Various packages for traceroute and BGP dump analysis.",
    url="https://github.com/alexmarder/traceutils",
    packages=find_packages(),
    # setup_requires=["cython", "traceutils"],
    install_requires=['scapy', 'traceutils'],
    # cmdclass={'build_ext': build_ext},
    ext_modules=extensions,
    entry_points={
        'console_scripts': ['fasttrace=cloudtrace.fasttrace:main'],
    },
    zip_safe=False,
    package_data=package_data,
    include_package_data=True,
    python_requires='>3.6'
)
