#!/usr/bin/python
# -*- coding: UTF-8 -*-
import click
from swagger_diff.swagger_diff import Diff


@click.command()
@click.option("--old", help="old version")
@click.option("--new", help="new version")
@click.option("--output", default="report.html", help="example: report.hml")
def main(old, new, output):
    processed_diff = Diff(old, new, output)
    processed_diff.generate()
    print(processed_diff.is_compatible())
    if processed_diff.is_compatible() is not True:
        processed_diff.render()
        # raise Exception("some change, please find the report.")


main()
