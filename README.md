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

### Directly

The new post will be created in `source/_posts/my-slug.md`.

```sh
hexo new post "New post" -s "my-slug"
```

### As a draft

You can create a draft with similar options as you would create a post, changing the layout.

```sh
hexo new draft "New post" -s "my-slug"
```

See [Serve locally](#serve-locally) for how to render drafts.

Once satisfied, you can publish the draft to a post.

```sh
hexo publish "my-slug"
```

## Serve locally

This will create a development server that watches any changes to files. The `--draft` argument will render any drafts as posts.

```sh
hexo server --draft
```

## Build

You can build static files for deployment in production. They will be generated in `build/`.

```sh
hexo generate
```

