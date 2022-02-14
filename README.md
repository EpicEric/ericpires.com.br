# ericpires.com.br

My personal static website, built from scratch with Next.js. Currently work-in-progress.

## Development server

```sh
npm run dev
```

## Build and deploy

```sh
npm run build
npm run deploy:webdav
```

Certain deployment options (server, directory, username) can be saved to `.env.local` for autofill:

- `WEBDAV_DEPLOY_SERVER`
- `WEBDAV_DEPLOY_DIRECTORY`
- `WEBDAV_DEPLOY_USERNAME`
