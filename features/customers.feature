Feature: The customer REST API back-end
    As an E-Commerce website owner
    I need a RESTful catalog service
    So that I can keep track of all my customers

Background:
    Given the following customers
        | id | first_name | last_name | gender | age | email | address_line1 | address_line2 | phonenumber |
        | 1  | Jackie     | Shroff    | M      | 51  | j@k.c | Aamchi        | Mumbai        | 420420      |
        | 2  | Roger      | Federer   | M      | 35  | r@f.c | Zurich        | Switzerland   | 241561      |
        | 3  | Maria      | Sharapova | F      | 28  | m@s.c | Moscow        | Russia        | 138453      |

Scenario: The server is running
    When I visit the home page
    Then I should see "Customer REST API Service for E-Commerce website"
    Then I should not see "404 Not Found"

Scenario: List all customers
    When I visit "customers"
    Then I should see "Jackie"
    And I should see "Roger"
    And I should see "Maria"

Scenario: Get customer with id 2
    When I retrieve "customers" with id "2"
    Then I should see "Roger"

Scenario: Add a new customer
    When I add a new customer "Lionel Messi"
    Then I should see "Lionel"

Scenario: Update a customer
    When I retrieve "customers" with id "1"
    And I change "address_line1" to "Nariman Point"
    And I update "customers" with id "2"
    Then I should see "Nariman Point"

Scenario: Delete a customer
    When I visit "customers"
    Then I should see "Jackie"
    And I should see "Maria"
    When I delete "customers" with id "3"
    And I visit "customers"
    Then I should see "Jackie"
    And I should not see "Maria"

Scenario: Query by phone number
    When I query "customers" by "phonenumber" with value "420420"
    Then I should see "Jackie"
    When I query "customers" by "phonenumber" with value "111111"
    Then I should see "0" rows of data

Scenario: Activate a customer
    When I retrieve "customers" with id "2"
    Then I should have "active" as "True"
    When I "deactivate" "customers" with id "2"
    And I retrieve "customers" with id "2"
    Then I should have "active" as "False"
    When I "activate" "customers" with id "2"
    And I retrieve "customers" with id "2" 
    Then I should have "active" as "True"

Scenario: Deactivate a customer
    When I retrieve "customers" with id "1"
    Then I should have "active" as "True"
    When I "deactivate" "customers" with id "1"
    And I retrieve "customers" with id "1" 
    Then I should have "active" as "False"    
