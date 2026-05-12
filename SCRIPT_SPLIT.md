# Recording Script Split — 4 Speakers

Splits the 20-minute video ([SLIDES.md](SLIDES.md) Part a + [DEMO_SCRIPT.md](DEMO_SCRIPT.md)
Part b) across the four team members. Each person speaks for ~5 minutes,
aligned with the role they own in [Slide 1](SLIDES.md#slide-1--team-members--000--100).

| #  | Name             | SJSU ID    | Role-aligned segment                                  | Speaking time |
|----|------------------|------------|-------------------------------------------------------|---------------|
| 1  | Lam Nguyen       | 018229432  | Team intro + allocator-behavior test cases            | ~5:00         |
| 2  | Jahnavi Kedia    | 018282368  | Core/UI features + UI-validation test cases           | ~5:00         |
| 3  | Nishan Paudel    | 018280561  | Architecture + extras + live-data test cases          | ~4:40         |
| 4  | Harishita Gupta  | 018323331  | Challenges + persistence test cases + intro/outro     | ~5:20         |

---

## Master timeline

| Time          | Segment                                | Speaker      |
|---------------|----------------------------------------|--------------|
| 0:00 – 1:00   | Slide 1 — Team Members                 | **Lam**      |
| 1:00 – 2:00   | Slide 2 — Architecture                 | **Nishan**   |
| 2:00 – 3:00   | Slide 3 — Core Features                | **Jahnavi**  |
| 3:00 – 4:00   | Slide 4 — Extra Features               | **Nishan**   |
| 4:00 – 5:00   | Slide 5 — Challenges                   | **Harishita**|
| 5:00 – 5:30   | Demo Intro                             | **Harishita**|
| 5:30 – 6:50   | TC1 — Min investment, single strategy  | **Lam**      |
| 6:50 – 8:10   | TC2 — Below-minimum rejected           | **Jahnavi**  |
| 8:10 – 9:30   | TC3 — No strategy selected             | **Jahnavi**  |
| 9:30 – 10:50  | TC4 — More than 2 strategies blocked   | **Jahnavi**  |
| 10:50 – 12:10 | TC5 — Two strategies combined          | **Lam**      |
| 12:10 – 13:30 | TC6 — Large investment scaling         | **Lam**      |
| 13:30 – 14:50 | TC7 — Live refresh                     | **Nishan**   |
| 14:50 – 16:10 | TC8 — 5-day chart + benchmark          | **Nishan**   |
| 16:10 – 17:30 | TC9 — CSV export                       | **Harishita**|
| 17:30 – 19:00 | TC10 — Save and load portfolio         | **Harishita**|
| 19:00 – 20:00 | Outro                                  | **Harishita**|

---

## Per-speaker assignments

### 1. Lam Nguyen — Team intro + allocator/strategy demos (~5:00)

**Owns:** Allocation Engine & Strategy Mapping → demos that show *how* money
is split and *which* tickers each strategy returns.

- **Slide 1 — Team Members** ([SLIDES.md:17](SLIDES.md#slide-1--team-members--000--100))
  Use the existing narration verbatim. Introduces all four team members.
- **TC1 — Minimum investment, single strategy** ([DEMO_SCRIPT.md:38](DEMO_SCRIPT.md#test-case-1-minimum-investment-single-strategy-030--150))
  Shows the 5-ticker equal-weight result for `$5,000` + Index Investing.
- **TC5 — Two strategies combined and deduped** ([DEMO_SCRIPT.md:84](DEMO_SCRIPT.md#test-case-5-two-strategies-combined-550--710))
  Shows `combine_tickers` in [engine/strategies.py](engine/strategies.py).
- **TC6 — Large investment scales correctly** ([DEMO_SCRIPT.md:96](DEMO_SCRIPT.md#test-case-6-large-investment-single-strategy-710--830))
  Shows share counts inversely proportional to price at `$100,000`.

> **Hand-off line at end of Slide 1:** "Nishan will walk you through the
> architecture."

---

### 2. Jahnavi Kedia — Core features + UI-validation demos (~5:00)

**Owns:** Streamlit UI & Visualization → demos that exercise the input
validation and the multiselect behavior in [app.py](app.py).

- **Slide 3 — Core Features** ([SLIDES.md:70](SLIDES.md#slide-3--core-features--200--300))
- **TC2 — Below-minimum rejected** ([DEMO_SCRIPT.md:51](DEMO_SCRIPT.md#test-case-2-below-minimum-rejected-150--310))
- **TC3 — No strategy selected** ([DEMO_SCRIPT.md:62](DEMO_SCRIPT.md#test-case-3-no-strategy-selected-310--430))
- **TC4 — More than 2 strategies blocked** ([DEMO_SCRIPT.md:72](DEMO_SCRIPT.md#test-case-4-more-than-2-strategies-blocked-430--550))

> **Hand-off line at end of Slide 3:** "Nishan will cover the extras we
> built on top of the spec."
> **Hand-off line at end of TC4:** "Lam will demo combining two strategies."

---

### 3. Nishan Paudel — Architecture + extras + live-data demos (~4:40)

**Owns:** Market Data Integration & Portfolio Valuation → owns architecture
diagram, the extras list (most extras are data/visualization features), and
the two test cases that touch live yfinance.

- **Slide 2 — Architecture** ([SLIDES.md:40](SLIDES.md#slide-2--overall-architecture--100--200))
- **Slide 4 — Extra Features** ([SLIDES.md:97](SLIDES.md#slide-4--extra-features--300--400))
- **TC7 — Live refresh re-pulls prices** ([DEMO_SCRIPT.md:108](DEMO_SCRIPT.md#test-case-7-live-refresh-updates-value-830--950))
- **TC8 — 5-day chart + SPY benchmark** ([DEMO_SCRIPT.md:120](DEMO_SCRIPT.md#test-case-8-5-day-chart-with-reference-line-950--1110))

> **Hand-off line at end of Slide 2:** "Jahnavi will walk through the core
> features visible in the dashboard."
> **Hand-off line at end of Slide 4:** "Harishita will close the slides
> with the challenges we hit."
> **Hand-off line at end of TC8:** "Harishita will finish with CSV export
> and the save/load workflow."

---

### 4. Harishita Gupta — Challenges + persistence demos + intro/outro (~5:20)

**Owns:** Persistence, Testing & Documentation → frames the challenges
slide (it's mostly about persistence + caching trade-offs), bookends the
demo, and runs the two persistence-related test cases.

- **Slide 5 — Challenges** ([SLIDES.md:122](SLIDES.md#slide-5--challenges--400--500))
- **Demo Intro** ([DEMO_SCRIPT.md:29](DEMO_SCRIPT.md#intro-000--030))
- **TC9 — CSV export** ([DEMO_SCRIPT.md:133](DEMO_SCRIPT.md#test-case-9-csv-export-1110--1230))
- **TC10 — Save and load portfolio** ([DEMO_SCRIPT.md:144](DEMO_SCRIPT.md#test-case-10-save-and-load-portfolio-1230--1400))
- **Outro** ([DEMO_SCRIPT.md:159](DEMO_SCRIPT.md#outro-1400--1500))

> **Hand-off line at end of Slide 5:** "That's the slide deck — let's switch
> to the live demo."
> **Hand-off line at end of Demo Intro:** "Lam will start with Test Case 1."

---

## Recording tips

- **Screen-share owner:** whoever is currently speaking should drive the
  Streamlit tab so cursor movement matches the voice. Pre-agree who passes
  control after each segment.
- **Build state between cases:** TC2/3/4 don't need a fresh build, but TC5,
  TC6, TC7, TC8, TC9, TC10 each need a fresh `Build Portfolio` click with the
  amounts shown in [TEST_CASES.md](TEST_CASES.md). Practice the click order
  once before recording.
- **Hand-off cadence:** add a 1-second pause at each speaker change so the
  editor can cut cleanly if you record segments separately.
- **Backup plan:** if yfinance throws an error during TC7 or TC8 in the live
  take, Nishan should narrate the cache fallback (mention the 60-second TTL
  in [engine/data_provider.py](engine/data_provider.py)) and re-click
  `Refresh Live Prices` once.
