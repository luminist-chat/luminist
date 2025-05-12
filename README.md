# Luminist ✨
Luminist is a conversational AI assistant for deep document understanding and semantic exploration.

Try it out at [luminist.chat](https://luminist.chat/)

[Join my Discord!](https://discord.gg/PYKTaJ5Ett)

## Why Luminist?

Modern AI chat solutions are all severely lacking the ability to reason deeply through documents within domains that are highly ontologically complex.  Many of these solutions just rely on a simple similarity search for their RAG, which is often insufficient to provide a holistic understanding of a topic to answer a user's question.

The addition of a dynamically generated knowledge graph is key in order to gain an understanding of how concepts interconnect together, in order to gain deeper, ontology-driven insights.

## Quickstart

Clone the repo and run locally in a few steps:

```
git clone https://github.com/luminist-chat/luminist
cd luminist
poetry install
docker compose up
```

Visit [`http://localhost:8000`](http://localhost:8000) to use the locally running instance!

*(Full setup and usage instructions coming soon!)*

## Project Structure

```
luminist/
├── api/              # FastAPI backend service
├── frontend/         # React frontend (TypeScript, Tailwind)
├── scripts/          # Document processing and ingestion scripts
├── utils/            # Common utilities
├── tests/            # Test suites and evaluation scripts
└── docker-compose.yml
```

## Contributing

Luminist is an open project, and your contributions are warmly welcomed!

* **Report Issues:** Found a bug or have ideas? Open a GitHub issue!
* **Pull Requests:** Improvements, features, or fixes—send a PR.
* **Comments/Discussion:** [Join my Discord!](https://discord.gg/PYKTaJ5Ett)

## Roadmap

Here's what's coming next:

* [ ] Improved semantic chunking
* [ ] User authentication and sharing capabilities
* [ ] Payment integration (Stripe)
* [ ] Expanded ontology and knowledge graph capabilities
* [ ] More robust entity recognition (custom NER training?)

## License

MIT License. Use freely, build cool stuff!
