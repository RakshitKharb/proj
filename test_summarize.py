# test_summarize.py

from utils.text_generation import summarize_text

def main():
    sample_text = """
    Renewable energy is energy that is collected from renewable resources, which are naturally replenished on a human timescale, such as sunlight, wind, rain, tides, waves, and geothermal heat. Renewable energy often provides energy in four important areas: electricity generation, air and water heating/cooling, transportation, and rural energy services. The use of renewable energy sources is important for environmental sustainability, reducing greenhouse gas emissions, and decreasing dependence on fossil fuels.
    """
    summary = summarize_text(sample_text, max_new_tokens=150)  # Ensure using max_new_tokens
    print("Summary:", summary)

if __name__ == "__main__":
    main()
