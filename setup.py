#!/usr/bin/env python
#
# Copyright 2009-2011, Red Hat, Inc
# John Eckersberg <jeckersb@redhat.com>
#
# This software may be freely redistributed under the terms of the GNU
# general public license.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 675 Mass Ave, Cambridge, MA 02139, USA.
"""
Standard build script.
"""

__docformat__ = 'restructuredtext'


import os
import sys

from os import path
from distutils.core import Command, setup

from taboot import __version__, __license__, __author__, __url__


class SetupBuildCommand(Command):
    """
    Master setup build command to subclass from.
    """

    user_options = []

    def initialize_options(self):
        """
        Setup the current dir.
        """
        self._dir = os.getcwd()

    def finalize_options(self):
        """
        No clue ... but it's required.
        """
        pass


class SphinxCommand(SetupBuildCommand):
    """
    Creates HTML documentation using Sphinx.
    """

    description = "Generate documentation via sphinx"

    def initialize_options(self):
        """
        Setup the current dir.
        """
        self._dir = os.getcwd()

    def finalize_options(self):
        """
        No clue ... but it's required.
        """
        pass

    def run(self):
        """
        Run the DocCommand.
        """
        print "Creating html documentation ..."

        try:
            from sphinx.application import Sphinx

            if not os.access(path.join('docs', 'html'), os.F_OK):
                os.mkdir(path.join('docs', 'html'))
            buildername = 'html'
            outdir = path.abspath(path.join('docs', 'html'))
            doctreedir = os.path.join(outdir, '.doctrees')

            confdir = path.abspath('docs')
            srcdir = path.abspath('docs')
            freshenv = False

            # Create the builder
            app = Sphinx(srcdir, confdir, outdir, doctreedir, buildername,
                         {}, sys.stdout, sys.stderr, freshenv)

            # And build!
            app.builder.build_all()
            print "Your docs are now in %s" % outdir
        except ImportError, ie:
            print >> sys.stderr, "You don't seem to have the following which"
            print >> sys.stderr, "are required to make documentation:"
            print >> sys.stderr, "\tsphinx.application.Sphinx"
        except Exception, ex:
            print >> sys.stderr, "FAIL! exiting ... (%s)" % ex


class RPMBuildCommand(SetupBuildCommand):
    """
    Creates an RPM based off spec files.
    """

    description = "Build an rpm based off of the top level spec file(s)"

    def run(self):
        """
        Run the RPMBuildCommand.
        """
        # TODO: This should be changed from shelling out to actually
        # using the code. For now this works.
        try:
            if os.system('./setup.py sdist'):
                raise Exception("Couldn't call ./setup.py sdist!")
                sys.exit(1)
            if not os.access('dist/rpms/', os.F_OK):
                os.mkdir('dist/rpms/')
            rpm_cmd = 'rpmbuild -ba --clean \
                                    --define "_rpmdir dist/rpms/" \
                                    --define "_srcrpmdir dist/rpms/" \
                                    --define "_sourcedir %s" *spec' % (
                      os.path.join(os.getcwd(), 'dist'))
            if os.system(rpm_cmd):
                raise Exception("Could not create the rpms!")
        except Exception, ex:
            print >> sys.stderr, str(ex)


class ViewDocCommand(SetupBuildCommand):
    """
    Quick command to view generated docs.
    """

    def run(self):
        """
        Opens a webbrowser on docs/html/index.html
        """
        import webbrowser

        print ("NOTE: If you have not created the docs first this will not be "
               "helpful. If you don't see any documentation in your browser "
               "run ./setup.py doc first.")
        if not webbrowser.open('docs/html/index.html'):
            print >> sys.stderr, "Could not open on your webbrowser."


setup(name = "python-taboot",
    version = __version__,
    description = "Client library for performing deployments with func",
    long_description = "Client library for performing deployments with func",
    author = __author__,
    author_email = 'jeckersb@redhat.com',
    platforms = ['any'],

    license = __license__,
    url = __url__,

    packages = ['taboot',
                'taboot.tasks',
                'taboot-func'],

    scripts = ['bin/taboot'],

    classifiers = [
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Development Status :: 5 - Production/Stable',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Programming Language :: Python'],

    cmdclass = {'doc': SphinxCommand,
                'viewdoc': ViewDocCommand,
                'rpm': RPMBuildCommand})
