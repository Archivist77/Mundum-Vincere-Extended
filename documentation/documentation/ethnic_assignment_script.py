import requests
from pathlib import Path
import time

# Define ethnic keywords to scan for in Wikipedia summaries
ETHNIC_KEYWORDS = {
    "mediterranean": ["greek", "roman", "italian", "mediterranean", "hellenic"],
    "egyptian": ["egyptian", "nile", "pharaoh", "coptic"],
    "north_african": ["berber", "numidian", "north african"],
    "arabic": ["arab", "arabic", "arabian"],
    "african": ["nubian", "ethiopian", "african"],
    "caucasiandark": ["caucasian", "armenian", "georgian", "colchis"],
    "eastasian": ["chinese", "han", "east asian", "qin", "han dynasty"],
    "indian": ["indian", "maurya", "gupta"],
    "unknown": []
}

DEFAULT_ETHNICITY = [("unknown", 100)]

def wiki_summary(place_name):
    """Fetch Wikipedia summary for the place."""
    url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{place_name.replace(' ', '_')}"
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            data = response.json()
            return data.get("extract", "")
    except Exception as e:
        print(f"Failed to fetch Wikipedia summary for {place_name}: {e}")
    return ""

def infer_ethnicity_from_text(text):
    """Infer ethnicity percentages based on keyword frequency."""
    text_lower = text.lower()
    counts = {eth: 0 for eth in ETHNIC_KEYWORDS if eth != "unknown"}

    for eth, keywords in ETHNIC_KEYWORDS.items():
        if eth == "unknown":
            continue
        for kw in keywords:
            counts[eth] += text_lower.count(kw.lower())

    total = sum(counts.values())
    if total == 0:
        return DEFAULT_ETHNICITY

    distribution = []
    for eth, cnt in counts.items():
        if cnt > 0:
            pct = round(cnt / total * 100)
            distribution.append((eth, pct))
    return distribution

def build_region_block(region, ethnicities):
    block = f"\t{region}\n\t{{\n"
    for eth, dist in ethnicities:
        block += "\n\t\tvariant\n\t\t{{\n"
        block += f"\t\t\tethnicity {eth}\n"
        block += f"\t\t\tdistribution {dist}\n"
        block += "\t\t}}\n"
    block += "\t}}\n"
    return block

def main():
    input_file = "places_input.txt"  # Your list of places
    output_file = "places_ethnicity_output.txt"
    unmapped_log_file = "places_unmapped_log.txt"

    with open(input_file, encoding="utf-8") as f:
        places = [line.strip() for line in f if line.strip()]

    output_blocks = "region\n{\n\n"
    unmapped = []

    for place in places:
        summary = wiki_summary(place)
        if not summary:
            unmapped.append(place)
            ethnicities = DEFAULT_ETHNICITY
        else:
            ethnicities = infer_ethnicity_from_text(summary)
            if ethnicities == DEFAULT_ETHNICITY:
                unmapped.append(place)
        output_blocks += build_region_block(place, ethnicities) + "\n"
        time.sleep(0.5)  # be nice to Wikipedia servers

    output_blocks += "}"

    Path(output_file).write_text(output_blocks, encoding="utf-8")
    Path(unmapped_log_file).write_text("\n".join(unmapped), encoding="utf-8")

    print(f"Ethnic data written to {output_file}")
    print(f"Unmapped places logged to {unmapped_log_file}")

if __name__ == "__main__":
    main()
