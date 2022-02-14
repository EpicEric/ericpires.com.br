import "../styles/globals.css";
import { html } from "htm/react";
import type { AppProps } from "next/app";

const App = ({ Component, pageProps }: AppProps) => {
  return html`<${Component} ...${pageProps} />`;
};

export default App;
