import fs from "fs";
import path from "path";
import { exit } from "process";
import { createClient, FileStat } from "webdav";
import * as prompt from "prompt";
import { loadEnvConfig } from "@next/env";

export const ROOT_PATH = process.cwd();
export const BUILD_PATH = path.join(ROOT_PATH, "build");

function getAllBuildFiles() {
  const filenames: string[] = [];
  const dirnames: string[] = [];
  const directoryStack = [BUILD_PATH];
  while (directoryStack.length > 0) {
    const currDir = directoryStack.shift();
    fs.readdirSync(currDir, { withFileTypes: true }).forEach((dirent) => {
      if (dirent.isDirectory()) {
        directoryStack.push(path.join(currDir, dirent.name));
        dirnames.push(path.join(currDir, dirent.name));
      } else if (dirent.isFile()) {
        filenames.push(path.join(currDir, dirent.name));
      } else {
        throw new Error("Unexpected file type.");
      }
    });
  }
  return { filenames, dirnames };
}

async function deployToWebDAV() {
  const { filenames, dirnames } = getAllBuildFiles();
  if (filenames.length === 0) {
    console.log("No build files found. Exiting.");
    exit(1);
  }
  const { combinedEnv: env } = loadEnvConfig(ROOT_PATH);
  prompt.start();
  const { server, directory, username, password }: { [key: string]: string } =
    await prompt.get({
      properties: {
        server: {
          description: "Address of the WebDAV server",
          required: true,
          default: env.WEBDAV_DEPLOY_SERVER,
        },
        directory: {
          description: "WebDAV directory",
          default: env.WEBDAV_DEPLOY_DIRECTORY,
        },
        username: {
          description: "Username",
          required: true,
          default: env.WEBDAV_DEPLOY_USERNAME,
        },
        password: {
          description: "Password",
          required: true,
          hidden: true,
          replace: "*",
        } as any,
      },
    });
  const client = createClient(server, { username, password });
  const prevFiles = (
    (await client.getDirectoryContents(directory)) as FileStat[]
  ).filter((file) => file.filename !== directory);
  if (prevFiles.length > 0) {
    console.log("The following files will be deleted:");
    prevFiles.forEach((file) =>
      console.log(
        `  - ${file.basename}${file.type === "directory" ? " (directory)" : ""}`
      )
    );
    console.log("Proceed?");
    const { proceed }: { [key: string]: string } = await prompt.get({
      properties: {
        proceed: {
          description: "(y/n)",
          required: true,
          pattern: /^(y|n)$/i,
        },
      },
    });
    if (proceed.match(/n/i)) {
      console.log("Cancelled.");
      exit(1);
    }
    await Promise.all(
      prevFiles.map((file) => client.deleteFile(file.filename))
    );
    console.log(
      `Files deleted. Uploading build/ folder (${
        filenames.length > 1 ? `${filenames.length} files` : "1 file"
      })...`
    );
  } else {
    console.log(
      `No files found in WebDAV. Uploading build/ folder (${
        filenames.length > 1 ? `${filenames.length} files` : "1 file"
      })...`
    );
  }

  // Create necessary sub-directories
  for (const dirname of dirnames) {
    const davDirname = path.posix.join(
      directory,
      ...dirname.replace(BUILD_PATH, "").split(path.sep)
    );
    await client.createDirectory(davDirname);
  }
  if (dirnames.length > 0) {
    console.log(
      ` ${
        dirnames.length > 1
          ? `${dirnames.length} subdirectories`
          : "1 subdirectory"
      } created.`
    );
  }
  for (let i = 0; i < filenames.length; i++) {
    const filename = filenames[i];
    const davFilename = path.posix.join(
      directory,
      ...filename.replace(BUILD_PATH, "").split(path.sep)
    );

    /* Create files */
    const wasWritten = await client.putFileContents(
      davFilename,
      fs.readFileSync(filename)
    );
    if (!wasWritten) {
      throw new Error(
        `Failed to write file ${filename.replace(BUILD_PATH, "")}`
      );
    }

    console.log(` (${i + 1}/${filenames.length})`);
  }
  console.log("Success.");
}

deployToWebDAV();
