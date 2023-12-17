module.exports = {
  env: {
    browser: true,
    es2021: true,
  },
  extends: [
    "eslint:recommended",
    "plugin:react/recommended",
    "plugin:@typescript-eslint/recommended",
    "plugin:security/recommended-legacy",
    "plugin:react-hooks/recommended",
  ],
  parser: "@typescript-eslint/parser",
  parserOptions: {
    ecmaFeatures: {
      jsx: true,
    },
    ecmaVersion: "latest",
    sourceType: "module",
  },
  plugins: ["react", "@typescript-eslint", "security"],
  rules: {},
  settings: {
    react: {
      pragma: "React", // Pragma to use, default to "React"
      version: "detect", // React version. "detect" automatically picks the version you have installed.
    },
  },
  overrides: [
    {
      files: ["*.tsx", "*.ts"],
      rules: {
        "react/react-in-jsx-scope": "off",
        "react/display-name": "off",
        "react/jsx-key": "off",
        "@typescript-eslint/no-explicit-any": "off",
      },
    },
  ],
};
