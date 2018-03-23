Feature: Get information about identities

  As a user
  I want to find out about my identities managed by Atmoshere

  Scenario: Show all of my identities
    Given a new working directory
    When I run "atmo identity list"
    Then it should pass
    And the command output should contain:
        """
        +--------------------------------------+--------+-------------------+-----------+--------------+---------------+
        | uuid                                 | name   | provider          | quota_cpu | quota_memory | quota_storage |
        +--------------------------------------+--------+-------------------+-----------+--------------+---------------+
        | a5a6140d-1122-4581-87dc-bd9704fa07ec | eriksf | Cloudlab - ErikOS |        16 |          128 |            10 |
        +--------------------------------------+--------+-------------------+-----------+--------------+---------------+
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
        | id                      | 2                                    |
        | uuid                    | a5a6140d-1122-4581-87dc-bd9704fa07ec |
        | username                | eriksf                               |
        | user_id                 | 1                                    |
        | user_uuid               | 3697d380-95d4-43fa-ad3e-3e9371f0522e |
        | key                     | Username: eriksf, Project:eriksf     |
        | is_leader               | True                                 |
        | provider                | Cloudlab - ErikOS                    |
        | provider_id             | 4                                    |
        | provider_uuid           | e367f6fa-e834-4fe6-873c-bba4344d1464 |
        | usage                   | -1                                   |
        | quota_cpu               | 16                                   |
        | quota_memory            | 128                                  |
        | quota_storage           | 10                                   |
        | quota_floating_ip_count | 10                                   |
        | quota_instance_count    | 10                                   |
        | quota_port_count        | 10                                   |
        | quota_snapshot_count    | 10                                   |
        | quota_storage_count     | 10                                   |
        +-------------------------+--------------------------------------+
        """
