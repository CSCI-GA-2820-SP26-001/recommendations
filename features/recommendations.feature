Feature: Recommendations Service
    As a store manager
    I need to be able to manage recommendations
    So that I can link two products together with a recommendation type

    Background: The server is running
        Given the server is running at "http://localhost:8080"

    Scenario: Create a Recommendation
        When I visit the "Home Page"
        Then I should see "Recommendations" in the title
        When I set the "Source Product ID" to "1"
        And I set the "Recommended Product ID" to "2"
        And I select "Cross Sell" in the "Recommendation Type" dropdown
        And I press the "Create" button
        Then I should see the message "Recommendation created successfully!"
        And I should see "1" in the "Source Product ID" field
        And I should see "2" in the "Recommended Product ID" field