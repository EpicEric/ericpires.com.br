import { html } from "htm/react";
import type { FC } from "react";
import type { GetStaticProps } from "next";
import Link from "next/link";
import Head from "next/head";
import { getAllPosts } from "../../utils/MDXPosts";
import { formatISODate } from "../../utils/formatISODate";
import Env from "../../utils/Env";
import type { MDXPost } from "../../types/MDXPost";

type StaticProps = { posts: MDXPost[] };

export const getStaticProps: GetStaticProps<StaticProps> = async () => {
  if (Env.disableBlog) {
    return { notFound: true };
  }
  const posts = await getAllPosts();
  return {
    props: { posts },
  };
};

const Blog: FC<StaticProps> = ({ posts }) => {
  return html`
    <div>
      <${Head}>
        <title>Blog - Eric Rodrigues Pires</title>
      <//>
      <h1>Blog</h1>
      <div>
        <li>
          ${posts.map((post) => {
            return html`
              <ul key=${post.slug}>
                <${Link}
                  href=${{
                    pathname: "/blog/[slug]",
                    query: { slug: post.slug },
                  }}
                >
                  ${`${
                    post.frontmatter.language
                      ? `${post.frontmatter.language} `
                      : ""
                  }${formatISODate(post.frontmatter.createdOn)} - ${
                    post.frontmatter.title
                  }`}
                <//>
              </ul>
            `;
          })}
        </li>
      </div>
    </div>
  `;
};

export default Blog;
