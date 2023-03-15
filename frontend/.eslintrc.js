// to-do: currently does not work unless error is ignored, Es6 upgrade did not work either
// eslint-disable-next-line no-undef
module.exports = {
  env: {
    browser: true,
    es2021: true,
  },
  extends: [
    "eslint:recommended",
    "plugin:react/recommended",
    "plugin:@typescript-eslint/recommended",
    "plugin:security/recommended",
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
      // You can also use `16.0`, `16.3`, etc, if you want to override the detected value.
      // It will default to "latest" and warn if missing, and to "detect" in the future
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
