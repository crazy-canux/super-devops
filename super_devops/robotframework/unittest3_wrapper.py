import sys
import unittest
from unittest.case import SkipTest, _Outcome
import traceback
import inspect

from robot.api import logger
from robot.errors import ExecutionFailed


class BaseUnitTest(unittest.TestCase):

    """Customize unittest for different business.

    class YourAUC(BaseUnitTest):
        def __init__(self, keyword, *args, **kwargs):
            super(YourAUC, self).__init__(keyword, method_name='test_your_auc')
            pass

        def test_your_auc(self):
            pass

        def  validate_input(self):
            pass

        def validate_output(self):
            pass
    """

    def __init__(self, keyword, method_name='runTest'):
        super(BaseUnitTest, self).__init__(method_name)

        # Used for debug.
        self.keyword = keyword

    def run(self, result=None):
        """Rewrite this method to cover default action in unittest."""
        orig_result = result
        if result is None:
            result = self.defaultTestResult()
            startTestRun = getattr(result, 'startTestRun', None)
            if startTestRun is not None:
                startTestRun()

        self._resultForDoCleanups = result
        result.startTest(self)

        testMethod = getattr(self, self._testMethodName)
        if (getattr(self.__class__, "__unittest_skip__", False) or
                getattr(testMethod, "__unittest_skip__", False)):
            # If the class or method was skipped.
            try:
                skip_why = (getattr(self.__class__, '__unittest_skip_why__', '')
                            or getattr(testMethod, '__unittest_skip_why__', ''))
                self._addSkip(result, self, skip_why)
            finally:
                result.stopTest(self)
            return

        expecting_failure_method = getattr(testMethod,
                                           "__unittest_expecting_failure__", False)
        expecting_failure_class = getattr(self,
                                          "__unittest_expecting_failure__", False)
        expecting_failure = expecting_failure_class or expecting_failure_method
        outcome = _Outcome(result)

        try:
            # Customize for super-devops about validate input arguments.
            try:
                self._validate_input()
            except SkipTest as e:
                self._addSkip(result, testMethod, str(e))
            except Exception:
                raise
            else:
            # Customize for super-devops about validate input arguments.

                self._outcome = outcome

                with outcome.testPartExecutor(self):
                    self.setUp()
                if outcome.success:
                    outcome.expecting_failure = expecting_failure
                    with outcome.testPartExecutor(self, isTest=True):
                        testMethod()
                    outcome.expecting_failure = False
                    with outcome.testPartExecutor(self):
                        self.tearDown()

                self.doCleanups()
                for test, reason in outcome.skipped:
                    self._addSkip(result, test, reason)
                self._feedErrorsToResult(result, outcome.errors)
                if outcome.success:
                    if expecting_failure:
                        if outcome.expectedFailure:
                            self._addExpectedFailure(result,
                                                     outcome.expectedFailure)
                        else:
                            self._addUnexpectedSuccess(result)
                    else:
                        result.addSuccess(self)
                return result

        # Customize for super-devops.
        except self.failureException as e:
            result.addFailure(self, sys.exc_info())
            tb = traceback.format_tb(sys.exc_info()[-1])
            logger.debug(
                'Within ({}) AUC, Code Stack: {}'.format(
                    self.keyword, ''.join(tb[1:])
                )
            )
            if self.__ignore_failure(debug_only=True):
                return self._validate_output()
            else:
                raise ExecutionFailed(e, continue_on_failure=True)
        except Exception:
            result.addError(self, sys.exc_info())
            raise
        else:
            return self._validate_output()
        # Customize for super-devops.

        finally:
            # Customize for super-devops.
            status = 'FAILED' if (result.failures or result.errors) else \
                'PASSED'
            logger.info(
                '[AUC] <-> {} <-> {}'.format(
                    ' '.join([
                        word.capitalize()
                        for word in self.keyword.split('_')
                    ]),
                    status
                ), html=False, also_console=True
            )
            try:
                self.tearDown()
            except Exception as e:
                logger.warn(
                    'tearDown failed in unittest: {}'.format(e)
                )
            # except KeyboardInterrupt:
            #     raise
            # except:
            #     result.addError(self, sys.exc_info())
            #     success = False
            # Customize for super-devops.

            result.stopTest(self)
            if orig_result is None:
                stopTestRun = getattr(result, 'stopTestRun', None)
                if stopTestRun is not None:
                    stopTestRun()

            # explicitly break reference cycles:
            # outcome.errors -> frame -> outcome -> outcome.errors
            # outcome.expectedFailure -> frame -> outcome -> outcome.expectedFailure
            outcome.errors.clear()
            outcome.expectedFailure = None

            # clear the outcome, no more needed
            self._outcome = None

    @staticmethod
    def __ignore_failure(debug_only=False):
        if debug_only:
            for frame in inspect.stack()[::-1]:
                if frame[1].endswith('pydevd.py'):
                    return True
            else:
                return bool(sys.flags.debug)
        return False

    def _validate_input(self):
        pass

    def _validate_output(self):
        return


