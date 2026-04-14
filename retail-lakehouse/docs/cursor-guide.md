# Cursor Guide

How to use Cursor IDE as your learning companion for this course.

## What Is Cursor-Guided Learning?

This repository includes a course specification (`databricks-course.md`) and an adaptive learning tracker (`notes.md`). When you open the repo in Cursor, the AI assistant uses these files to:

- Give you one task at a time, with clear requirements and success criteria
- Review your solutions like a senior engineer
- Adapt difficulty based on your progress and mistakes
- Avoid dumping full solutions unless you explicitly ask

This is not a chatbot Q&A. It's structured mentorship powered by a detailed teaching spec.

## Files That Drive the Cursor Experience

| File | Role | Do you edit it? |
|---|---|---|
| `databricks-course.md` | Course specification: phases, task format, teaching philosophy, interaction rules | No — this is for the AI |
| `notes.md` | Your learning tracker: strengths, mistakes, concepts learned | Yes — keep it updated |
| `project-setup.md` | Repo generation spec (how the skeleton was built) | No |
| `README-for-cursor-usage.md` | Internal doc explaining how Cursor uses the repo | No |
| `.cursor/rules/databricks-course.mdc` | Cursor workspace rules | No |

If you're not using Cursor, you can ignore all of these files.

## Getting Started

1. Open the `retail-lakehouse/` folder in Cursor
2. Make sure the workspace rules in `.cursor/rules/` are active (Cursor loads these automatically)
3. Start a chat and say:

```
Start the course
```

Cursor will orient you, explain the current phase, and give you Task 1.

## Recommended Prompts

### Starting and progressing

| You say | What happens |
|---|---|
| `Start the course` | Cursor begins Phase 1 with Task 1 |
| `Give me the next task` | Cursor gives exactly one task — no more |
| `What phase am I in?` | Cursor checks your progress and tells you |

### Getting help

| You say | What happens |
|---|---|
| `I'm stuck` | Cursor gives escalating hints: conceptual → implementation → partial code |
| `Explain this concept` | Cursor explains in the context of the current project, not abstractly |
| `Show solution` | Cursor shows the full solution for the current task only |

### Getting reviewed

| You say | What happens |
|---|---|
| `Review my solution` | Cursor reviews like a senior engineer: what's good, what's wrong, what to improve, whether to move on |

### Exploring

| You say | What happens |
|---|---|
| `What TODOs are left?` | Cursor scans the repo and lists remaining work |
| `Explain how config works in this project` | Cursor walks through `config.py` and `conf/` in context |

## Working Agreement with Cursor

To get the most out of Cursor-guided learning, follow these principles:

### 1. Try before you ask

Attempt the TODO yourself before asking Cursor for help. If you jump to "Show solution" immediately, you'll learn the syntax but not the thinking.

### 2. Ask for review, not validation

Don't ask "Is this right?" — ask "Review my solution." Cursor will point out things you might miss: edge cases, style issues, whether the code belongs in the right place.

### 3. One task at a time

The course is designed for incremental progress. Don't ask for all remaining tasks at once. Each task builds understanding that the next task assumes.

### 4. Keep notes.md honest

After each session, add a short note about what you learned, struggled with, or got wrong. Cursor reads `notes.md` to calibrate difficulty.

Good entries:
- `Struggled with: left join producing duplicate columns`
- `Learned: dropDuplicates needs a column list to dedup on a key`
- `Mistake: forgot to cast types before computing total_amount`

Bad entries:
- `Did some stuff today` (too vague)
- Long paragraphs (keep it to one line per entry)

### 5. Don't over-rely on Cursor for basic Python

Cursor is best at teaching Databricks and PySpark concepts in context. For basic Python syntax, use standard references.

## How the Course Adapts

Cursor reads `notes.md` before each task to understand:
- What concepts you've already learned
- What you've struggled with
- What mistakes keep recurring

This means:
- If you keep getting joins wrong, Cursor will give more guidance on the next join task
- If you're breezing through, Cursor will offer stretch goals
- If you skip phases, Cursor will notice gaps and fill them

The more honest your `notes.md`, the better the adaptation.

## When to Stop Using Cursor

You don't need Cursor forever. A good sign you're ready to work independently:

- You can implement a silver or gold transformation without hints
- You can write a quality check from scratch
- You can read a PySpark chain and explain what each step does
- You can tell where code should live (notebook vs. package vs. test)

At that point, use Cursor for code review and exploration rather than guided tasks.
