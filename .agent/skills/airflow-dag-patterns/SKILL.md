---
name: airflow-dag-patterns
description: kurumsal apache airflow dag mimarisi, veri boru hatlari, operatorler ve hata yonetimi.
when_to_use: "zamanlanmis etl, veri akislari ve analitik is akislari tasarlanirken kullanilir."
allowed-tools: Read, Write, Edit, Grep
version: 1.0.0
---

# airflow-dag-patterns — kurumsal bulut, devops ve gozlemlenebilirlik standardi

> 46 p0 kuralina ve sifir kesinti ilkesine bagli kurumsal operasyon kalibi.

# Apache Airflow DAG Patterns

Production-ready patterns for Apache Airflow including DAG design, operators, sensors, testing, and deployment strategies.

## Use this skill when

- Creating data pipeline orchestration with Airflow
- Designing DAG structures and dependencies
- Implementing custom operators and sensors
- Testing Airflow DAGs locally
- Setting up Airflow in production
- Debugging failed DAG runs

## Do not use this skill when

- You only need a simple cron job or shell script
- Airflow is not part of the tooling stack
- The task is unrelated to workflow orchestration

## Instructions

1. Identify data sources, schedules, and dependencies.
2. Design idempotent tasks with clear ownership and retries.
3. Implement DAGs with observability and alerting hooks.
4. Validate in staging and document operational runbooks.

Refer to `resources/implementation-playbook.md` for detailed patterns, checklists, and templates.

## Safety

- Avoid changing production DAG schedules without approval.
- Test backfills and retries carefully to prevent data duplication.

## Resources

- `resources/implementation-playbook.md` for detailed patterns, checklists, and templates.
