# ericpires.com.br

My personal website, built with Hugo and deployed with Netlify.

## Installation

```sh
sudo apt-get install hugo  # or brew install hugo
git clone --recurse-submodules https://github.com/epiceric/ericpires.com.br
cd ericpires.com.br
```

## Add a post

Create a draft in `content/posts/my-new-post.md`, edit, and publish.

```sh
hugo new posts/my-new-post.md  # Create a draft
# Change `draft: true` to `draft: false`
```

## Serve locally

```sh
hugo server
```

You can also use the `-D` flag to show drafts as posts.

## Build

```sh
hugo
```

Serve files from the `public/` folder. You can also use the `-D` flag to transform drafts into posts.
