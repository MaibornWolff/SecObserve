/// <reference types="cypress" />

describe('sanity check - login', () => {
  beforeEach(() => {
    cy.visit(Cypress.env('BASE_URL') + '/#/login')
  })

  it('displays 2 credential fields and 2 buttons', () => {
    cy.get('input').should('have.length', 2)
    cy.get('button').should('have.length', 2)
  })
})
