# -*- coding: utf-8 -*-
# Taboot - Client utility for performing deployments with Func.
# Copyright © 2009-2011, Red Hat, Inc.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


import yaml


class YamlDoc:
    """
    Representation of a Yaml Document
    """
    def __init__(self, yamlDoc):
        self.yamlDoc = yamlDoc

    def getYamlDoc(self):
        return yamlDoc

    def __str__(self):
        return ("---\n" + yaml.dump(self.yamlDoc))


class TabootScript(YamlDoc):
    """
    Representation of a Taboot Script
    """
    def validateScript(self):
        # TODO add validation logic and throw exception if invalid
        return True

    def __init__(self, yamlDoc, fileName, edited):
        YamlDoc.__init__(self, yamlDoc)
        self.fileName = fileName
        self.edited = edited
        self.validateScript()

    def deletePreflight(self):
        for b in self.yamlDoc:
            if 'preflight' in b:
                del b['preflight']
        self.validateScript()

    def addLogging(self, logfile):
        for b in self.yamlDoc:
            if 'output' in b:
                b['output'].append({'LogOutput': {'logfile': logfile}})
            else:
                b['output'] = [{'LogOutput': {'logfile': logfile}},
                               'CLIOutput']
        self.validateScript()

    def setConcurrency(self, concurrency):
        for b in self.yamlDoc:
            b['concurrency'] = concurrency
                