# TaxWatchdog — Data Processing & Architecture

[![Website](https://img.shields.io/badge/Website-taxwatchdog.ca-blue)](https://taxwatchdog.ca)

**TaxWatchdog** is an open-data web platform designed to provide transparent, long-term municipal financial intelligence for Ontario taxpayers. This repository contains the public documentation, issue tracker, and data aggregation methodology utilized by the platform.

Visit the live platform at **[taxwatchdog.ca](https://taxwatchdog.ca)**.

## Overview

The platform processes and aggregates 25 years of Ontario Financial Information Return (FIR) datasets (2000–2024). To ensure high performance and instantaneous querying on the client side without the latency of server round-trips, the raw municipal financial data is cleaned, calibrated, and mathematically aggregated into a highly optimized 106.4 MB seed file. 

## Technical Architecture

TaxWatchdog is built with a modern, serverless edge architecture prioritizing speed, local data processing, and zero-telemetry privacy. 

- **Frontend:** React and Vite
- **Edge Database (Point Lookups):** Cloudflare D1 (Serverless SQLite at the edge)
- **In-Browser Data Engine (Heavy Analytics):** DuckDB-WASM running in a dedicated WebWorker with an LRU query cache.
- **Edge SEO Routing:** Cloudflare Workers utilizing `HTMLRewriter` to inject dynamic, SEO-compliant canonical titles and meta tags directly into the static HTML stream for programmatic search indexing (bypassing the need for a Node.js SSR server).

### Architecture Deep Dive: Why Edge + WASM?

Hosting 25 years of normalized government data across 444 jurisdictions on a traditional managed cloud database incurs heavy, fixed baseline costs just sitting idle, plus compute and egress fees. For an independent, ad-free civic open-data project, that architecture was unsustainable. 

We eliminated persistent database server overhead by adopting a hybrid model. Basic lookups and primary dashboards resolve instantly via edge D1 APIs, while DuckDB-WASM initializes in the background to handle heavy multi-schedule analytical comparisons, multi-year CAGRs, and custom SQL exports directly in the user's browser memory. 

## The "Two-Tier" Boundary Calibration Engine

Comparing a single-tier city (like Toronto) against a lower-tier municipality (like Mississauga) on raw line items yields an inaccurate comparison because regional upper-tier spending (like Peel Region police or paramedics) is omitted. Naively adding them causes regional double-counting. 

To solve this, TaxWatchdog utilizes a proprietary boundary calibration engine that apportions upper-tier regional levies across constituent municipalities using statutory Current Value Assessment (CVA) ratios, producing accurate, consolidated per-household figures across the "Big 6" property tax drivers.

## Repository Contents

- **[Data Methodology & Glossary](GLOSSARY.md):** Detailed documentation on how raw Ontario FIR datasets are standardized, defining complex civic accounting concepts (like the PSAB-3150 shift, Amortization, and the Annual Repayment Limit).
- **Database Schema:** Structure of the DuckDB-optimized tables used for municipal comparisons.
- **Issue Tracker:** The public board for reporting data anomalies, UI bugs, or edge cases in the Move Simulator. 
- **Processing Utilities:** *[Coming Soon]* Open-source Python/Node utilities used for sanitizing specific FIR schedules.

## Bug Reports & Feature Requests

If you find a data anomaly, a bug in the Move Simulator's rollover equity logic, or experience a WASM out-of-memory error on a specific device, please **[open an issue](https://github.com/sentientcoders/Tax-Watchdog/issues)** in this repository.

## About Sentient Coders 

TaxWatchdog is a project developed and maintained by **[Sentient Coders Inc.](https://github.com/sentientcoders)**, dedicated to building zero-telemetry, highly efficient software and transparent public data platforms.
