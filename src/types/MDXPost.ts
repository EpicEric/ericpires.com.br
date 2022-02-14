export interface Frontmatter {
  title: string;
  shortDescription: string;
  isPublished: boolean;
  language?: string;
  createdOn?: Date | string;
  updatedOn?: Date | string;
}

export interface CompiledMDX {
  code: string;
  frontmatter: Frontmatter;
}

export interface MDXPost {
  code: string;
  frontmatter: Frontmatter;
  slug: string;
}
