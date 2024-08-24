module.exports = {
  e2e: {
    // Folder where Cypress should look for test files
    specPattern: 'cypress/e2e/**/*.cy.{js,jsx,ts,tsx}',

    // Base URL of the application under test
    baseUrl: 'http://localhost:3000',

    // viewport size for the tests
    viewportWidth: 1280,
    viewportHeight: 720,
  },
};
