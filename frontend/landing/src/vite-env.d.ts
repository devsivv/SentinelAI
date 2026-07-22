/// <reference types="vite/client" />

interface ImportMetaEnv {
  readonly VITE_CITIZEN_URL?: string;
  readonly VITE_POLICE_URL?: string;
}

interface ImportMeta {
  readonly env: ImportMetaEnv;
}
