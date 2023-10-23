import { Given, When, Then } from 'cypress-cucumber-preprocessor/steps';

Given('I am on the login page', () => {
  cy.visit('http://localhost:5000/login'); // Replace with your login page URL
});

When('I enter my username and password', () => {
  cy.get("[data-test='input-email']").type('master@test.com'); // Replace with your username field selector
  cy.get("[data-test='input-password']").type('123456'); // Replace with your password field selector
});

When('I enter an invalid username and password', () => {
  cy.get("[data-test='input-email']").type('other@test.com'); // Replace with your username field selector
  cy.get("[data-test='input-password']").type('1234'); // Replace with your password field selector
});

When('I click on the login button', () => {
  cy.get('[data-test="button-login"]').click(); // Replace with your login button selector
});

Then('I should be logged in', () => {
  cy.get('[data-test="button-exit"]').should('be.visible'); // Replace with the URL of the page after successful login
});

Then('I should see an error message', () => {
  cy.get('[data-test="msg-invalid-login"]').should('be.visible'); // Replace with your error message selector
});

Then('I should see mandatory field message', () => {
  cy.get('.invalid-feedback').should('be.visible'); // Replace with your error message selector
});
