🌍 MCP-Based Weather AI Application

A hands-on project demonstrating Model Context Protocol (MCP) by building a fault-tolerant Weather AI system using FastAPI, Streamlit, and external weather providers.

This project shows how AI systems should safely interact with tools (APIs) using a clean, production-ready architecture.

📌 What This Project Does

Fetches current weather for any city

Fetches 7-day weather forecast

Uses an MCP Server to isolate tool access

Provides a Streamlit web UI

Handles API failures gracefully

Demonstrates agent-ready architecture

🧠 What is MCP (Model Context Protocol)?

MCP is a design pattern where:

AI or client applications do not directly call external APIs.
Instead, they interact with a dedicated tool server (MCP server).

This makes systems:

Safer

Easier to maintain

Replaceable

AI-agent friendly
