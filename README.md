# 🌐 PageRank AI — Markov Chain Sampling & Iterative Graph Model

![Python](https://img.shields.io/badge/python-v3.12+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-brightgreen.svg)

An AI implementation of Google's original **PageRank algorithm** designed to measure the relative importance of web pages through **Markov Chain Random Walk Sampling** and **Iterative Algebraic Graph Models**.

Developed as part of **Harvard's CS50's Introduction to Artificial Intelligence with Python course**.

---

## 💡 About the Project

When search engines rank web pages, they need a way to quantify importance beyond simple keyword matching. PageRank solves this by treating the web as a directed graph where hyperlinks act as votes of confidence. A page is considered important if it is linked to by other important pages, creating a recursive structure.

This project implements two distinct approaches to calculate PageRank:

1. **Sampling Model (Monte Carlo Simulation):** Simulates a random surfer navigating the web via a Markov Chain, recording time spent on each page across $N$ steps.
2. **Iterative Model (Algebraic Matrix Convergence):** Mathematically solves the recursive PageRank equation repeatedly across all graph nodes until probabilities reach numeric convergence ($< 0.001$).

### Key Highlights:

* **Damping Factor ($d = 0.85$):** Models user behavior where a surfer follows links $85\%$ of the time and jumps to a completely random page $15\%$ of the time.
* **Handling Dangling Nodes:** Automatically converts pages without outgoing links into links to all pages in the corpus, preventing probability sinks.
* **Monte Carlo Random Walk:** Uses `random.choices` with weighted probabilities to simulate non-deterministic web navigation.
* **Mathematical Convergence Engine:** Guarantees precision by updating state distributions simultaneously using historical snapshot copies until strict stability is achieved.

---

## 🧠 How the Algorithms Work

### 1. The Damping Factor & Transition Model

The transition model defines the probability distribution of moving from page $P$ to any other page in the corpus:

$$PR(p) = \frac{1 - d}{N} + d \left( \frac{1}{\text{NumLinks}(P)} \right)$$

* **Probability $1 - d$:** The user gets bored and jumps to any page in the entire corpus chosen uniformly at random.
* **Probability $d$:** The user clicks one of the hyperlinks on the current page chosen uniformly at random.

---

### 2. Sample PageRank (Monte Carlo Simulation)

Simulates $n$ steps of a random web surfer to estimate PageRank by frequency of visits.

```
[Start at Random Page] ──> [Calculate Transition Model] ──> [Sample Next Page (Weighted)] ──> [Increment Counter]
                                     ▲                                                             │
                                     └────────────────────── Loop (n - 1) times ───────────────────┘

```

1. **Step 1:** Select the initial page uniformly at random from the corpus.
2. **Steps 2 to $n$:** Generate a probability distribution for the current page using `transition_model()`. Symmetrically select the next page based on those weights using `random.choices()`.
3. **Normalization:** Divide total visit counts by $n$ to convert frequencies into a normalized probability distribution summing to $1.0$.

---

### 3. Iterative PageRank (Algebraic Graph Convergence)

Calculates the exact PageRank mathematically by recursively updating the PageRank equation across all pages $p$ simultaneously:

$$PR(p) = \frac{1 - d}{N} + d \sum_{i \in \text{Inbound}(p)} \frac{PR(i)}{\text{NumLinks}(i)}$$

Where $\text{Inbound}(p)$ represents all pages $i$ that contain a hyperlink pointing to page $p$.

1. **Initialization:** Every page starts with an equal probability of $1 / N$.
2. **Synchronous Update:** At each iteration, calculate $PR_{\text{new}}(p)$ for all pages using values strictly from $PR_{\text{old}}$.
3. **Convergence Test:** Repeat the update cycle until $\vert{}PR_{\text{new}}(p) - PR_{\text{old}}(p)\vert{} \le 0.001$ for every page in the corpus.

---

### 4. Sampling vs. Iterative Comparison

| Feature | Sample PageRank (Monte Carlo) 🎲 | Iterative PageRank (Algebraic) 📐 |
| --- | --- | --- |
| **Methodology** | Non-deterministic random walk simulation | Deterministic mathematical convergence |
| **Accuracy** | Approximates values (higher $n$ increases precision) | Exact mathematical values |
| **Time Complexity** | $O(n)$ where $n$ is the number of samples | $O(k \cdot \vert{}V\vert{} \cdot \vert{}E\vert{})$ where $k$ is iterations |
| **Edge Case Handling** | Handles dangling nodes step-by-step | Transforms empty node sets into complete graph connections |
| **Execution Speed** | Dependent on sample size $n$ | Extremely fast, converging in few iterations |

---

## 🛠️ Built With

* **Language:** Python 3.12+
* **Standard Libraries:** `random`, `sys`
* **Paradigms:** Object-Oriented Programming (OOP) / Markov Chains / Graph Theory / Iterative Numerical Methods

---

## 🚀 Getting Started

### Prerequisites

Ensure you have **Python 3.12+** installed on your system.

### Installation & Execution

1. **Clone the repository:**
```bash
git clone https://github.com/felipemarcioli/PageRank-AI.git
cd PageRank-AI
```

2. **Run the PageRank algorithm on a corpus:**
```bash
python pagerank.py corpus0
```



---

## 📁 Repository Structure

```
├── corpus0/                       # Example web corpus 0 (HTML files with hyperlinks)
│   ├── 1.html
│   ├── 2.html
│   └── 3.html
├── corpus1/                       # Example web corpus 1
├── corpus2/                       # Example web corpus 2
├── LICENSE                        # Project license (MIT)
├── pagerank.py                    # [Developed by me] Core PageRank logic (transition_model, sample_pagerank, iterate_pagerank)
└── README.md                      # Project documentation
```

---

## 📄 License

This project is licensed under the [MIT License](https://www.google.com/search?q=./LICENSE). Feel free to use, modify, and distribute it for learning purposes.

---

## 📞 Contact

If you have any questions or would like to get in touch, feel free to email me at: felipemmarcioli@gmail.com