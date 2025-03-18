import pathlib
import sys

root_directory = pathlib.Path(__file__).parent.parent
src_directory = root_directory / 'src'
sys.path.append(str(src_directory))