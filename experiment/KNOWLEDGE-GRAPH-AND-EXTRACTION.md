# FamCloud — Entity Extraction, Knowledge Graph & Agent Integration

## The Architecture Question

Charles wants to know: can we build entity extraction + knowledge graph per family, and integrate it as a native OpenClaw skill/tool?

**Short answer: Yes, absolutely. And it's the right architectural approach.**

---

## Component 1: Entity Extraction from User Queries

### What We're Extracting
From every message the family sends, we pull:
- **People** — "Mom", "Sarah", "Jake", "Grandma Linda"
- **Relationships** — "Sarah is Jake's sister", "Linda is Mom's mom"  
- **Events** — "Soccer practice Tuesday at 4", "Dentist appointment Wednesday 10am"
- **Locations** — "School", "Dr. Smith's office", "Home"
- **Preferences** — "Jake hates vegetables", "Mom prefers morning meetings"
- **Decisions** — "We're going to Disney in March"
- **Patterns** — "Family asks about calendar 40% of queries"
- **Facts** — "Sarah is 8 years old", "Jake's birthday is June 15"

### How It Works
Three approaches, from simple to advanced:

**Approach A: LLM-Based Extraction (Easiest, Start Here)**
- After every message, run a small extraction prompt alongside the main query
- Example prompt: "From this family conversation, extract: people, events, relationships, preferences, facts. Output as JSON."
- Run on the same model (Qwen 14B) — adds ~0.5-1s overhead per message
- Store extracted entities in the knowledge graph
- **Feasibility: HIGH. Can build in 1-2 weeks.**

**Approach B: Structured NER Pipeline (More Efficient)**
- Use spaCy or a dedicated NER model for named entity recognition
- Faster than LLM extraction (~100ms vs ~1s)
- Less flexible — needs custom training for family-specific entities
- **Feasibility: MEDIUM. Good to add later for performance.**

**Approach C: Hybrid (LLM + Rules)**
- LLM extracts complex entities (relationships, preferences, decisions)
- Rules extract simple entities (dates, times, locations, phone numbers)
- Best of both: flexibility + speed
- **Feasibility: HIGH. Recommended eventual state.**

### Technical Implementation
```python
# Pseudocode for the extraction pipeline
def extract_entities(conversation_message):
    """Extract structured knowledge from a family conversation."""
    
    # LLM-based extraction (main path)
    prompt = f"""
    Extract entities from this family conversation.
    Return as JSON: {{
        "people": ["names mentioned"],
        "events": [{"name": "soccer", "day": "tuesday", "time": "4pm", "person": "Sarah"}],
        "relationships": [{"person1": "Sarah", "person2": "Jake", "relation": "sister"}],
        "preferences": [{"person": "Jake", "pref": "hates vegetables"}],
        "facts": [{"person": "Sarah", "fact": "is 8 years old"}],
        "locations": ["school", "dr smith office"]
    }}
    
    Conversation: {conversation_message}
    """
    
    result = ollama.chat("qwen2.5:14b", prompt)
    return parse_json(result)

# Run alongside every query (async, non-blocking)
async def process_family_query(message, family_id):
    user_response = agent.generate_response(message)
    knowledge = extract_entities(message)  # runs in parallel
    knowledge_graph.upsert(family_id, knowledge)
    return user_response
```

### Overhead
- LLM extraction: +0.5-1s per message (acceptable for async/background)
- Can run after the user gets their response (non-blocking)
- Storage: ~100-500KB per family per day (negligible)

---

## Component 2: Knowledge Graph Storage & Query

### What We Need to Store
A graph of entities with relationships:
```
Family: Johnson
├── Members
│   ├── Mom (Sarah, 42)
│   ├── Dad (Mike, 45)
│   ├── Sarah (8) ── sister_of ── Jake
│   ├── Jake (5) ── brother_of ── Sarah
│   └── Grandma Linda (68) ── mother_of ── Mom
├── Events
│   ├── Soccer (Tue 4pm, Sarah)
│   ├── Dentist (Wed 10am, Jake)
│   └── Movie Night (Fri 7pm, Family)
├── Preferences
│   ├── Mom: "hates early meetings"
│   ├── Jake: "loves dinosaurs"
│   └── Dad: "works remotely Tue/Thu"
└── Patterns
    ├── Calendar queries: 40% of all queries
    ├── Homework help: 30%
    └── General chat: 20%
```

