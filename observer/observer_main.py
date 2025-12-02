import argparse
import asyncio
import os
import re
import sys
from pathlib import Path

# Add the project root to the Python path so imports work when running this script directly
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

import yaml

from observer.litter_box_observer import LitterBoxObserver
from observer.models import LitterBoxObserverConfig


def _substitute_env_vars(value):
    """Recursively substitute environment variables in strings, lists, and dicts.
    
    Supports both $VAR and ${VAR} syntax.
    Raises ValueError if an environment variable is not found.
    """
    if isinstance(value, str):
        # Find all environment variable references in the string
        # Matches both $VAR_NAME and ${VAR_NAME}
        pattern = r'\$\{([A-Za-z_][A-Za-z0-9_]*)\}|\$([A-Za-z_][A-Za-z0-9_]*)'
        
        def replace_env_var(match):
            # Extract the variable name (from either capture group)
            var_name = match.group(1) if match.group(1) else match.group(2)
            if var_name not in os.environ:
                raise ValueError(f"Environment variable '{var_name}' is not set")
            return os.environ[var_name]
        
        return re.sub(pattern, replace_env_var, value)
    elif isinstance(value, dict):
        return {k: _substitute_env_vars(v) for k, v in value.items()}
    elif isinstance(value, list):
        return [_substitute_env_vars(item) for item in value]
    else:
        return value


def load_config_from_yaml(yaml_path: str) -> LitterBoxObserverConfig:
    """Load and deserialize YAML config into LitterBoxObserverConfig model.
    
    Environment variables in the form $VAR or ${VAR} will be substituted with
    their actual values. Raises ValueError if a referenced environment variable
    is not set.
    """
    with open(yaml_path, 'r') as f:
        config_dict = yaml.safe_load(f)
    
    # Substitute environment variables
    config_dict = _substitute_env_vars(config_dict)
    
    # Convert YAML dict to Pydantic model
    config = LitterBoxObserverConfig.model_validate(config_dict)
    return config


async def main():
    parser = argparse.ArgumentParser(description='Litter Box Observer Main')
    parser.add_argument(
        '--config',
        type=str,
        required=True,
        help='Path to the YAML configuration file'
    )
    args = parser.parse_args()
    
    # Load config from YAML
    config = load_config_from_yaml(args.config)
    
    # Create observer with config
    observer = LitterBoxObserver(config)
    
    # Begin observing
    await observer.begin_observing()


if __name__ == '__main__':
    asyncio.run(main())

