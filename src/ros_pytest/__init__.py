# coding=utf-8
import os

import pytest
import rospy


def get_output_file(argv):
    for arg in argv:
        if arg.startswith('--gtest_output'):
            return arg.split('=xml:')[1]

    raise RuntimeError('No output file has been passed')

def get_add_args(argv):
    # don't include the --gtest, as that is the first non-usersupplied arg
    end = next(argv.index(arg) for arg in argv if arg.startswith('--gtest_output'))
    # strip executable path as well
    return argv[1:end]

def run_pytest(argv):
    output_file = get_output_file(argv)
    test_module = rospy.get_param('test_module')
    module_path = os.path.realpath(test_module)
    add_args = get_add_args(argv)

    call_args = [module_path, '--junitxml={}'.format(output_file)]
    call_args.extend(add_args)
    return pytest.main(call_args)
