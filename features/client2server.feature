Feature: Client to server
  As a personal assistant user
  I want to be able to send messages to my personal assistant
  So that I can communicate to it
  
  Background: Server is set up
    Given the server is running
      And pa is configured to use the server

  Scenario: Send ping
    Given pa is connected to the server
      And the client is set up correctly
     When I send the 'ping' action
     Then pa receives the 'ping' event
