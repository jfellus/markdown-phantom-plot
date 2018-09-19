from setuptools import setup
setup(
    name='markdown-phantom-plot',
    version='1.0',
    py_modules=['markdown-phantom-plot'],
    install_requires = ['markdown>=2.5'],
    data_files=[('/usr/local/bin', ['svg2pdf'])]
)
