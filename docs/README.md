# Echo Server Documentation

This is the documentation for Echo Server, built with Jekyll using the default Minima theme.

## Local Development

### Prerequisites
- Ruby 2.6+
- Bundler

### Setup
```bash
cd docs
bundle install
bundle exec jekyll serve
```

Visit http://localhost:4000/echoserver/

## Build for GitHub Pages

The site is automatically built and deployed by GitHub Pages when changes are pushed to the main branch.

## Structure

- `_config.yml` - Jekyll configuration
- `index.md` - Home page
- `*.md` - Documentation pages
- `Gemfile` - Ruby dependencies (minimal)

## Theme

Using Jekyll's default Minima theme with minimal dependencies:
- jekyll (~> 4.3)
- minima (~> 2.5)
- webrick (~> 1.7)

