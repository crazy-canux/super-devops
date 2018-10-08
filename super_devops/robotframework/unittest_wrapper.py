import sys
import warnings
import unittest
from unittest.case import SkipTest, _ExpectedFailure, _UnexpectedSuccess
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
                self._addSkip(result, skip_why)
            finally:
                result.stopTest(self)
            return

        try:
            success = False

            # Customize for super-devops about validate input arguments.
            try:
                self._validate_input()
            except SkipTest as e:
                self._addSkip(result, str(e))
            except Exception:
                raise
            else:

                try:
                    self.setUp()
                # except SkipTest as e:
                #     self._addSkip(result, str(e))
                # except KeyboardInterrupt:
                #     raise
                # except:
                #     result.addError(self, sys.exc_info())
                except Exception as e:
                    logger.warn(
                        'setUp failed in unittest: {}'.format(e.message)
                    )

                try:
                    testMethod()
                except KeyboardInterrupt:
                    raise
                # except self.failureException:
                #     result.addFailure(self, sys.exc_info())
                except _ExpectedFailure as e:
                    addExpectedFailure = getattr(result, 'addExpectedFailure', None)
                    if addExpectedFailure is not None:
                        addExpectedFailure(self, e.exc_info)
                    else:
                        warnings.warn("TestResult has no addExpectedFailure method, reporting as passes",
                                      RuntimeWarning)
                        result.addSuccess(self)
                except _UnexpectedSuccess:
                    addUnexpectedSuccess = getattr(result, 'addUnexpectedSuccess', None)
                    if addUnexpectedSuccess is not None:
                        addUnexpectedSuccess(self)
                    else:
                        warnings.warn("TestResult has no addUnexpectedSuccess method, reporting as failures",
                                      RuntimeWarning)
                        result.addFailure(self, sys.exc_info())
                except SkipTest as e:
                    self._addSkip(result, str(e))
                except:
                    raise
                    # result.addError(self, sys.exc_info())
                else:
                    success = True

            cleanUpSuccess = self.doCleanups()
            success = success and cleanUpSuccess
            if success:
                result.addSuccess(self)

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
                raise ExecutionFailed(e.message, continue_on_failure=True)
        except Exception:
            result.addError(self, sys.exc_info())
            raise
        else:
            return self._validate_output()

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
                    'tearDown failed in unittest: {}'.format(e.message)
                )
            # except KeyboardInterrupt:
            #     raise
            # except:
            #     result.addError(self, sys.exc_info())
            #     success = False

            result.stopTest(self)
            if orig_result is None:
                stopTestRun = getattr(result, 'stopTestRun', None)
                if stopTestRun is not None:
                    stopTestRun()

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


