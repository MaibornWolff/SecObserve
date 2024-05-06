from unittest import TestCase

from application.core.models import Observation, Parser
from application.import_observations.management.commands.register_parsers import Command
from application.import_observations.models import Api_Configuration


class TestRegisterParsers(TestCase):

    def setUp(self):
        Api_Configuration.objects.all().delete()
        Observation.objects.all().delete()
        Parser.objects.all().delete()

    def test_register_parsers(self):
        command = Command()
        command.handle()

        parsers = Parser.objects.all()
        self.assertEqual(10, len(parsers))

        parser = parsers[0]
        self.assertEqual("Manual", parser.name)
        self.assertEqual("Manual", parser.type)
        self.assertEqual("Manual", parser.source)
        self.assertEqual("", parser.module_name)
        self.assertEqual("", parser.class_name)

        parser = parsers[1]
        self.assertEqual("Dependency Track", parser.name)
        self.assertEqual("SCA", parser.type)
        self.assertEqual("API", parser.source)
        self.assertEqual("dependency_track", parser.module_name)
        self.assertEqual("DependencyTrack", parser.class_name)
