const constants = {
  DEVELOPMENT: 'development',
  runtimeConfigPath: 'window.__RUNTIME_CONFIG__',
};

const generateJSON = (config) =>
  `${constants.runtimeConfigPath} = ${JSON.stringify(config)};`;

module.exports = {
  generateJSON,
  constants,
};
