/// <reference types="react" />
import type { ReactElement, ReactHTML } from "react";
import type { ComponentMap } from "mdx-bundler/client";
import { html } from "htm/react";
import Link from "next/link";
import type { CustomHeadingProps } from "../types/CustomHeadingProps";

const CustomLink: (props: JSX.IntrinsicElements["a"]) => ReactElement = (
  props
) => {
  const { href } = props;
  const isInternalLink = href && (href.startsWith("/") || href.startsWith("#"));

  if (isInternalLink) {
    return html`
      <${Link} href=${href}>
        <a ...${props} />
      <//>
    `;
  }

  return html`<a target="_blank" rel="noopener noreferrer" ...${props} />`;
};

function createHeadingAnchorId(title: string) {
  const id = title
    .toLowerCase()
    .replaceAll(/[^- \w\d'_:]/g, "")
    .trim()
    .split(/ +/g)
    .join("-");
  if (id.match(/^\d/)) {
    return `a-${id}`;
  }
  return id;
}

export function createHeadingComponent(
  element: keyof ReactHTML,
  className?: string
) {
  return (props: JSX.IntrinsicElements["h1"] & CustomHeadingProps) => {
    const { noAnchor, customId, ...headingProps } = props;
    if (noAnchor) {
      return html`<${element} className=${className} ...${headingProps} />`;
    }
    const anchorId = encodeURIComponent(
      customId || createHeadingAnchorId(props.children.toString())
    );
    return html`<${element}
      id=${anchorId}
      className=${className}
      ...${headingProps}
    />`;
  };
}

const Heading1 = createHeadingComponent("h1", "text-4xl");
const Heading2 = createHeadingComponent("h2", "text-3xl");
const Heading3 = createHeadingComponent("h3", "text-2xl");
const Heading4 = createHeadingComponent("h4", "text-xl");

const CustomMDXPostComponents: ComponentMap = {
  /* Base components */
  a: CustomLink,
  h1: Heading1,
  h2: Heading2,
  h3: Heading3,
  h4: Heading4,

  /* MDX components */
  Heading1,
  Heading2,
  Heading3,
  Heading4,
  Link,
  // Image, // TODO: SSG with https://nextjs.org/docs/messages/export-image-api
};

export default CustomMDXPostComponents;
