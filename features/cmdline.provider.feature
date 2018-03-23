Feature: Get information about cloud providers

  As a user
  I want to find out about the cloud providers managed by Atmoshere

  Scenario: Show all of the cloud providers
    Given a new working directory
    When I run "atmo provider list"
    Then it should pass
    And the command output should contain:
        """
        +----+--------------------------------------+-------------------+-----------+----------------+--------+--------+------------+
        | id | uuid                                 | name              | type      | virtualization | public | active | start_date |
        +----+--------------------------------------+-------------------+-----------+----------------+--------+--------+------------+
        |  4 | e367f6fa-e834-4fe6-873c-bba4344d1464 | Cloudlab - ErikOS | OpenStack | KVM            | True   | True   | 2017-09-18 |
        +----+--------------------------------------+-------------------+-----------+----------------+--------+--------+------------+
        """

  Scenario: Show all the details for a particular cloud provider
    Given a new working directory
    When I run "atmo provider show e367f6fa-e834-4fe6-873c-bba4344d1464"
    Then it should pass
    And the command output should contain:
        """
        +----------------+--------------------------------------------------------------------------+
        | Field          | Value                                                                    |
        +----------------+--------------------------------------------------------------------------+
        | id             | 4                                                                        |
        | uuid           | e367f6fa-e834-4fe6-873c-bba4344d1464                                     |
        | name           | Cloudlab - ErikOS                                                        |
        | description    | This is a Cloudlab cloud.                                                |
        | type           | OpenStack                                                                |
        | virtualization | KVM                                                                      |
        | sizes          | m1.xlarge, m1.large, m1.medium, m1.small, m1.tiny, manila-service-flavor |
        | auto_imaging   | False                                                                    |
        | public         | True                                                                     |
        | is_admin       | True                                                                     |
        | active         | True                                                                     |
        | start_date     | 2017-09-18                                                               |
        | end_date       |                                                                          |
        +----------------+--------------------------------------------------------------------------+
        """
