import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import { App } from "./App";
import "./styles.css";

declare global {
  interface Window {
    GitLogsBoot?: {
      restRoot: string;
      nonce: string;
      version: string;
    };
  }
}

const mount = document.getElementById("git-logs-admin-root");
if (mount) {
  createRoot(mount).render(
    <StrictMode>
      <App boot={window.GitLogsBoot} />
    </StrictMode>
  );
}
