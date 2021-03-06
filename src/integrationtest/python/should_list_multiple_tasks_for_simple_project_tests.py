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
from pythonbuilder.core import task

@task
def my_task (): pass

@task
def another_task (): pass

@task("a_task_with_overridden_name")
def any_method_name (): pass
        """)
        reactor = self.prepare_reactor()
        
        tasks = reactor.get_tasks()

        self.assertEquals(3, len(tasks))
        self.assertEquals("my_task", tasks[0].name)
        self.assertEquals("a_task_with_overridden_name", tasks[1].name)
        self.assertEquals("another_task", tasks[2].name)
        
if __name__ == "__main__":
    unittest.main()
