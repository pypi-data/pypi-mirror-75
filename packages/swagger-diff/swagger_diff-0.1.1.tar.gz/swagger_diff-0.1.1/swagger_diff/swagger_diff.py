#!/usr/bin/python
# -*- coding: UTF-8 -*-
import os
import re
import json
import jinja2
import argparse
from swagger_diff.swagger_parser import SwaggerParser
from swagger_diff.model import (
    AddedItem,
    RemovedItem,
    ChangedItem,
    MethodEnum,
    Parameter
)
from dictdiffer import diff, patch, swap, revert


def get_http_method(text):
    pattern = r"(.get.)|(.post.)|(.put.)|(.delete.)|(.patch.)"
    return re.search(pattern,text).group()[1:-1]


def get_endpoint(text):
    return text[:text.index(".")]


class Diff(object):
    new_parsed = None
    old_parsed = None

    added_definitions = []
    removed_definitions = []
    added_operations = []
    removed_operations = []
    added_paths = []
    removed_paths = []

    def __init__(self, old, new, output="report.html"):
        parsed_old = SwaggerParser(swagger_path=old)
        parsed_new = SwaggerParser(swagger_path=new)
        self.old_parsed = parsed_old
        self.new_parsed = parsed_new
        self.output = output

    @property
    def diff_paths(self):
        return self.get_diff_paths()

    # def from_config(self, config):
    #     parsed_new = SwaggerParser(swagger_path=config.new_spec)
    #     parsed_old = SwaggerParser(swagger_path=config.old_spec)
    #
    #     self.old_parsed = parsed_old
    #     self.new_parsed = parsed_new
    #     self.generate()
    #     return self

    def is_compatible(self):
        return len(self.diff_paths) == 0

    def generate(self):
        # cls.find_changed_operations()
        self.find_changed_paths()

    def get_diff_paths(self) -> list:
        return list(diff(self.old_parsed.paths, self.new_parsed.paths))

    def find_changed_paths(self):
        # diff_paths = self.diff_paths
        self.added_paths = [path for path in self.diff_paths if path[0] == 'add']
        self.removed_paths = [path for path in self.diff_paths if path[0] == 'remove']
        # cls.changed_paths = [path for path in changed_paths if path[0] == 'changed']
        # cls.changed_paths = [path for path in changed_paths if "parameters" in path[1]]
        self.changed_paths = self.get_changed_paths()

    def get_changed_paths(self):
        changed_paths = []
        for path in self.diff_paths:
            params: list = []
            if "parameters" in path[1]:
                for detail in path[2]:
                    params.append(
                        Parameter(
                            status=path[0],
                            name=detail[0],
                            description=detail[1]["description"]
                              ))
            elif "produces" in path[1]:
                # todo
                pass

            if params:
                changed_paths.append(
                    ChangedItem(
                        method=get_http_method(path[1]).upper(),
                        path=get_endpoint(path[1])[1:],
                        summary="",
                        parameters=params
                    )
                )
        return changed_paths

    def get_added_details(self):
        return self._get_path_details(
            self.added_paths,
            AddedItem
        )

    def get_removed_details(self):
        return self._get_path_details(
            self.removed_paths,
            RemovedItem
        )

    def render(self):
        external_data = {
            "old_version": self.old_parsed.specification["info"]["version"],
            "new_version": self.new_parsed.specification["info"]["version"],
            "added_details": self.get_added_details(),
            "removed_details": self.get_removed_details(),
            "changed_details": self.changed_paths
        }

        with open(self.__default_html_template_path(), encoding="utf-8") as f:
            t = jinja2.Template(f.read(), trim_blocks=True)
        content = t.render(SwaggerDiffReport=external_data)

        with open(self.output, "w", encoding="utf-8") as f:
            f.write(content)

    @staticmethod
    def _get_path_details(paths, path_model):
        details = []
        for path in paths:
            endpoint = path[1]
            for path_details in path[2]:
                if path_details[0].upper() in MethodEnum._value2member_map_:
                    details.append(path_model(
                        method=path_details[0].upper(),
                        path=endpoint[1:],
                        summary=path_details[1]["summary"]
                        ))
        return details

    @staticmethod
    def __default_html_template_path(html_file="template.html"):
        return os.path.join(os.path.dirname(os.path.abspath(__file__)), html_file)


class Config(object):
    new_spec = None
    old_spec = None
    output = None

    @classmethod
    def from_json(cls, filename):
        config = Config()
        raw_config = json.loads(filename)
        config.new_spec = raw_config['new_spec']
        config.old_spec = raw_config['old_spec']
        return config


def load_config(args):
    if args.config is not None:
        config = Config.from_json(args.config)
    else:
        config = Config()

    if args.new is not None:
        config.new_spec = args.new

    if args.old is not None:
        config.old_spec = args.old

    if args.output is not None:
        config.output = args.output

    return config

# if __name__ == "__main__":
#     parser = argparse.ArgumentParser()
#     # parser.add_argument('--config', help='JSON config file')
#     parser.add_argument('--new', help='after swagger_diff spec')
#     parser.add_argument('--old', help='before swagger_diff spec')
#     parser.add_argument('--output', default='report.html', help='where do you want the diff?')
#     parsed_args, leftovers = parser.parse_known_args()
#     processed_diff = Diff(parsed_args.old, parsed_args.new, parsed_args.output)
#     processed_diff.is_compatible()
