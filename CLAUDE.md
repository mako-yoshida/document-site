# Document Site - Claude Code Configuration

## Repository Information
- **Repository**: https://github.com/mako-yoshida/document-site
- **GitHub Pages**: https://mako-yoshida.github.io/document-site
- **Main Branch**: main

## Project Structure
```
documents/
├── config.json              # Site configuration
├── business-strategy/       # Business strategy documents
│   ├── zenpo-strategy.md
│   └── proptech-market-strategy.md
├── sample-folder/
└── technical/
```

## Development Commands
```bash
# Authentication
git config --global credential.helper store

# Check status
git status
git log --oneline -5

# Deploy changes
git add .
git commit -m "Description"
git push origin main

# Local server (if needed)
python3 -m http.server 8000
```

## File Management
- All documents are managed through `documents/config.json`
- New files must be added to both the filesystem and config.json
- Changes require git commit and push to appear on GitHub Pages

## Last Updated
2025-08-12 - Initial configuration setup