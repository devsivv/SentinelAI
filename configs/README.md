# Configuration

## Purpose

Contains all environment-independent configuration for SentinelAI.

## Files

- development.yaml
- production.yaml
- agents.yaml
- datasets.yaml
- models.yaml

## Rules

Application code must never hardcode:

- Database credentials
- API ports
- Model paths
- Dataset paths
- Logging directories

Sensitive values belong in `.env`.

## Sprint Status

Initialized in Sprint 0.