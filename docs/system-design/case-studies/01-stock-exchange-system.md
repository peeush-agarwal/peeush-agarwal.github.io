# How a Stock Exchange Works: A Deep Dive into System Design

The stock market moves trillions of dollars every day — but have you ever wondered what happens *under the hood* when you hit "Buy"? In this post, we'll break down the architecture of a modern stock exchange, from the moment you place an order to the moment a trade is executed.

---

## The Farmer's Market Analogy

Before diving into architecture, let's ground ourselves with a simple mental model.

Think of a stock exchange as a **farmer's market**:
- Each stock is a stall where buyers and sellers gather.
- Sellers set a price; if no one buys, they lower it.
- Buyers want the cheapest price and queue up by willingness to pay.
- A **trade happens** when a buyer's price meets or exceeds a seller's price.

In technical terms:
- **BUY orders** → sorted in *decreasing* order (highest bid first)
- **SELL orders** → sorted in *increasing* order (lowest ask first)
- The **overlap point** = the market price

---

## Core Requirements

A well-designed exchange must support:

- Placing **BUY / SELL** orders
- **Cancelling** orders at any time
- **Real-time matching** of buyers and sellers
- **Per-user trading limits** (shares per day)
- **Real-time market data** publishing

In real exchanges, message distribution looks roughly like this:

| Message Type | Approximate Share |
|---|---|
| New Orders | ~50% |
| Cancellations | ~40% |
| Executions | ~2% |
| Other (noise) | ~8% |

---

## Key Trading Concepts

Before jumping into architecture, here are a few terms worth knowing:

- **Broker** — An app or platform (e.g. Robinhood, Charles Schwab) that lets users place orders on an exchange.
- **Order Book** — A real-time list of all open BUY and SELL orders for a given stock.
- **Market Order** — Executes immediately at the current market price; gets priority in the order book.
- **Limit Order** — Executes only at your specified price or better.
- **Spread** — The gap between the highest BUY price and the lowest SELL price.
- **Liquidity** — How easily a stock can be bought/sold without moving its price.

---

## The Three Pillars of Exchange Architecture

A stock exchange is built on an **asynchronous, event-sourced** architecture. Three components form its backbone:

### 1. 🏦 Broker

The broker is the **user-facing layer**. It:
- Sends order requests to the exchange
- Receives real-time market data back

Users connect to brokers via **REST APIs and WebSockets**. Brokers communicate with the exchange using the **FIX (Financial Information Exchange) protocol** — a bidirectional, secure messaging standard that:
- Assigns unique **sequence numbers** to every message
- Uses **checksums and message length** to verify data integrity

### 2. 🚪 Gateway

The gateway is the **entry point** for all broker communication. It has three critical sub-components:

| Component | Role |
|---|---|
| **Risk Manager** | Validates funds, blocks suspicious activity, calculates fees |
| **Wallet** | Stores user funds and assets |
| **Order Manager** | Assigns sequence numbers, manages order state, routes to matching engine |

The **Order Manager** is especially important — it acts as a lightweight ledger of *all* orders (open, cancelled, rejected). It assigns a **globally increasing sequence number** to every event, which guarantees:

- ✅ Ordering fairness
- ✅ Fast recovery and deterministic replay
- ✅ Exactly-once delivery guarantee

Each message type (new order, cancel, execution) gets its own **topic queue with independent sequence numbers** — enabling parallel processing and easier recovery.

### 3. ⚙️ Matching Engine

This is the **heart of the exchange**. It:
- Verifies sequence numbers
- Matches BUY and SELL orders
- Generates market data from trades

It contains two key parts:

#### Order Book
An **in-memory data structure** that maintains open orders per stock symbol. For each stock, there are two sorted lists:
- One for BUY orders
- One for SELL orders

Each price level uses a **doubly linked list** (FIFO queue):
- New orders appended at the tail → **O(1)**
- Cancellations via pointer lookup → **O(1)**
- An **index maps order IDs to order objects** in memory for O(1) lookups

#### Matching Logic
A match occurs when:

```
buy_price ≥ sell_price
```

The matching function must be **fast, accurate, and deterministic** — the same input sequence must always produce the same output sequence.

---

## End-to-End Workflows

### 📥 Placing a BUY/SELL Order

```
User → Broker → Gateway (auth + rate limit)
     → Order Manager (risk checks + wallet freeze)
     → Matching Engine (order book update)
     → Trade Execution → Market Data Broadcast
     → Payment Settlement
```

A matched order produces **two execution fills** — one for the buyer, one for the seller. An order can be:
- **Fully filled** ✅
- **Partially filled** — remaining quantity re-enters the order book
- **Unmatched** — sits in the order book until a counterparty appears

### ❌ Cancelling an Order

```
User → Gateway → Order Manager (index lookup, O(1))
     → Amount set to 0 / removed from list
     → Matching Engine updates order book
     → Market data broadcast + wallet balance restored
```

### 📊 Market Data Flow

After each trade execution:
1. Matching engine groups matched order info into a **tick** (price, quantity, client ID, fill info)
2. Data is broadcast to brokers and clients via the gateway using **multicast** (one message → many receivers)
3. A **real-time analytics database** stores data for dashboards and trend analysis
4. Trade records are written to a database for **auditing and tax reporting**

> ⚡ Market data flow runs *outside* the critical trading path to preserve performance.

---

## Performance & Scalability Considerations

Modern exchanges are engineered for **microsecond-level latency**. Here's how:

- **Minimize network hops** — keep only essential services in the critical path
- **In-memory databases** — for the order book and active order state
- **Co-location** — place gateway servers physically near exchange servers
- **Time-series databases** — for incoming orders and historical data
- **CDN/cache** — for historical time-series data and static assets
- **Dedicated databases** per entity type — deposits, trades, swaps, etc.
- **On-premise servers** — many exchanges avoid cloud for fine-grained control and predictable latency

---

## Architecture at a Glance

```
[User]
  ↓ REST / WebSocket
[Broker]
  ↓ FIX Protocol
[Gateway]
  ├── Risk Manager
  ├── Wallet
  └── Order Manager (sequence numbers)
        ↓
[Matching Engine]
  ├── Order Book (in-memory, per symbol)
  └── Matching Logic (deterministic)
        ↓
[Market Data] → broadcast via multicast
[Payment Service] → fund settlement
```

---

## Final Thoughts

A stock exchange is one of the most **performance-critical distributed systems** ever built. Every design decision — from doubly linked lists in the order book to FIX protocol sequence numbers — exists to ensure **fairness, speed, and reliability** at massive scale.

Whether you're preparing for a system design interview or just curious about the infrastructure powering global markets, understanding these patterns gives you a powerful mental model for designing *any* high-throughput, low-latency system.

> 🧠 **Key Takeaway:** The same principles behind stock exchange design — event sourcing, sequence guarantees, in-memory state, and deterministic processing — apply broadly to trading platforms, gaming servers, auction systems, and beyond.
