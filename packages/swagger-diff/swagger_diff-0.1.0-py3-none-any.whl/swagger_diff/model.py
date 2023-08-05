#!/usr/bin/python
# -*- coding: UTF-8 -*-
from enum import Enum
from pydantic import BaseModel
from typing import List, Text, Dict, Optional


class MethodEnum(Text, Enum):
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    DELETE = "DELETE"
    HEAD = "HEAD"
    OPTIONS = "OPTIONS"
    PATCH = "PATCH"


class StatusEnum(Text, Enum):
    ADD = "Add"
    DELETE = "Delete"


class PathItem(BaseModel):
    method: MethodEnum = MethodEnum.GET
    path: str
    summary: str


class AddedItem(PathItem):
    pass


class RemovedItem(PathItem):
    pass


class Parameter(BaseModel):
    status: str
    name: str
    description: str = None


class Produces(BaseModel):
    pass


class ChangedItem(PathItem):
    parameters: List[Parameter]
    produces: List[Produces] = []