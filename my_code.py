import logging
import os
import re
import sys

import click
import pyocr
from PIL import Image


@click.command()
@click.option('--input', help='input file (png, jpg, pdf)')
@click.option('--output', help='output file (.txt)')
@click.option('--verbose', is_flag=True, help='output detailed logs')
def func(input, output, verbose):
    if not input or not output:
        logger.error("Invalid command.")
        sys.exit(1)
    filepath = input
    if not os.path.exists(filepath):
        logger.error("Input file doesn't exist.")
        sys.exit(1)
    if not re.match(r'([a-zA-Z0-9]+)\.txt', output):
        logger.error("Invalid output file.")
        sys.exit(1)
    img = Image.open(filepath)
    tools = pyocr.get_available_tools()
    if len(tools) == 0:
        logger.error("OCR tool not found")
        sys.exit(1)
    tool = tools[0]
    text = tool.image_to_string(img,
                                lang="eng",
                                builder=pyocr.builders.TextBuilder())
    os.chdir(os.getcwd())
    with open(output, mode='w') as f:
        f.write(text)


if __name__ == '__main__':
    logger = logging.getLogger("my_code")
    func()
