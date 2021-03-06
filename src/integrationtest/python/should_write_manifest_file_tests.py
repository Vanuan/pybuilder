#  This file is part of Python Builder
#   
#  Copyright 2011 The Python Builder Team
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
import unittest

from integrationtest_support import IntegrationTestSupport

class Test (IntegrationTestSupport):
    def test (self):
        self.write_build_file("""
from pythonbuilder.core import use_plugin, init

use_plugin('python.core')
use_plugin('python.distutils')

name = 'integration-test'
default_task = 'publish'

@init
def init (project):
    project.include_file('spam', 'eggs')
    project.install_file('spam_dir', 'more_spam')
    project.install_file('eggs_dir', 'more_eggs')
""")
        self.create_directory("src/main/python/spam")
        self.write_file("src/main/python/spam/eggs", "")
        self.write_file("src/main/python/more_spam", "")
        self.write_file("src/main/python/more_eggs", "")
        
        reactor = self.prepare_reactor()
        reactor.build()
        
        self.assert_directory_exists("target/dist/integration-test-1.0-SNAPSHOT")
        self.assert_directory_exists("target/dist/integration-test-1.0-SNAPSHOT/spam")
        self.assert_file_empty("target/dist/integration-test-1.0-SNAPSHOT/spam/eggs")
        self.assert_file_empty("target/dist/integration-test-1.0-SNAPSHOT/more_spam")
        self.assert_file_empty("target/dist/integration-test-1.0-SNAPSHOT/more_eggs")
        
        manifest_in = "target/dist/integration-test-1.0-SNAPSHOT/MANIFEST.in"
        
        self.assert_file_exists(manifest_in)
        self.assert_file_permissions(0o664, manifest_in)
        self.assert_file_content(manifest_in, """include spam/eggs
include more_spam
include more_eggs
""")


if __name__ == "__main__":
    unittest.main()