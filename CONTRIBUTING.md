# Contributing to the Canvas AI Assistant

We're excited to have you contribute! To ensure a smooth workflow, please follow these guidelines.

## Branching Strategy

1. **`main` Branch**: This branch is for stable, reviewed code only. Direct pushes to `main` are disabled.
2. **Feature Branches**: All new work must be done on a feature branch.
   * Name your branch clearly, e.g., `feat/llm-integration`, `fix/database-connection`, `docs/update-readme`.
   * Create your branch from the most up-to-date version of `main`.
   ```bash
   git checkout main
   git pull
   git checkout -b feat/your-feature-name
   ```

## Pull Request (PR) Process

1. Once your feature is complete, push your branch to GitHub.
2. Open a Pull Request to merge your feature branch into `main`.
3. In your PR description, clearly explain the changes you made.
4. Assign at least one other team member to review your code.
5. The reviewer will check for code quality, bugs, and adherence to the project goals. Once approved, the PR can be merged into `main`.

## Coding Style

Please follow the [PEP 8 style guide](https://www.python.org/dev/peps/pep-0008/) for all Python code.

## Development Workflow

### Setting Up Your Development Environment

1. Clone the repository and create a virtual environment:
   ```bash
   git clone https://github.com/your-username/canvas-ai-assistant.git
   cd canvas-ai-assistant
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Running Tests

Before submitting a PR, make sure to:
- Test your changes locally
- Run the Flask server to ensure it starts without errors
- Test API endpoints using Postman or curl

### Commit Message Format

Use clear, descriptive commit messages:
- `feat: add Canvas API integration`
- `fix: resolve database connection issue`
- `docs: update README with setup instructions`

## Team Communication

- Use GitHub Issues to track bugs and feature requests
- Use GitHub Discussions for questions and general discussion
- Tag team members in PRs for review using `@username`

## Code Review Checklist

When reviewing code, check for:
- [ ] Code follows PEP 8 style guidelines
- [ ] Functions and classes have appropriate docstrings
- [ ] Error handling is implemented where needed
- [ ] No sensitive information (API keys, passwords) is committed
- [ ] Code is well-tested and functional