# -*- coding: utf-8 -*-
import json

def printWarning(msg):
    print("[WARNING] ", msg)

def printFatal(msg):
    print("[FATAL] ", msg)

def printException(msg):
    print("[EXCEPTION] ", msg)

def printInfo(msg):
    print("[INFO] ", msg)

def raiseException(msg):
    raise Exception(msg)

def read_dict(fn):
    return set([word.strip() for word in open(fn, encoding="utf8")])

def divide_chunks(l, n):
    return [l[i:i + n] for i in range(0, len(l), n)]

def read_list(fname, remove_dup=False):
    list_obj = [line.strip() for line in open(fname, "r", encoding="utf8")]
    if remove_dup:
        list_obj = list(set(list_obj))
    return list_obj

def read_json(fname):
    return json.load(open(fname, "r", encoding="utf8"))
