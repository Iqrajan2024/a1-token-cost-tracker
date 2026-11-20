# H1 Assignment 01: Two LLM Provider Cost and Token Tracker

This assignment is a python script that sends the same prompt to two LLM providers, Google Gemini and Groq. Then prints both responses and a performance table comparing the input and output token counts, cost per call (in USD), and the response time (in seconds) for both providers.

# H2 How to run:
1. Clone the repository and navigate into the project.
2. Install the dependencies using **uv sync**.
3. Obtain the free Gemini and Groq API keys from Google AI Studio and GroqCloud and place them in the **.env** file.
4. Run the application using **uv run tracker.py "Your prompt here"**.

# H2 Sample Output
Prompt: Explain AI in simple words

GEMINI RESPONSE:
---------------------------------------------------------------------------
At its simplest, **Artificial Intelligence (AI)** is teaching computers to **think and learn the way humans do**. 

Here is an easy way to understand it:

### 1. Normal Computers vs. AI
* **A normal computer** is like a calculator. It only does exactly what a human tells it to do, step by step. If it meets a problem it hasn’t been programmed for, it gets stuck.
* **An AI computer** is like a student. It learns from experience, spots patterns, and can make decisions or guesses on its own.

---

### 2. How does it learn?
Think about how a toddler learns what a "cat" is. 

You don’t give the toddler a math formula describing a cat. Instead, you point to a cat and say, *"Look, a cat!"* After seeing enough cats, the child’s brain figures out: *fur + whiskers + pointy ears = cat.*

AI learns the exact same way:
1. We feed the computer **millions of pictures** of cats.
2. The computer studies them and finds the **patterns**.
3. Soon, if you show it a brand-new picture, it can say: *"That's a cat!"*

---

### 3. AI you probably already use:
You interact with AI every day without realizing it:
* **Netflix & Spotify:** They notice what you watch or listen to, spot patterns in your taste, and guess what you’ll like next.
* **Siri & Alexa:** They listen to your voice, figure out what words you said, and understand what you mean.
* **Smartphone Face Unlock:** It looks at your face through a camera and recognizes your features, even if you are in the dark or wearing glasses.
* **Google Maps:** It looks at current traffic patterns to predict the fastest route home.

---

### The Big Takeaway
AI doesn't have a soul, feelings, or true "thoughts." 

Instead, it is a very clever machine that looks at mountains of information, finds the patterns, and makes really good guesses about what to do next.


GROQ RESPONSE:
---------------------------------------------------------------------------
**Artificial Intelligence (AI) in a nutshell**

Think of AI as a “smart helper” that a computer can learn to do things that usually need a human brain.

| What it is | How it works | What it can do |
|------------|--------------|----------------|
| **Computer program** | Trains on lots of examples (data). | Recognizes faces, speaks, plays chess, writes music, helps doctors diagnose |
| **Learns patterns** | Finds regularities in the data. | Makes predictions, suggests the next word, finds the best route |
| **Adapts** | Gets better the more data it sees. | Improves its answers over time |

So, AI is like a very fast, very flexible learning machine that can take a pile of information, find useful patterns, and then use those patterns to make decisions or give you answers—just like a human would, but often much quicker.


## LLM PERFORMANCE COMPARISON

| Provider | Input Tokens | Output Tokens | Seconds | Cost (USD) |
|:---------|-------------:|--------------:|--------:|-----------:|
| Gemini   | 6            | 453           | 51.175  | 0.0017032500 |
| Groq     | 76           | 262           | 0.954   | 0.0000843000 |


# H3 Learning outcomes:
This assignment helped me understand and learn how LLM providers are called through their API. I learned how to get the input and output tokens from their actual API usage metadata and calculate the total cost per API call. 