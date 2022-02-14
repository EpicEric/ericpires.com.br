import { html } from "htm/react";
import { useMemo } from "react";
import type { FC } from "react";
import type { GetStaticProps, GetStaticPaths } from "next";
import Head from "next/head";
import { getMDXComponent } from "mdx-bundler/client";
import CustomMDXPostComponents from "../../components/CustomMDXPostComponents";
import { getAllPosts, getSinglePost } from "../../utils/MDXPosts";
import { formatISODate } from "../../utils/formatISODate";
import Env from "../../utils/Env";
import type { MDXPost } from "../../types/MDXPost";

type StaticPath = { slug: string };

export const getStaticProps: GetStaticProps<MDXPost, StaticPath> = async ({
  params: { slug },
}) => {
  if (Env.disableBlog) {
    return { notFound: true };
  }
  const post = await getSinglePost(slug);
  return {
    props: { ...post },
  };
};

export const getStaticPaths: GetStaticPaths<StaticPath> = async () => {
  if (Env.disableBlog) {
    return { paths: [], fallback: false };
  }
  const paths = (await getAllPosts()).map(({ slug }) => ({ params: { slug } }));
  return {
    paths,
    fallback: false,
  };
};

const BlogPost: FC<MDXPost> = ({ code, frontmatter }) => {
  const Component = useMemo(() => getMDXComponent(code), [code]);

  return html`
    <div>
      <${Head}>
        <title>${frontmatter.title} - Eric Rodrigues Pires</title>
      <//>
      <${CustomMDXPostComponents.Heading1} noAnchor=${true}
        >${frontmatter.title}<//
      >
      ${frontmatter.createdOn &&
      html`<p>${formatISODate(frontmatter.createdOn)}</p>`}
      ${frontmatter.createdOn &&
      frontmatter.updatedOn &&
      frontmatter.updatedOn !== frontmatter.createdOn &&
      html`<p>Last update: ${formatISODate(frontmatter.updatedOn)}</p>`}
      <p>${frontmatter.shortDescription}</p>
      <${Component} components=${CustomMDXPostComponents} />
    </div>
  `;
};

export default BlogPost;
