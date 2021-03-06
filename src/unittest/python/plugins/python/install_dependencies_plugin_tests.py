#  This file is part of pybuilder
#
#  Copyright 2011 The pybuilder Team
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

__author__ = "Alexander Metzner"

import unittest

from mockito import mock, when, verify, unstub, any as any_value

from pythonbuilder.core import Project, Logger, Dependency
from pythonbuilder.plugins.python.install_dependencies_plugin import (install_runtime_dependencies,
                                                                      install_build_dependencies,
                                                                      install_dependencies,
                                                                      install_dependency)

import pythonbuilder.plugins.python.install_dependencies_plugin


class InstallDependencyTest(unittest.TestCase):
    def setUp(self):
        self.project = Project("unittest", ".")
        self.project.set_property("dir_install_logs", "any_directory")
        self.logger = mock(Logger)
        when(pythonbuilder.plugins.python.install_dependencies_plugin).execute_command(any_value(), any_value(),
            shell=True).thenReturn(0)

    def tearDown(self):
        unstub()

    def test_should_install_dependency_without_version(self):
        dependency = Dependency("spam")

        install_dependency(self.logger, self.project, dependency)

        verify(pythonbuilder.plugins.python.install_dependencies_plugin).execute_command("pip install spam", any_value()
            , shell=True)

    def test_should_install_dependency_using_custom_index_url(self):
        self.project.set_property("install_dependencies_index_url", "some_index_url")
        dependency = Dependency("spam")

        install_dependency(self.logger, self.project, dependency)

        verify(pythonbuilder.plugins.python.install_dependencies_plugin).execute_command(
            "pip install --index-url some_index_url spam", any_value()
            , shell=True)

    def test_should_not_use_extra_index_url_when_index_url_is_not_set(self):
        self.project.set_property("install_dependencies_extra_index_url", "some_index_url")
        dependency = Dependency("spam")

        install_dependency(self.logger, self.project, dependency)

        verify(pythonbuilder.plugins.python.install_dependencies_plugin).execute_command(
            "pip install spam", any_value()
            , shell=True)

    def test_should_not_use_index_and_extra_index_url_when_index_and_extra_index_url_are_set(self):
        self.project.set_property("install_dependencies_index_url", "some_index_url")
        self.project.set_property("install_dependencies_extra_index_url", "some_extra_index_url")
        dependency = Dependency("spam")

        install_dependency(self.logger, self.project, dependency)

        verify(pythonbuilder.plugins.python.install_dependencies_plugin).execute_command(
            "pip install --index-url some_index_url --extra-index-url some_extra_index_url spam", any_value()
            , shell=True)

    def test_should_use_mirrors_to_install_dependency(self):
        self.project.set_property("install_dependencies_use_mirrors", True)
        dependency = Dependency("spam")

        install_dependency(self.logger, self.project, dependency)

        verify(pythonbuilder.plugins.python.install_dependencies_plugin).execute_command(
            "pip install --use-mirrors spam", any_value()
            , shell=True)

    def test_should_upgrade_dependencies(self):
        self.project.set_property("install_dependencies_upgrade", True)
        dependency = Dependency("spam")

        install_dependency(self.logger, self.project, dependency)

        verify(pythonbuilder.plugins.python.install_dependencies_plugin).execute_command(
            "pip install --upgrade spam", any_value()
            , shell=True)

    def test_should_install_dependency_with_version(self):
        dependency = Dependency("spam", "0.1.2")

        install_dependency(self.logger, self.project, dependency)

        verify(pythonbuilder.plugins.python.install_dependencies_plugin).execute_command("pip install spam>=0.1.2",
            any_value()
            , shell=True)

    def test_should_install_dependency_with_version_and_operator(self):
        dependency = Dependency("spam", "==0.1.2")

        install_dependency(self.logger, self.project, dependency)

        verify(pythonbuilder.plugins.python.install_dependencies_plugin).execute_command("pip install spam==0.1.2",
            any_value()
            , shell=True)

    def test_should_install_dependency_with_url(self):
        dependency = Dependency("spam", url="some_url")

        install_dependency(self.logger, self.project, dependency)

        verify(pythonbuilder.plugins.python.install_dependencies_plugin).execute_command("pip install some_url",
            any_value()
            , shell=True)

    def test_should_install_dependency_with_url_even_if_version_is_given(self):
        dependency = Dependency("spam", version="0.1.2", url="some_url")

        install_dependency(self.logger, self.project, dependency)

        verify(pythonbuilder.plugins.python.install_dependencies_plugin).execute_command("pip install some_url",
            any_value()
            , shell=True)


class InstallRuntimeDependenciesTest(unittest.TestCase):
    def setUp(self):
        self.project = Project("unittest", ".")
        self.project.set_property("dir_install_logs", "any_directory")
        self.logger = mock(Logger)
        when(pythonbuilder.plugins.python.install_dependencies_plugin).execute_command(any_value(), any_value(),
            shell=True).thenReturn(0)

    def tearDown(self):
        unstub()

    def test_should_install_multiple_dependencies(self):
        self.project.depends_on("spam")
        self.project.depends_on("eggs")

        install_runtime_dependencies(self.logger, self.project)

        verify(pythonbuilder.plugins.python.install_dependencies_plugin).execute_command("pip install spam",
            any_value()
            , shell=True)
        verify(pythonbuilder.plugins.python.install_dependencies_plugin).execute_command("pip install eggs",
            any_value()
            , shell=True)


class InstallBuildDependenciesTest(unittest.TestCase):
    def setUp(self):
        self.project = Project("unittest", ".")
        self.project.set_property("dir_install_logs", "any_directory")
        self.logger = mock(Logger)
        when(pythonbuilder.plugins.python.install_dependencies_plugin).execute_command(any_value(), any_value(),
            shell=True).thenReturn(0)

    def tearDown(self):
        unstub()


    def test_should_install_multiple_dependencies(self):
        self.project.build_depends_on("spam")
        self.project.build_depends_on("eggs")

        install_build_dependencies(self.logger, self.project)

        verify(pythonbuilder.plugins.python.install_dependencies_plugin).execute_command("pip install spam",
            any_value()
            , shell=True)
        verify(pythonbuilder.plugins.python.install_dependencies_plugin).execute_command("pip install eggs",
            any_value()
            , shell=True)


class InstallDependenciesTest(unittest.TestCase):
    def setUp(self):
        self.project = Project("unittest", ".")
        self.project.set_property("dir_install_logs", "any_directory")
        self.logger = mock(Logger)
        when(pythonbuilder.plugins.python.install_dependencies_plugin).execute_command(any_value(), any_value(),
            shell=True).thenReturn(0)

    def tearDown(self):
        unstub()


    def test_should_install_single_dependency_without_version(self):
        self.project.depends_on("spam")
        self.project.build_depends_on("eggs")

        install_dependencies(self.logger, self.project)

        verify(pythonbuilder.plugins.python.install_dependencies_plugin).execute_command("pip install spam",
            any_value()
            , shell=True)
        verify(pythonbuilder.plugins.python.install_dependencies_plugin).execute_command("pip install eggs",
            any_value()
            , shell=True)
