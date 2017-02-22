

######################################################################################
#
# YOU CAN / SHOULD EDIT THE FOLLOWING SETTING
#
######################################################################################

PKG_NAME = 'peak_fisher'

VERSION = (0, 0, 1)

# list all required packages here:

REQUIRED_PACKAGES = []


### install package as emzed extension ? #############################################
#   -> package will appear in emzed.ext namespace after installation

IS_EXTENSION = True


### install package as emzed app ?  ##################################################
#   -> can be started as app.peak_fisher()
#   set this variable to None if this is a pure extension and not an emzed app

APP_MAIN = "peak_fisher.app:run"


### author information ###############################################################

AUTHOR = 'Gerald Lackner'
AUTHOR_EMAIL = 'gerald.lackner@uni-jena.de'
AUTHOR_URL = ''


### package descriptions #############################################################

DESCRIPTION = "A tool to find MS spectra containing a given list of peaks"
LONG_DESCRIPTION = """

find all ms2_spectra containing MS2 peaks with given mz within relative mz_tol,
more intense than rel_noise_threshold. Result is a table with Scan number, precursor mass, precursor rt

"""

LICENSE = "http://opensource.org/licenses/GPL-3.0"


######################################################################################
#                                                                                    #
# DO NOT TOUCH THE CODE BELOW UNLESS YOU KNOW WHAT YOU DO !!!!                       #
#                                                                                    #
#                                                                                    #
#       _.--""--._                                                                   #
#      /  _    _  \                                                                  #
#   _  ( (_\  /_) )  _                                                               #
#  { \._\   /\   /_./ }                                                              #
#  /_"=-.}______{.-="_\                                                              #
#   _  _.=('""')=._  _                                                               #
#  (_'"_.-"`~~`"-._"'_)                                                              #
#   {_"            "_}                                                               #
#                                                                                    #
######################################################################################


VERSION_STRING = "%s.%s.%s" % VERSION

ENTRY_POINTS = dict()
ENTRY_POINTS['emzed_package'] = [ "package = " + PKG_NAME, ]
if IS_EXTENSION:
    ENTRY_POINTS['emzed_package'].append("extension = " + PKG_NAME)
if APP_MAIN is not None:
    ENTRY_POINTS['emzed_package'].append("main = %s" % APP_MAIN)


if __name__ == "__main__":   # allows import setup.py for version checking

    from setuptools import setup
    setup(name=PKG_NAME,
        packages=[ PKG_NAME ],
        author=AUTHOR,
        author_email=AUTHOR_EMAIL,
        url=AUTHOR_URL,
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        license=LICENSE,
        version=VERSION_STRING,
        entry_points = ENTRY_POINTS,
        install_requires = REQUIRED_PACKAGES,
        )
   