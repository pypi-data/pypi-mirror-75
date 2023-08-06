import setuptools

setuptools.setup(
   name='gc_bokeh_app_test',
   version='0.0.3',
   author='Greg Coyle',
   author_email='gregory.coyle@tufts.edu',
   packages=setuptools.find_packages(),
   description='Testing a Bokeh app in conda',
   long_description='Testing a Bokeh app in Anaconda',
   install_requires=[
       "bokeh >= 2.1.1"],
   python_requires='>=3.6',
)