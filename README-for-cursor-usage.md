# How To Use This Repository With Cursor

## Purpose

This file explains how Cursor should be used with this repository.

The repository contains:
- a project setup specification
- a course specification
- a notes file for adaptive learning

## Files

### `project-setup.md`
Defines the repository shape and generation rules.

### `databricks-course.md`
Defines how the tutorial should be taught.

### `notes.md`
Tracks learning progress, weak spots, and recurring mistakes.

## Expected Workflow

### Step 1 — Generate the repository
Use `project-setup.md` to scaffold the realistic Databricks project.

### Step 2 — Review the generated structure
Check whether the repository shape is clear, realistic, and teachable.

### Step 3 — Populate the files
Fill the repository with partial implementations, docs, tests, sample data, and notebooks.

### Step 4 — Start the course
Use `databricks-course.md` to begin teaching inside the generated repository.

### Step 5 — Adapt over time
Use `notes.md` before giving future tasks so the course adapts to weak spots and progress.

## Rules For Cursor

When generating code or files:
- keep it realistic
- keep it understandable
- avoid hiding Spark logic
- avoid over-engineering
- leave meaningful TODOs for the student

When teaching:
- give one task at a time
- use actual repo files
- review solutions like a senior engineer
- adapt to `notes.md`