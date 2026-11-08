# TaxWatchdog — Data Processing & Architecture

[![Website](https://img.shields.io/badge/Website-taxwatchdog.ca-blue)](https://taxwatchdog.ca)

**TaxWatchdog** is an open-data web platform designed to provide transparent, long-term municipal financial intelligence for Ontario taxpayers. This repository contains the public documentation and data aggregation methodology utilized by the platform.

Visit the live platform at **[taxwatchdog.ca](https://taxwatchdog.ca)**.

## Overview

The platform processes and aggregates 25 years of Ontario Financial Information Return (FIR) datasets. To ensure high performance and instantaneous querying on the client side, the raw municipal financial data is pre-computed and mathematically aggregated into a highly optimized 106.4 MB seed file.

## Technical Architecture

TaxWatchdog is built with a modern, serverless edge architecture prioritizing speed and local data processing:

* **Frontend:** React and Vite
* **In-Browser Data Engine:** DuckDB-WASM (for client-side analytical SQL processing)
* **Database & Hosting:** Cloudflare D1 and Cloudflare Pages

## Repository Contents

* **Data Methodology:** Documentation on how raw Ontario FIR datasets are standardized, cleaned, and compiled into the core seed file.
* **Database Schema:** Structure of the DuckDB-optimized tables used for municipal comparisons.
* **Processing Utilities:** Future open-source scripts used for aggregating the financial metrics.

## About Sentient Coders 

TaxWatchdog is a project developed and maintained by **Sentient Coders Inc.**, dedicated to building zero-telemetry, highly efficient software and transparent public data platforms.
