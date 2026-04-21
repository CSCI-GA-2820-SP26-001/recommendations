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

    Scenario: Read an existing Recommendation
        When I visit the "Home Page"
        Then I should see "Recommendations" in the title
        When I set the "Source Product ID" to "10"
        And I set the "Recommended Product ID" to "20"
        And I select "Cross Sell" in the "Recommendation Type" dropdown
        And I press the "Create" button
        Then I should see the message "Recommendation created successfully!"
        When I copy the "ID" field
        And I press the "Clear" button
        And I paste the "Read ID" field
        And I press the "Read" button
        Then I should see the message "Recommendation retrieved successfully!"

    Scenario: Read a non-existent Recommendation returns 404
        When I visit the "Home Page"
        Then I should see "Recommendations" in the title
        When I set the "Read ID" to "999999"
        And I press the "Read" button
        Then I should see the message "was not found"

    Scenario: Update an existing Recommendation's type
        When I visit the "Home Page"
        Then I should see "Recommendations" in the title
        When I set the "Source Product ID" to "30"
        And I set the "Recommended Product ID" to "40"
        And I select "Cross Sell" in the "Recommendation Type" dropdown
        And I press the "Create" button
        Then I should see the message "Recommendation created successfully!"
        When I copy the "ID" field
        And I press the "Clear" button
        And I paste the "Update ID" field
        And I select "Up Sell" in the "Update Type" dropdown
        And I press the "Update" button
        Then I should see the message "Recommendation updated successfully!"

    Scenario: Update a non-existent Recommendation returns 404
        When I visit the "Home Page"
        Then I should see "Recommendations" in the title
        When I set the "Update ID" to "999999"
        And I select "Up Sell" in the "Update Type" dropdown
        And I press the "Update" button
        Then I should see the message "was not found"

    Scenario: List all Recommendations when some exist
        When I visit the "Home Page"
        Then I should see "Recommendations" in the title
        When I set the "Source Product ID" to "100"
        And I set the "Recommended Product ID" to "200"
        And I select "Cross Sell" in the "Recommendation Type" dropdown
        And I press the "Create" button
        Then I should see the message "Recommendation created successfully!"
        When I press the "Clear" button
        And I press the "List All" button
        Then I should see the message "Recommendations listed successfully!"
        And I should see "100" in the results
        And I should see "200" in the results
        And I should see "CROSS_SELL" in the results

    Scenario: List all Recommendations when none exist
        When I visit the "Home Page"
        Then I should see "Recommendations" in the title
        When I press the "List All" button
        Then I should see the message "No recommendations found"

    Scenario: Delete an existing Recommendation
        When I visit the "Home Page"
        Then I should see "Recommendations" in the title
        When I set the "Source Product ID" to "50"
        And I set the "Recommended Product ID" to "60"
        And I select "Cross Sell" in the "Recommendation Type" dropdown
        And I press the "Create" button
        Then I should see the message "Recommendation created successfully!"
        When I copy the "ID" field
        And I press the "Clear" button
        And I paste the "Delete ID" field
        And I press the "Delete" button
        Then I should see the message "Recommendation deleted successfully!"

    Scenario: Delete a non-existent Recommendation returns 404
        When I visit the "Home Page"
        Then I should see "Recommendations" in the title
        When I set the "Delete ID" to "999999"
        And I press the "Delete" button
        Then I should see the message "was not found"

    Scenario: Search Recommendations by Source Product ID
        When I visit the "Home Page"
        Then I should see "Recommendations" in the title
        When I set the "Source Product ID" to "500"
        And I set the "Recommended Product ID" to "600"
        And I select "Cross Sell" in the "Recommendation Type" dropdown
        And I press the "Create" button
        Then I should see the message "Recommendation created successfully!"
        When I press the "Clear" button
        And I set the "Query Source Product ID" to "500"
        And I press the "Search" button
        Then I should see the message "Search completed successfully!"
        And I should see "500" in the results
        And I should see "600" in the results

    Scenario: Search Recommendations by Type
        When I visit the "Home Page"
        Then I should see "Recommendations" in the title
        When I set the "Source Product ID" to "700"
        And I set the "Recommended Product ID" to "800"
        And I select "Up Sell" in the "Recommendation Type" dropdown
        And I press the "Create" button
        Then I should see the message "Recommendation created successfully!"
        When I press the "Clear" button
        And I select "Up Sell" in the "Query Type" dropdown
        And I press the "Search" button
        Then I should see the message "Search completed successfully!"
        And I should see "UP_SELL" in the results

    Scenario: Search Recommendations with no matches
        When I visit the "Home Page"
        Then I should see "Recommendations" in the title
        When I set the "Query Source Product ID" to "99999999"
        And I press the "Search" button
        Then I should see the message "No recommendations found"

    Scenario: Like a Recommendation
        When I visit the "Home Page"
        Then I should see "Recommendations" in the title
        When I set the "Source Product ID" to "900"
        And I set the "Recommended Product ID" to "901"
        And I select "Cross Sell" in the "Recommendation Type" dropdown
        And I press the "Create" button
        Then I should see the message "Recommendation created successfully!"
        When I copy the "ID" field
        And I press the "Clear" button
        And I paste the "Like ID" field
        And I press the "Like" button
        Then I should see the message "Recommendation liked successfully!"
        And I should see "1" in the "Like Result Like Count" field
    
    Scenario: Like a non-existent Recommendation returns 404
        When I visit the "Home Page"
        Then I should see "Recommendations" in the title
        When I set the "Like ID" to "999999"
        And I press the "Like" button
        Then I should see the message "was not found"
    
