import os
import sys
import json
import time

from dotenv import load_dotenv
from google import genai
from groq import Groq


# 1. LOAD ENVIRONMENT VARIABLES

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

GEMINI_MODEL = os.getenv(
    "GEMINI_MODEL",
    "gemini-3.6-flash"
)

GROQ_MODEL = os.getenv(
    "GROQ_MODEL",
    "openai/gpt-oss-20b"
)


# 2. MODEL PRICING (USD PER MILLION TOKENS)

PRICING = {
    "gemini": {
        "input": 0.75,
        "output": 3.75
    },

    "groq": {
        "input": 0.075,
        "output": 0.30
    }
}


# 3. FUNCTION TO CALCULATE API COST PER CALL


def calculate_cost(
    input_tokens,
    output_tokens,
    input_price,
    output_price
):

    input_cost = (
        input_tokens * input_price
    ) / 1_000_000

    output_cost = (
        output_tokens * output_price
    ) / 1_000_000

    total_cost = input_cost + output_cost

    return total_cost


# 4. GEMINI API FUNCTION

def call_gemini(prompt):

    print("\nCalling Google Gemini...")

    client = genai.Client(
        api_key=GEMINI_API_KEY
    )

    start_time = time.perf_counter()

    response = client.models.generate_content(
        model=GEMINI_MODEL,
        contents=prompt
    )

    elapsed_time = time.perf_counter() - start_time

    # Get actual token usage from API
    usage = response.usage_metadata

    if usage is None:
        raise RuntimeError(
            "Gemini did not return usage metadata."
        )

    input_tokens = usage.prompt_token_count
    output_tokens = usage.candidates_token_count

    if input_tokens is None or output_tokens is None:
        raise RuntimeError(
            "Gemini returned incomplete token counts."
        )

    reply = response.text or ""

    # Get pricing
    input_price = PRICING["gemini"]["input"]
    output_price = PRICING["gemini"]["output"]

    # Calculate cost
    cost = calculate_cost(
        input_tokens,
        output_tokens,
        input_price,
        output_price
    )

    return {
        "provider": "gemini",
        "model": GEMINI_MODEL,
        "reply": reply,
        "input_tokens": input_tokens,
        "output_tokens": output_tokens,
        "input_price_per_m": input_price,
        "output_price_per_m": output_price,
        "cost_usd": cost,
        "seconds": elapsed_time
    }


# 5. GROQ API FUNCTION

def call_groq(prompt):

    print("\nCalling Groq...")

    client = Groq(
        api_key=GROQ_API_KEY
    )

    start_time = time.perf_counter()

    response = client.chat.completions.create(

        model=GROQ_MODEL,

        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    elapsed_time = time.perf_counter() - start_time

    # Get actual token usage from API
    usage = response.usage

    if usage is None:
        raise RuntimeError(
            "Groq did not return usage metadata."
        )

    input_tokens = usage.prompt_tokens
    output_tokens = usage.completion_tokens

    if input_tokens is None or output_tokens is None:
        raise RuntimeError(
            "Groq returned incomplete token counts."
        )

    reply = response.choices[0].message.content or ""

    # Get pricing
    input_price = PRICING["groq"]["input"]
    output_price = PRICING["groq"]["output"]

    # Calculate cost
    cost = calculate_cost(
        input_tokens,
        output_tokens,
        input_price,
        output_price
    )

    return {
        "provider": "groq",
        "model": GROQ_MODEL,
        "reply": reply,
        "input_tokens": input_tokens,
        "output_tokens": output_tokens,
        "input_price_per_m": input_price,
        "output_price_per_m": output_price,
        "cost_usd": cost,
        "seconds": elapsed_time
    }


# 6. DISPLAY RESULTS

def display_results(results):

    print("\n")
    print("=" * 75)

    print("                 LLM PERFORMANCE COMPARISON")

    print("=" * 75)

    print(
        f"{'Provider':<12}"
        f"{'Input':<12}"
        f"{'Output':<12}"
        f"{'Seconds':<12}"
        f"{'Cost (USD)':<15}"
    )

    print("-" * 75)

    for result in results:

        print(
            f"{result['provider']:<12}"
            f"{result['input_tokens']:<12}"
            f"{result['output_tokens']:<12}"
            f"{result['seconds']:<12.3f}"
            f"{result['cost_usd']:<15.10f}"
        )

    print("-" * 75)


# 7. SAVE RESULTS TO JSON

def save_results(results):
    
    saved_results = []

    required_fields = [
        "provider",
        "model",
        "reply",
        "input_tokens",
        "output_tokens",
        "input_price_per_m",
        "output_price_per_m",
        "cost_usd"
    ]

    for result in results:

        saved_results.append({
            key: result[key]
            for key in required_fields
        })

    with open(
        "results.json",
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            saved_results,
            file,
            indent=4,
            ensure_ascii=False
        )

   
# 8. MAIN FUNCTION

def main():

    # Read prompt from command line
    if len(sys.argv) < 2:

        print(
            'Usage: uv run tracker.py "Give your prompt here"'
        )

        sys.exit(1)

    prompt = " ".join(sys.argv[1:])

    # Check API keys
    if not GEMINI_API_KEY or not GROQ_API_KEY:

        print("ERROR: Missing API keys.")

        print("Please check your .env file.")

        sys.exit(1)

    print("\n" + "=" * 75)

    print("                 LLM COST & TOKEN TRACKER")

    print("=" * 75)

    print("\nPrompt:", prompt)

    results = []

    try:

        # Call Gemini
        gemini_result = call_gemini(prompt)

        results.append(gemini_result)

        print("\nGEMINI RESPONSE:")
        print("-" * 75)

        print(gemini_result["reply"])

        # Call Groq
        groq_result = call_groq(prompt)

        results.append(groq_result)

        print("\nGROQ RESPONSE:")
        print("-" * 75)

        print(groq_result["reply"])

        # Display comparison
        display_results(results)

        # Save JSON
        save_results(results)

    except Exception as error:

        print("\nERROR:", error)

        print(
            "\nCheck your API keys, model names, "
            "internet connection, and API limits."
        )

        sys.exit(1)


if __name__ == "__main__":

    main()