
# segment_router.py

import json

def load_loops(file_path="logic/family_loops_west_yellowstone_jackson_with_segments.json"):
    with open(file_path, "r") as f:
        return json.load(f)

def find_segment(from_location, to_location, loop_id=None):
    loops = load_loops()
    matches = []

    for i, loop in enumerate(loops):
        if loop_id is not None and i + 1 != loop_id:
            continue
        for segment in loop.get("segments", []):
            if from_location.lower() in segment["from"].lower() and to_location.lower() in segment["to"].lower():
                matches.append({
                    "loop_id": i + 1,
                    "from": segment["from"],
                    "to": segment["to"],
                    "full_route": segment["full_route"],
                    "title": loop["loop_title"]
                })

    return matches if matches else [{"error": "Segment not found in the provided loop(s)."}]