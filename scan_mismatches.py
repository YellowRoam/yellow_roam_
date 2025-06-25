import os

def scan_file_for_mismatches(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        text = f.read()

    return {
        "file": os.path.basename(filepath),
        "curly": (text.count('{'), text.count('}')),
        "square": (text.count('['), text.count(']')),
        "parens": (text.count('('), text.count(')')),
    }

# Path to your Yellowstone_Fallbacks folder
fallbacks_path = os.path.join(os.getcwd(), "Yellowstone_Fallbacks")
results = []

for filename in os.listdir(fallbacks_path):
    if filename.endswith(".py"):
        filepath = os.path.join(fallbacks_path, filename)
        stats = scan_file_for_mismatches(filepath)

        mismatches = []
        if stats["curly"][0] != stats["curly"][1]:
            mismatches.append(f"{{}} mismatch: {stats['curly']}")
        if stats["square"][0] != stats["square"][1]:
            mismatches.append(f"[] mismatch: {stats['square']}")
        if stats["parens"][0] != stats["parens"][1]:
            mismatches.append(f"() mismatch: {stats['parens']}")

        if mismatches:
            results.append((stats["file"], mismatches))

if results:
    print("\n🛑 Mismatched brackets found:\n")
    for filename, issues in results:
        print(f"{filename}:")
        for issue in issues:
            print(f"  - {issue}")
else:
    print("✅ All logic files passed bracket structure checks.")