### Storage Options
**Option A: Local SQLite + JSON (Easiest, Start Here)**
- Every family rig has a local SQLite database
- Tables: `people`, `events`, `relationships`, `preferences`, `facts`, `locations`
- Store as structured JSON in SQLite JSON columns
- Query with standard SQL
- Backup: JSON file or SQLite dump
- **Feasibility: HIGH. Can build in 1 week. Zero dependencies beyond what's already installed.**

**Option B: NetworkX Graph (Python-native, Flexible)**
- Use NetworkX library (Python) to store as actual graph
- Supports graph queries (shortest path, centrality, etc.)
- Serialize to JSON/GraphML for storage
- **Feasibility: HIGH. Good for complex relationship queries.**

**Option C: Neo4j / Graph DB (Enterprise, Overkill for Now)**
- Full graph database with Cypher query language
- Runs as a Docker container alongside the agent
- Overkill for one family's data
- **Feasibility: MEDIUM. Save for when you have multiple families on one rig.**

### Recommended: SQLite + NetworkX Hybrid
- SQLite for structured storage (events, preferences, facts)
- NetworkX for relationship graph (people → relationships → people)
- Both run locally on the rig, lightweight, zero cloud dependency
- **Total storage: ~1-5MB per family** (fits easily on 500GB NVMe)

### Query Examples
```python
# Query 1: "When is Sarah's soccer game this week?"
def find_event(person, event_type, timeframe="this_week"):
    """Query the knowledge graph for events."""
    return db.query(f"""
        SELECT * FROM events 
        WHERE person = '{person}' 
        AND type = '{event_type}'
        AND date BETWEEN {start_of_week()} AND {end_of_week()}
    """)

# Query 2: "Who in the family has appointments this week?"
def find_family_events(timeframe="this_week"):
    """Get all family events for this week."""
    events = db.query(f"""
        SELECT events.*, people.name, people.relationship_to_family
        FROM events
        JOIN people ON events.person_id = people.id
        WHERE events.date BETWEEN {start_of_week()} AND {end_of_week()}
        ORDER BY events.date ASC
    """)
    return events

# Query 3: "What does Jake like?"
def get_preferences(person):
    """Get all preferences for a person."""
    return db.query(f"""
        SELECT preference, confidence, source 
        FROM preferences 
        WHERE person = '{person}'
        ORDER BY confidence DESC
    """)

# Query 4: "Is Sarah related to Jake?"
def find_relationship(person1, person2):
    """Find the relationship between two people."""
    return networkx_graph.has_edge(person1, person2)
```

---

## Component 3: Integration as an OpenClaw Skill/Tool

### How OpenClaw Integration Works
OpenClaw skills are defined in `SKILL.md` files. Tools are callable functions the agent can invoke at runtime.

**What we'd build:** A skill called `family-knowledge-graph` with these tools:

```yaml
# SKILL.md
name: family-knowledge-graph
description: Query and update the family knowledge graph with structured information about family members, events, preferences, and relationships.

tools:
  - name: query_events
    description: Find events for a person or the whole family
    parameters: { person: string, event_type: string, timeframe: string }
  
  - name: query_people
    description: Get information about a family member
    parameters: { person: string }
  
  - name: query_relationships
    description: Find relationships between family members
    parameters: { person1: string, person2: string }
  
  - name: query_preferences
    description: Get preferences for a person
    parameters: { person: string }
  
  - name: add_entity
    description: Add a new entity to the knowledge graph
    parameters: { type: string, person: string, data: object }
  
  - name: update_entity
    description: Update an existing entity
    parameters: { entity_id: string, data: object }
  
  - name: weekly_summary
    description: Generate a weekly family summary
    parameters: { family_id: string }
```

### How the Agent Uses It
```
User: "What's Sarah's schedule this week?"

Agent thinking:
1. This is a query about events for "Sarah" in "this week"
2. I should use the `family-knowledge-graph` tool
3. Call: query_events(person="Sarah", timeframe="this_week")
4. The tool returns: [{event: "soccer", day: "Tuesday", time: "4pm", location: "field"}]
5. I respond: "Sarah has soccer practice on Tuesday at 4pm at the field."
```

