import sys
import argparse

def generate_metadata(topic, flavor, frequency):
    # The SEO Engine
    title = f"{frequency} | {topic} for The DEEPEST Healing Sleep: Whole Body Regeneration (10 Hours {flavor.title()})"
    
    description = f"""
🌿 **Welcome to Aura Labs** 🌿
*Your sanctuary for cellular restoration and soul-deep peace.*

This 10-hour journey is engineered specifically for **{topic.lower()}**. Using a mathematically precise {frequency} carrier signal, we facilitate the transition into the Delta state—the most critical frequency for physical healing.

✨ **The Science of this Track:**
* **Frequency:** {frequency} (Solfeggio/Binaural Offset)
* **Flavor:** {flavor.title()} Ambiance for acoustic masking.
* **Benefit:** Designed specifically to target {topic.lower()}.

🌌 **Breathe in stillness. Exhale tension. Feel the shift.**

#AuraLabs #HealingFrequencies #SleepScience #{flavor.replace(' ', '')} #DeepSleep #10Hours
"""
    
    tags = f"{topic}, Aura Labs, healing frequencies, sleep science, 10 hours {flavor}, binaural beats, delta waves, sound therapy"

    print("\n" + "="*20 + " SEO METADATA " + "="*20)
    print(f"TITLE:\n{title}\n")
    print(f"DESCRIPTION:\n{description}")
    print(f"TAGS:\n{tags}")
    print("="*54)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--topic", help="What is the video about? (e.g., Stress Relief)")
    parser.add_argument("--flavor", help="Rain, Stars, or Nebula")
    parser.add_argument("--freq", help="e.g., 528Hz + 432Hz")
    args = parser.parse_args()
    
    generate_metadata(args.topic, args.flavor, args.freq)
