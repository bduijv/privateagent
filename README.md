                    Host
                      │
                Podman containers
                      │
          ┌───────────┴───────────┐
          │                       │
          ▼                       ▼
    ┌───────────┐           ┌───────────┐
    │   Agent   │           │ Executor  │
    │           │           │           │
    │ Planning  │──────────▶│ Python    │
    │ Reasoning │  requests │ Tests     │
    │ Tool logic│           │ Commands  │
    └─────┬─────┘           └─────┬─────┘
          │                       │
          ▼                                      ▼
       Ollama              Restricted workspace
       
The agent decides what to do. The executor performs operations within explicitly granted permissions.

We would aim for:
- An unprivileged agent user.
- An unprivileged executor user.
- No unnecessary Linux capabilities.
- no-new-privileges.
- No access to your SSH keys or other sensitive host directories.
- An internal network for agent-to-Ollama communication.
- A narrowly scoped workspace mount.
- Resource and execution-time limits for the executor.
- Git commits or another recovery mechanism for project changes.
One crucial qualification: separate containers do not automatically mean the executor is secure. If the agent can instruct it to execute arbitrary shell commands, the executor's filesystem mounts, credentials, network access, and Linux privileges determine what those commands can do.
