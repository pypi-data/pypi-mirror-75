#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jul 18 16:16:08 2020

@author: shane
"""

import csv

from tabulate import tabulate

from .utils import remote


def list_nutrients():
    response = remote.request("/nutrients")
    results = response.json()["data"]

    table = tabulate(results, headers="keys", tablefmt="presto")
    print(table)
    return table


def sort_foods_by_nutrient_id(id, by_kcal=False):
    response = remote.request("/foods/sort", params={"nutr_id": id})
    results = response.json()["data"]
    # TODO: if err

    sorted_foods = results["sorted_foods"]

    nutrients = results["nutrients"]
    nutrient = nutrients[str(id)]
    units = nutrient["units"]

    fdgrp = results["fdgrp"]

    for x in sorted_foods:
        id = str(x["fdgrp"])
        units = nutrient["units"]
        x["fdgrp"] = f"{fdgrp[id]['fdgrp_desc']} [{id}]"
        x[f"value ({units})"] = x["value"]
        del x["value"]
    # for
    table = tabulate(sorted_foods, headers="keys", tablefmt="presto")
    print(table)
    return table


def sort_foods_by_kcal_nutrient_id(id):
    response = remote.request("/foods/sort", params={"nutr_id": id, "by_kcal": True})
    results = response.json()["data"]
    # TODO: if err

    sorted_foods = results["sorted_foods"]

    nutrients = results["nutrients"]
    nutrient = nutrients[str(id)]
    units = nutrient["units"]

    fdgrp = results["fdgrp"]

    for x in sorted_foods:
        id = str(x["fdgrp"])
        units = nutrient["units"]
        x["fdgrp"] = f"{fdgrp[id]['fdgrp_desc']} [{id}]"
        x[f"value ({units})"] = x["value"]
        del x["value"]
    # for
    table = tabulate(sorted_foods, headers="keys", tablefmt="presto")
    print(table)
    return table


def day_analyze(day_csv, rda_csv=None):
    day_csv_input = csv.DictReader(day_csv)

    log = []
    for row in day_csv_input:
        log.append(row)

    rda = []
    if rda_csv:
        rda_csv_input = csv.DictReader(rda_csv)
        for row in rda_csv_input:
            rda.append(row)

    response = remote.request("/day/analyze", body={"log": log, "rda": rda})
    results = response.json()["data"]

    totals = results["nutrient_totals"]
    print(totals)
