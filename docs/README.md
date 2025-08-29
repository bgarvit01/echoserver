# Echo Server Documentation

This directory contains the Jekyll-based documentation website for Echo Server.

## Local Development

### Prerequisites
- Ruby 3.1+
- Bundler

### Setup
```bash
cd docs
bundle install
```

### Run Locally
```bash
bundle exec jekyll serve
```

The site will be available at `http://localhost:4000`.

### Build for Production
```bash
bundle exec jekyll build
```

## Structure

```
docs/
├── _config.yml           # Jekyll configuration
├── Gemfile               # Ruby dependencies
├── index.md              # Homepage
├── pages/
│   ├── quick-start/      # Quick start guides
│   │   ├── index.md
│   │   ├── docker.md
│   │   ├── docker-compose.md
│   │   ├── kubernetes.md
│   │   └── helm.md
│   └── configuration/    # Configuration docs
│       ├── index.md
│       ├── feature-toggle.md
│       ├── loggers.md
│       └── commands.md
├── assets/               # Static assets
└── _layouts/             # Jekyll layouts
```

## GitHub Pages Deployment

The documentation is automatically deployed to GitHub Pages when changes are pushed to the `main` branch. The deployment is handled by the GitHub Actions workflow in `.github/workflows/docs.yml`.

## Theme

This documentation uses the [Just the Docs](https://just-the-docs.github.io/just-the-docs/) theme, which provides:

- Clean, professional design
- Built-in search
- Mobile responsive
- Code syntax highlighting
- Easy navigation
- SEO optimization

## Contributing

When adding new documentation:

1. Follow the existing structure and naming conventions
2. Add proper front matter to each page
3. Use appropriate navigation order (`nav_order`)
4. Test locally before submitting
5. Update the table of contents as needed

## Customization

The documentation can be customized by:

- Modifying `_config.yml` for site-wide settings
- Adding custom CSS in `assets/css/`
- Creating custom layouts in `_layouts/`
- Adding custom JavaScript in `assets/js/`
