# Hosting Options for ClinPharm Vault

## Recommendation

Use this stack:
- **Obsidian** for editing
- **Git** for history and backup
- **Obsidian Git plugin** for convenient pull/push inside Obsidian
- **GitHub Pages** for public or semi-public static hosting

This gives the best balance of:
- low lock-in
- version control
- easy rollback
- cheap hosting
- clean separation between editing and publishing

## Option 1: Obsidian Publish

### Pros
- easiest polished publishing experience
- native Obsidian feel
- low setup burden

### Cons
- paid and proprietary
- less flexible than Git-backed static hosting
- weaker fit for source-first pipelines where you want generated outputs and deployment automation

### Best use case
- fastest path if you want minimal setup and are comfortable paying for convenience

## Option 2: GitHub Pages

### Pros
- free for static hosting
- fits naturally with Git history
- works well with generated sites from vault markdown
- easy to automate with GitHub Actions

### Cons
- requires a repository and Pages setup
- less interactive than full app hosting
- public repos are simplest; private-repo Pages setups depend on account/org plan and settings

### Best use case
- best default for this project

## Option 3: Obsidian Git plugin

### Important note
The Obsidian Git plugin is **not a hosting solution**.
It is a sync/version-control convenience layer inside Obsidian.

### What it is good for
- pulling and pushing changes from inside Obsidian
- automatic snapshots
- reducing friction for note editing workflows

### Best use case
- use it together with GitHub Pages, not instead of GitHub Pages

## Recommended workflow

1. Edit vault files in Obsidian
2. Use Git or Obsidian Git plugin to commit and push changes
3. GitHub Actions runs `python build_vault_site.py`
4. Generated `site/` is deployed to GitHub Pages

## Current local implementation

This vault already includes:
- `build_vault_site.py` - static-site exporter for the `wiki/` layer
- `.github/workflows/deploy-pages.yml` - GitHub Pages deployment workflow
- `wiki/index.md` - site homepage entry point

## When to choose Obsidian Publish instead

Choose Obsidian Publish if you care most about speed and simplicity, and less about:
- open Git-based deployment
- custom build steps
- explicit separation of raw sources, registries, and derived site output

## Blunt recommendation

For this clinpharm system, I would use:
- **Obsidian Git plugin** for editing convenience
- **GitHub Pages** for hosting
- **Obsidian Publish only if you want the easiest polished UI and do not mind paying / being more locked in**
