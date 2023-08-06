import json
import yaml
import os
from functools import reduce


def deep_get(dictionary, keys, default=None):
    return reduce(lambda d, key: d.get(key, default) if isinstance(d, dict) else default, keys.split("."), dictionary)


class OpenApiSpecDiff(object):
    def __init__(self, spec_one_path, spec_two_path):
        if spec_one_path:
            spec_one = self._scan_input_spec(spec_one_path)
        else:
            spec_one = {}
        spec_two = self._scan_input_spec(spec_two_path)
        print("\n\t\t\t\t\t\t\t\t\t----------------- Open API Spec Diff Tool: Start -----------------")
        print("\n\tBaseline Spec: " + str(spec_one_path))
        print("\tNew Spec: " + str(spec_two_path) + "\n")
        self.diff = self._compare_spec_files(spec_one, spec_two)
        print("\n\t\t\t\t\t\t\t\t\t----------------- Open API Spec Diff Tool: Completed -----------------")

    def scan_input_spec(self, input_path):
        return self._scan_input_spec(input_path)

    def _process_nested_params(self, input_spec, info, lastkey, nested_data={}):
        for name, desc in deep_get(input_spec, info).get("properties").items():
            to_process = desc
            if lastkey not in nested_data:
                nested_data[lastkey] = {}
            if type(nested_data[lastkey]) is dict:
                nested_data[lastkey].update({name: "$"+name+"$"})
            else:
                nested_data[lastkey] = {name: "$"+name+"$"}
            while (1):
                if "$ref" not in to_process:
                    break
                _ = to_process.get('$ref')
                _ = _.replace("#/", "").replace("/", ".")
                nested_data[lastkey][name] = _
                _ = self._process_nested_params(input_spec, _, name, nested_data[lastkey])
                to_process = _
        return nested_data

    def _process_reqbody(self, input_spec, info):
        for k, v in info.get("content").items():
            for ref, schema_def in v.get("schema").items():
                schema_def = schema_def.replace("#/", "").replace("/", ".")
                detailed_info = deep_get(input_spec, schema_def)
                params = []
                for p, pspec in detailed_info.get("properties").items():
                    if pspec.get("type") == "array":
                        nparams = []
                        for i, j in pspec.get("items").items():
                            _ = j.replace("#/", "").replace("/", ".")
                            _ = self._process_nested_params(input_spec, _, p,{})
                            nparams.append({p:[_[p]]})
                        params.append({"in": "body", "name": p, "value": nparams})
                    elif pspec.get("type") == "object":
                        _ = pspec.get('$ref')
                        _ = _.replace("#/", "").replace("/", ".")
                        _ = self._process_nested_params(input_spec, _, p,{})
                        params.append({'in': 'body', "name": p, "value": _})
        return params

    def _scan_input_spec(self, input_path):
        if os.path.isdir(input_path):
            input_spec = {}
            for (root, dirs, files) in os.walk(input_path, topdown=True):
                for file in files:
                    if ".json" in file or ".yaml" in file or ".yml" in file:
                        print("Parsing the SPEC file: " + str(file))
                        try:
                            with open(os.path.join(root, file)) as specobj:
                                if ".json" in file:
                                    input = json.loads(specobj.read())
                                else:
                                    input = yaml.load(specobj.read())
                                if "swagger" not in input or "openapi" not in input:
                                    continue
                                if not input_spec:
                                    input_spec = input
                                else:
                                    input_spec["paths"].update(input.get("paths"))
                        except:
                            print("ignoring the SPEC " + str(file) + " due to unforseen exception")
        else:
            with open(input_path) as specobj:
                if ".json" in input_path:
                    input_spec = json.loads(specobj.read())
                elif ".yaml" in input_path or ".yml" in input_path:
                    input_spec = yaml.load(specobj.read())
        for api, api_info in input_spec["paths"].items():
            for method, method_info in api_info.items():
                to_replace = []
                if "requestBody" in method_info:
                    to_replace += self._process_reqbody(input_spec, method_info["requestBody"])
                if "parameters" in method_info:
                    for each in method_info["parameters"]:
                        if type(each) is dict:
                            for k, v in each.items():
                                if k == "$ref":
                                    v = v.replace("#/", "")
                                    v = v.replace("/", ".")
                                    to_replace.append(deep_get(input_spec, v))
                    if to_replace:
                        for _ in method_info["parameters"]:
                            if type(_) is dict:
                                for k, v in _.items():
                                    if "$ref" not in k:
                                        if _ not in to_replace:
                                            to_replace.append(_)
                        input_spec["paths"][api][method]["parameters"] = to_replace
        return input_spec

    def scan_input_spec(self, input_path):
        return self._scan_input_spec(input_path)

    @staticmethod
    def _pretty_print(specdiff):
        print(" (+) New API(s):\n")
        for api, params in specdiff["new"].items():
            print("------------" * 20)
            print("........... " + str(api) + "\n")
            print("                                   Parameter(s): " + str(params) + "\n")
            print("------------" * 20)
        print(" (.) Modified API(s):\n")
        for api, params in specdiff["changed"].items():
            print("------------" * 20)
            print("........... " + str(api) + "\n")
            print("                                   New/Modified Parameter(s): " + str(params) + "\n")
            print("------------" * 20)

    @staticmethod
    def _compare_spec_files(spec_one, spec_two):
        diff = {"new": {}, "changed": {}}
        basepath = spec_one.get("basePath", "/")
        for apipath in spec_two["paths"]:
            api_endpoint = basepath + apipath
            method_spec_two = list(spec_two["paths"][apipath].keys())
            if apipath not in spec_one.get("paths", {}):
                for method in spec_two["paths"][apipath]:
                    diff["new"].update({apipath: {method: spec_two["paths"][apipath][method].get("parameters", [])}})
            else:
                new_params = []
                for method in spec_two["paths"][apipath]:
                    new_params = [_ for _ in spec_two["paths"][apipath][method].get("parameters", []) if
                                  _["name"] not in [x["name"] for x in
                                                    spec_one["paths"][apipath][method].get("parameters", [])]]
                    if new_params:
                        diff["changed"].update({apipath: {method: new_params}})
        OpenApiSpecDiff._pretty_print(diff)
        return diff


def main():
    import sys
    print("*****" * 20)
    print("CloudVector APIShark - OpenAPI spec diff checker plugin")
    print("*****" * 20)
    input_spec_one = input("Enter absolute path to Old API SPEC(Version A): ")
    input_spec_two = input("Enter absolute path to New API SPEC(Version B) : ")
    OpenApiSpecDiff(input_spec_one, input_spec_two).diff


if __name__ == "__main__":
    main()