### Integration with OpenClaw
1. **Create the skill** — `~/.openclaw/skills/family-knowledge-graph/SKILL.md`
2. **Implement the tools** — Python scripts or shell scripts that query SQLite/NetworkX
3. **Register with OpenClaw** — Add to OpenClaw's skills directory, gateway picks it up
4. **Agent auto-discovery** — OpenClaw's agent picks up the skill automatically (it reads SKILL.md)
5. **Tool calling** — When the user asks a question, the agent sees the tool is available and uses it

### Technical Path
1. **Week 1-2:** Build the extraction pipeline (LLM-based + SQLite storage)
2. **Week 3:** Build the knowledge graph tools (query_events, query_people, etc.)
3. **Week 4:** Create the OpenClaw skill (SKILL.md + tool implementations)
4. **Week 5-6:** Test end-to-end — family queries → entity extraction → knowledge graph → agent response
5. **Week 7-8:** Refine extraction quality, handle edge cases, add NetworkX for relationships

---

## Feasibility Assessment

### Overall: HIGHLY FEASIBLE

| Component | Difficulty | Timeline | Dependencies |
|-----------|-----------|----------|--------------|
| Entity Extraction (LLM-based) | Easy | 1-2 weeks | Ollama + Qwen (already available) |
| SQLite Storage | Easy | 3-5 days | Built into Python |
| NetworkX Graph | Easy-Medium | 1 week | pip install networkx |
| OpenClaw Skill + Tools | Medium | 1-2 weeks | OpenClaw skill system (well-documented) |
| End-to-End Integration | Medium | 2-3 weeks | All components working together |
| Total | | 6-10 weeks | |

### What Makes This Feasible:
- ✅ All components run locally (no cloud, no API costs)
- ✅ SQLite is built into Python — zero setup
- ✅ NetworkX is a standard library — pip install
- ✅ OpenClaw has a documented skill system
- ✅ LLM extraction uses the same model already running (Qwen 14B)
- ✅ Storage is negligible (1-5MB per family)
- ✅ Processing is asynchronous (doesn't slow down user response)
- ✅ No external dependencies

### What Could Be Hard:
- ⚠️ Extraction quality: LLM may miss entities or extract wrong relationships
  - **Mitigation: Add confidence scores, human-in-the-loop review initially**
- ⚠️ Ambiguity: "She" could be Mom or Sarah — entity resolution is tricky
  - **Mitigation: Use context from conversation history to disambiguate**
- ⚠️ Storage growth: If extraction runs every message, storage grows fast
  - **Mitigation: Deduplicate, compress, only store high-confidence extractions**
- ⚠️ Query performance: As knowledge graph grows, queries slow down
  - **Mitigation: Indexes on SQLite, limit graph depth, cache frequent queries**

### Recommended Development Order:
1. **First:** Extraction pipeline (LLM + SQLite) — prove you can extract entities from conversations
2. **Second:** Knowledge graph tools (query_events, query_people, query_preferences) — prove you can query the stored data
3. **Third:** OpenClaw skill + integration — prove the agent can use the tools naturally
4. **Fourth:** NetworkX for relationships — add graph-specific queries
5. **Fifth:** Refinement — confidence scores, deduplication, edge cases, error handling

---

## The Premium Tier Differentiator: LoRA Adapters + Knowledge Graph

The knowledge graph + entity extraction is the CORE product (Pro tier).

The **PREMIUM** differentiator is:
- **LoRA adapters per family** (model fine-tuned on their data)
- **Advanced analytics** ("what did my kids ask about this week?")
- **Nightly model updates** (distilled model + adapter retrained)
- **Custom agent personality** (agent develops unique voice for this family)

The knowledge graph feeds into the LoRA training:
1. Extract entities from conversations → knowledge graph
2. Use knowledge graph as structured training data → train LoRA adapter
3. LoRA adapter + base model = personalized model for this family
4. Nightly: re-train adapter from new conversations → model gets better every week

This is the **PREMIUM tier killer feature** that justifies $75/month.

---

## Bottom Line

Building the entity extraction + knowledge graph + OpenClaw integration is:
- **Highly feasible** — all tools exist, local-only, no cloud dependencies
- **6-10 weeks** of focused development
- **SQLite + NetworkX + LLM extraction** — standard, well-documented tech
- **Integrates natively** with OpenClaw via the skill system
- **The core moat** — nobody else has this because nobody else is building local-first, privacy-preserving family knowledge graphs

The hardest part isn't the technology — it's getting extraction quality high enough that the knowledge graph is actually useful, not just noisy.
