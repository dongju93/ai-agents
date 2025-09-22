# Company Overview

**Company Name:** TrueNorth ITG  
**Headquarters:** Boston, MA (Hybrid—onsite 2–3 days/week)  
**Size:** ~51–200 employees (LinkedIn)  
**Industry:** IT consulting & professional services, digital transformation, custom software development  
**Founded:** 2016  
**Core Services:**

- Custom application development (Web & mobile)
- Cloud architecture & migration (AWS, Azure)
- Data engineering & analytics
- DevOps & infrastructure automation

# Mission and Values

**Mission:** To guide organizations “true north” through digital transformation—building scalable, secure solutions that solve business problems and adapt as needs evolve.  
**Values:**

- **Client Success:** We put your goals first—measuring our work by your outcomes.
- **Innovation:** We embrace new tools, frameworks, and methodologies to stay ahead of the technology curve.
- **Collaboration:** Cross-functional teamwork drives better solutions. We’re agile, transparent, and communicative.
- **Integrity:** We hold ourselves to high ethics in both code and client relationships.

# Recent News or Changes

- **AWS Partnership Expanded (Q1 2024):** TrueNorth ITG achieved AWS Advanced Consulting Partner status, unlocking deeper access to serverless, analytics, and ML capabilities.
- **Launch of AI-Driven Insights Platform (Feb 2024):** Internal pilot for predictive logistics analytics; early client feedback highlights 20% efficiency gains.
- **2023 Headcount Growth:** 30% increase in engineering staff to support multi-industry client pipeline (financial services, healthcare, manufacturing).
- **ISO 27001 Certification (Dec 2023):** Reinforces company commitment to security & compliance for regulated-industry clients.

# Role Context and Product Involvement

As a **Mid-Level Python Software Engineer**, you will join a 4–6-person backend pod within the larger Engineering practice. This team partners closely with frontend engineers, UX designers, and DevOps to build and maintain TrueNorth’s in-house SaaS platform—a microservices-based analytics/dashboard application built on:

- **Backend:** Python (Django for core admin panels; FastAPI for public REST/GraphQL endpoints)
- **Data Layer:** PostgreSQL (primary OLTP), Redis (caching, Pub/Sub for events)
- **Deployment:** Docker, AWS Lambda (event-driven tasks), AWS ECS (service orchestration), AWS S3 (static/media storage)
- **Dev Practices:**
  - TDD/BDD with pytest & factory-boy
  - Git-based code reviews (GitHub)
  - Agile ceremonies: sprint planning, daily standups, retrospectives
  - CI/CD pipelines (GitHub Actions → ECS deploy)

# Likely Interview Topics

**1. Python & Framework Expertise**

- Differences between Django and FastAPI; when to choose one vs. the other
- Pydantic models, request validation, serialization
- Async I/O in Python (async/await, event loops)

**2. API Design & Data Modeling**

- RESTful conventions vs. GraphQL trade-offs
- Database schema design, indexing strategies, normalization vs. denormalization
- Caching patterns with Redis (cache-aside, message queues)

**3. Cloud & DevOps**

- Containerization with Docker: multi-stage builds, image optimization
- AWS ECS vs. Lambda for microservices; use cases and cost/performance considerations
- S3 lifecycle policies, IAM roles & security best practices

**4. Testing & Quality**

- Unit vs. integration testing strategies; mocking external services
- CI/CD workflows: test coverage gates, linting (Flake8/Ruff), type checking (MyPy/Pyright)

**5. System Design & Scalability**

- Designing fault-tolerant services; retry/backoff strategies
- Data partitioning/sharding in PostgreSQL
- Observability: logging, metrics (Prometheus/Grafana), distributed tracing

**6. Behavioral & Culture Fit**

- Examples of agile teamwork: handling conflicting priorities, remote collaboration
- Times you’ve mentored/junior-engineered peers or led code reviews
- Approach to adopting new tech or refactoring legacy code

# Suggested Questions to Ask

1. **Team & Process**

   - “Can you describe the structure of the engineering pod I’d be joining? How do you balance feature delivery vs. technical debt?”
   - “What does a typical sprint look like, and how does the team track progress and blockers?”

2. **Product Roadmap & Success Metrics**

   - “What are the next major features or integrations planned for the SaaS platform this year?”
   - “How does the team measure success—performance SLAs, user engagement, business KPIs?”

3. **Tech Stack Decisions**

   - “What drove the choice of FastAPI for certain services, and how do you manage consistency across Django and FastAPI codebases?”
   - “Are there any plans to introduce new technologies (e.g., Kubernetes, serverless frameworks) in the near term?”

4. **Growth & Development**

   - “What learning resources or trainings does TrueNorth ITG offer to support continuous skill development?”
   - “How do career paths look for mid-level engineers—what growth opportunities are available?”

5. **Culture & Remote/Hybrid Work**

   - “How does the team stay connected and maintain culture in a hybrid environment?”
   - “What flexibility exists around on-site vs. remote work, especially for candidates relocating?”

6. **Onboarding & First 90 Days**
   - “What does the onboarding process look like, and what are the key milestones for a new hire’s first three months?”
