# ericpires.com.br

My personal website, built with Hexo and deployed with Netlify.

## Installation

```sh
npm install -g hexo
git clone --recurse-submodules https://github.com/epiceric/ericpires.com.br
cd ericpires.com.br
npm install
```

## Add a post

The new post will be created in `source/_posts/my-slug.md`.

```sh
hexo new post "New post" -s "my-slug"
```

## Build

Static files will be generated on `build/`.

```sh
hexo generate
```

## Serve locally

```sh
hexo server
```
