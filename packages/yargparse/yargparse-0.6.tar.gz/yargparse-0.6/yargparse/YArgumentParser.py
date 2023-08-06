import yaml
import argparse
import ast
import re
from argparse import Namespace

def dicts_to_namespaces(config) -> Namespace:
    """ 
    Translate a dictionary of dictionaries to namespaces of namespaces.  Recursively calls itself until reaching the basecase of not being a 
    dictionary, then returns the value at the leaf


    """
    if not isinstance(config, dict) and not isinstance(config, list):
        return config
    if isinstance(config, dict):
        return Namespace(**{key : dicts_to_namespaces(val) for key, val in config.items()})
    
    return [dicts_to_namespaces(val) for val in config]

class YArgumentParser(argparse.ArgumentParser):
    """
    Layer over argparse that merges YAML configuration with command line overrides.

    Allows some variables to be defined at the CLI, and others to be in the YAML.  CLI will always override
    defaults provided in YAML, if provided in both places.

    To override nested YAML use dot notation, e.g.:
    features
        dim: 100

    can be overridden via --features.dim 1000
    """
    def __init__(self, yaml_flag='-c', yaml_dest='--config', yaml_default=['config.yaml'], **kwargs):
        """
        Initialization including specifying the desired YAML file to use in command line interface.

        Example CLI: python <prog> -c / --config config.yaml

        yaml_flag: the one-dash command line shortcut (e.g., -c)
        yaml_dest: the two-dash command line arg (e.g., --config)
        yaml_default: Default value (e.g., config.yaml)
        """
        super().__init__(**kwargs)
        assert(yaml_flag is None or yaml_flag.startswith('-'))
        assert(yaml_dest.startswith('--'))
        if yaml_flag is not None:       
            self.add_argument(yaml_flag, yaml_dest, default=yaml_default, nargs='+')
        else:
            self.add_argument(yaml_dest, default=yaml_default, nargs='+')

        self.yaml_dest = yaml_dest[2:]

    def parse_args(self, args=None) -> Namespace:
        """
        Overrides argparse's parse_args, to first recover the yaml configuration file and other true CLI,
        then merges the other CLI with the YAML file.

        Lastly, it combines both into a dict, which is translated into a namespace
        """
        args, overrides = super().parse_known_args(args)
        args = vars(args)

        config = {}
        for c in args[self.yaml_dest]:
            with open(c) as fin:
                config = {**config, **yaml.safe_load(fin)}

        arg_none = {key : value for key, value in args.items() if value is None}
        args = {key : value for key, value in args.items() if value is not None}

        overrides = ' '.join(overrides)
        overrides = [s.strip() for s in overrides.split('--') if s != '']

        for override in overrides:
            splitpoint_start = re.search(' |=|:', override).start()
            splitpoint_end = re.search(' |=|:', override).end()

            keystr, value = override[:splitpoint_start], override[splitpoint_end:]
            keys = [key if '[' not in key else int(key[1:-1]) for key in re.findall(r'[a-zA-Z_0-9]+|\[[0-9]+\]', keystr)]
            root = config
            for key in keys[:-1]:
                root = root[key]
                    
            if type(root[keys[-1]]) != str:
                root[keys[-1]] = ast.literal_eval(value)
            else:
                root[keys[-1]] = value

        config = {**config, **args}

        # Merge in the None valued CLI only after no others are present
        arg_none = {key : value for key, value in arg_none.items() if key not in config}
        config = {**config, **arg_none}


        return dicts_to_namespaces(config)
