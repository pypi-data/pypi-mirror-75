__version__ = '3.4.1' # Keep this on the first line so it's easy for __init__.py to grab.



from distutils.core import setup
setup(name           = 'Spinmob',
      version        = __version__,
      description    = 'Data handling, plotting, analysis, and GUI building for scientific labs',
      author         = 'Jack Sankey',
      author_email   = 'jack.sankey@gmail.com',
      url            = 'https://github.com/Spinmob/spinmob',
      packages       = ['spinmob', 'spinmob.egg', 'spinmob._tests'],
      package_dir    = {'spinmob'      :   '.',
                        'egg'          :   'spinmob/egg',
                        '_tests'       :   'spinmob/_tests'}
     )
