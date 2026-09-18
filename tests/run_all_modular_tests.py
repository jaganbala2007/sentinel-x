"""
Sentinel-X Unified Modular Architecture Test Suite
==================================================
Runs unit, integration, simulation, and fault injection tests across:
  - /core
  - /environments
  - /hazards
  - /communication
  - /hardware
  - /digital_twin
  - /storage
"""

import sys
import os
import unittest

# Ensure project root is on sys.path
_project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _project_root not in sys.path:
    sys.path.insert(0, _project_root)

# Import test cases
from tests.test_core_engines import TestCoreEngines
from tests.test_environments_and_hazards import TestEnvironmentsAndHazards
from tests.test_hardware_and_storage import TestHardwareAndStorage
from tests.test_communication_and_demo import TestCommunicationAndDemo
from tests.test_disaster_management_suite import TestDisasterManagementSuite

def run_suite():
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    suite.addTests(loader.loadTestsFromTestCase(TestCoreEngines))
    suite.addTests(loader.loadTestsFromTestCase(TestEnvironmentsAndHazards))
    suite.addTests(loader.loadTestsFromTestCase(TestHardwareAndStorage))
    suite.addTests(loader.loadTestsFromTestCase(TestCommunicationAndDemo))
    suite.addTests(loader.loadTestsFromTestCase(TestDisasterManagementSuite))

    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    print("\n==================================================")
    print(f"Tests Run: {result.testsRun}")
    print(f"Errors: {len(result.errors)}")
    print(f"Failures: {len(result.failures)}")
    print(f"Success: {result.wasSuccessful()}")
    print("==================================================")
    return result.wasSuccessful()

if __name__ == "__main__":
    success = run_suite()
    sys.exit(0 if success else 1)
