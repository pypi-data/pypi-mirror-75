import synacell.cmodule


class Test:

    test_string = ""

    @staticmethod
    def run_test_li(test_li: list, name: str, print_log = True) -> int:
        """
        Runs list of functions that return int, str as test result.

        :param test_li: List of test functions for running
        :param name: Test name
        :param print_log: Print log file after each successfull test
        :return: 0: Success, 1: Fail
        """
        all_passed = True
        for i in range(len(test_li)):
            val, msg = test_li[i]()
            if val == 0:
                print(f"Test {name}_{i + 1} passed")
            else:
                print(f"Test {name}_{i + 1} failed")
                print(f"Log:\n{synacell.cmodule.SnnAPI.get_log()}")
                synacell.cmodule.SnnAPI.clear_log()
                all_passed = False
                Test.test_string += \
                    f"FAIL: Test {name}_{i + 1} failed with error message: {msg}\n"
                break
            if print_log:
                print(f"Log:\n{synacell.cmodule.SnnAPI.get_log()}")
            synacell.cmodule.SnnAPI.clear_log()

        if all_passed:
            Test.test_string += f"SUCCESS: All {name} tests passed!\n"
            return 0
        return 1
