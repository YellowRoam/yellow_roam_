import importlib.util
import logging
from pathlib import Path
from prototype.match_local_logic import match_fallback

logger = logging.getLogger(__name__)

def load_all_fallback_entries(package_name: str):
    entries = []
    fallback_dir = Path(__file__).parent.parent / package_name

    for file_path in fallback_dir.glob("*.py"):
        if file_path.name == "__init__.py":
            continue

        module_name = f"{package_name}.{file_path.stem}"

        try:
            spec = importlib.util.spec_from_file_location(module_name, file_path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)

            module_entries = getattr(module, "entries", [])

            if isinstance(module_entries, list):
                entries.extend(module_entries)
                logger.info(f"Loaded {len(module_entries)} entries from {file_path.name}")
            else:
                logger.warning(f"{file_path.name} has no valid `entries` list")
        except Exception as e:
            logger.error(f"Failed to import {file_path.name}: {e}")

    logger.info(f"Total fallback entries loaded: {len(entries)}")
    return entries

def route_fallback(user_input: str):
    entries = load_all_fallback_entries("Yellowstone_Fallbacks")
    return match_fallback(user_input, entries)
