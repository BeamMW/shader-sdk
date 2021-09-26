import argparse
from importlib.machinery import SourceFileLoader
import logging
import os
import pathlib
import platform
import shutil
import sys

os.environ['SHADER_SDK_BASE_DIR'] = str(pathlib.Path(__file__).parent.parent.absolute())
os.environ['PLATFORM_NAME'] = platform.system()
os.environ['CMAKE_EXECUTABLE'] = shutil.which('cmake')
os.environ['WASI_PATH'] = os.path.join(os.environ['SHADER_SDK_BASE_DIR'], [s for s in os.listdir(os.environ['SHADER_SDK_BASE_DIR']) if s.startswith('wasi-sdk')][0])

logging.getLogger().setLevel(logging.INFO)

parser = argparse.ArgumentParser()
subparsers = parser.add_subparsers(title='commands', dest='command_name')

parser_init = subparsers.add_parser('init', help='Initialize shader-sdk. The command must be called before any other.')

parser_create_proj = subparsers.add_parser('create_project', help='Create project with specified name')
parser_create_proj.add_argument('project_name')

args = parser.parse_args()

command_module = SourceFileLoader(args.command_name, os.path.join(os.environ['SHADER_SDK_BASE_DIR'], 'scripts', 'commands', args.command_name + '.py')).load_module()
command_module.Command().execute(args)