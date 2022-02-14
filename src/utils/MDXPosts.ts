import fs from "fs";
import path from "path";
import { compareDesc } from "date-fns";
import { bundleMDX } from "mdx-bundler";
import type { PluggableList } from "xdm/lib/core";
import type { Frontmatter, CompiledMDX, MDXPost } from "../types/MDXPost";

export const ROOT_PATH = process.cwd();
export const BLOG_PATH = path.join(ROOT_PATH, "blog");

export const readFile = (filename: string) => {
  return fs.readFileSync(path.join(BLOG_PATH, filename), { encoding: "utf-8" });
};

const getCompiledMDX = async (content: string) => {
  // Add remark and rehype plugins here
  const remarkPlugins: PluggableList = [];
  const rehypePlugins: PluggableList = [];

  try {
    const mdx = await bundleMDX<Frontmatter>({
      source: content,
      xdmOptions: (options) => {
        options.remarkPlugins = [
          ...(options.remarkPlugins ?? []),
          ...remarkPlugins,
        ];
        options.rehypePlugins = [
          ...(options.rehypePlugins ?? []),
          ...rehypePlugins,
        ];
        return options;
      },
    });
    return mdx;
  } catch (error) {
    throw new Error(error);
  }
};

export const getSinglePost = async (slug: string) => {
  const source = readFile(`${slug}.mdx`);
  const { code, frontmatter }: CompiledMDX = await getCompiledMDX(source);

  if (frontmatter.createdOn) {
    try {
      frontmatter.createdOn = new Date(frontmatter.createdOn).toISOString();
    } catch (e) {
      console.error(
        "Cannot convert createdOn date to ISO string",
        frontmatter.createdOn,
        e
      );
    }
  }
  if (frontmatter.updatedOn) {
    try {
      frontmatter.updatedOn = new Date(frontmatter.updatedOn).toISOString();
    } catch (e) {
      console.error(
        "Cannot convert updatedOn date to ISO string",
        frontmatter.updatedOn,
        e
      );
    }
  }

  return {
    frontmatter,
    code,
    slug,
  } as MDXPost;
};

export const getAllPosts = async () => {
  return (
    await Promise.all(
      fs
        .readdirSync(BLOG_PATH)
        .filter((path) => /\.mdx?$/.test(path))
        .map(async (fileName) => {
          const slug = fileName.replace(/\.mdx?$/, "");
          return await getSinglePost(slug);
        })
    )
  )
    .filter((post) => post.frontmatter.isPublished)
    .sort((first, second) => {
      const compare = compareDesc(
        new Date(first.frontmatter.createdOn),
        new Date(second.frontmatter.createdOn)
      );
      if (compare !== 0) {
        return compare;
      }
      return first.frontmatter.title.localeCompare(second.frontmatter.title);
    });
};
