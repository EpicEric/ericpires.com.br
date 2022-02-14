import { html } from "htm/react";
import type { FC } from "react";
import Head from "next/head";

const Index: FC = () => {
  return html`
    <div
      className="bg-gray-800 h-screen justify-center flex flex-col items-center text-center"
    >
      <${Head}>
        <title>Eric Rodrigues Pires</title>
      <//>
      <div
        className="rounded-full bg-gray-300 hover:scale-105 hover:bg-gray-500 transition group"
      >
        <img
          src="/images/logo-circle.png"
          alt="Logo"
          className="h-56 w-56 group-hover:scale-125 transition"
        />
      </div>
      <h1 className="mt-2 mb-3 text-2xl text-gray-100 font-bold">
        Eric Rodrigues Pires
      </h1>
      <div className="text-gray-400">
        <p className="text-md mb-1">
          Website em construção / Website under construction
        </p>
        <p className="text-sm">© 2022</p>
      </div>
    </div>
  `;
};

export default Index;
