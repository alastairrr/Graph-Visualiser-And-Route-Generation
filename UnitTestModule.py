
#   Unit Test Framework ============================================ #
#
#   Methods within class test harnesses must be named in order of execution (i.e., case_1_test_name, case_2_test_name)
#   Methods which are tests cases must use assertEqual, assertNotEqual or raise Exception() when validating data
#   Print statements are disabled
#   Name of test harness is the name of the class
#   Process for each test case: Generate values, then validate values.
#
#   =================================================================#
# 
#   CURTIN UNIVERISTY COMP1002 - Data Structures and Algorithms
#   Unit Test Module
#   Author: Alastair Kho
#   ID: 20214878
#


# ==== MODULES ==== #
import traceback
import timeit
import sys
import os
import numpy


# ==== MAIN UNIT TEST CLASS ==== #
class UnitTest:

    # ---- Public Methods ---- #
    def assertEqual(self, input1, input2, message=None) -> None:
        if message == None:
            message = f"Assertion Error! {input1} != {input2}"
        assert input1 == input2, message

    def assertNotEqual(self, input1, input2, message=None) -> None:
        if message == None:
            message = f"Assertion Error! {input1} == {input2}"
        assert input1 != input2, message

    # ---- Private Methods ---- #
    def _blockPrint(self):
        sys.stdout = open(os.devnull, 'w')

    def _enablePrint(self):
        sys.stdout = sys.__stdout__
    

    # ---- Core ---- #
    def run(self, blockPrint=False) -> None:
        print(f"\n\033[1m# =================== {self.__class__.__name__.upper()} =================== #")
        print(f"Python version: {sys.version}")
        print("# ------------------------------------------------------- #\n\033[0m")
        testCount = 0
        timeStart = timeit.default_timer()
        passed = 0
        failed = 0

        blackListedFunctions = numpy.array(("assertEqual", "assertNotEqual", "run"))

        for testCase in dir(self):
            if not testCase.startswith("_") and testCase not in blackListedFunctions:

                superTestCase = getattr(self, testCase)

                if hasattr(superTestCase, "__call__"):
                    testCount += 1
                    try:
                        if blockPrint == True: 
                            self._blockPrint()
                        superTestCase.__call__()
                        self._enablePrint()

                        passed += 1
                        print(f"\033[1m{superTestCase.__name__} ... \033[1;32mpassed\033[0m")

                    except Exception as e:
                        self._enablePrint()

                        failed += 1
                        print(f"\033[1m{superTestCase.__name__} ... \033[1;91mFAILED\033[0m")

                        print("\033[1;91m=========================================================")
                        print(f"FAIL: {superTestCase.__name__}")
                        print("---------------------------------------------------------")
                        print(f"{traceback.format_exc()}---------------------------------------------------------\033[0m\n")

        timeFinal = timeit.default_timer()

        print(f"\n\033[1;93mRan {testCount} test(s) in {timeFinal-timeStart} seconds")

        if failed == 0:
            print(f"\033[1;92m{passed} PASSED\033[0m, \033[1m{failed} FAILED\033[0m\n")
        else:
            print(f"\033[1;92m{passed} PASSED, \033[1;91m{failed} FAILED\033[0m\n")
                        
