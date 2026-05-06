from carla_nuscenes.generator import Generator
import os
import yaml

# Store the script's working directory as the reference point
_SCRIPT_ROOT = os.getcwd()

def yaml_include(loader, node):
    file_path = loader.construct_scalar(node)

    # If path is already absolute, use it directly
    if os.path.isabs(file_path):
        full_path = file_path
    else:
        # Resolve relative to the script's working directory
        full_path = os.path.join(_SCRIPT_ROOT, file_path.lstrip('./'))

    # Normalize path
    full_path = os.path.normpath(full_path)

    with open(full_path, 'r') as f:
        return yaml.load(f, Loader=yaml.FullLoader)

yaml.add_constructor('!include', yaml_include, Loader=yaml.FullLoader)
# --------------------------------

config_path = "./configs/config.yaml"

with open(config_path, 'r') as f:
    config = yaml.load(f, Loader=yaml.FullLoader)

runner = Generator(config)

if os.path.exists(config["dataset"]["root"]):
    runner.generate_dataset(True)
else:
    runner.generate_dataset(False)