Feature: Get information about identities

  As a user
  I want to find out about my identities managed by Atmoshere

  Scenario: Show all of my identities
    Given a new working directory
    When I run "atmo identity list"
    Then it should pass
    And the command output should contain:
        """
        +--------------------------------------+--------+--------------------------------+-----------+--------------+---------------+
        | uuid                                 | name   | provider                       | quota_cpu | quota_memory | quota_storage |
        +--------------------------------------+--------+--------------------------------+-----------+--------------+---------------+
        | 716ca588-3a40-4327-9c89-84913278db10 | eriksf | Jetstream - Indiana University |       132 |          360 |           100 |
        | 32e3354c-03cc-40e1-8c33-02bc7f6be299 | eriksf | Jetstream - TACC               |       132 |          360 |           100 |
        +--------------------------------------+--------+--------------------------------+-----------+--------------+---------------+
        """

  Scenario: Show all the details for a particular identity
    Given a new working directory
    When I run "atmo identity show a5a6140d-1122-4581-87dc-bd9704fa07ec"
    Then it should pass
    And the command output should contain:
        """
        +-------------------------+--------------------------------------+
        | Field                   | Value                                |
        +-------------------------+--------------------------------------+
        | id                      | 1403                                 |
        | uuid                    | 32e3354c-03cc-40e1-8c33-02bc7f6be299 |
        | username                | eriksf                               |
        | user_id                 | 1010                                 |
        | user_uuid               | 0ea75b5f-40a0-441e-a08c-486a89e2a9d7 |
        | key                     | Username: eriksf, Project:eriksf     |
        | is_leader               | True                                 |
        | provider                | Jetstream - TACC                     |
        | provider_id             | 5                                    |
        | provider_uuid           | 3ff65aa8-505b-48c3-aef1-aa0ada14c756 |
        | usage                   | -1                                   |
        | quota_cpu               | 132                                  |
        | quota_memory            | 360                                  |
        | quota_storage           | 100                                  |
        | quota_floating_ip_count | 25                                   |
        | quota_instance_count    | 25                                   |
        | quota_port_count        | 25                                   |
        | quota_snapshot_count    | 10                                   |
        | quota_storage_count     | 10                                   |
        +-------------------------+--------------------------------------+
        """
