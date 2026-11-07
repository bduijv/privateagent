                    AGENT
                      |
             ┌────────┴────────┐
             |                 |
           ai-net         exec-control
             |                 |
           Ollama           Executor
                               |
                            exec-net
                               |
                            Internet

Agent: no internet access, no shell access, LangGraph orchestration only.
Ollama: internal network only, local model inference.
Executor: shell access, project workspace, outbound internet.
Executor API: internal communication with the agent.
Networking: three separate networks.
Security: rootless containers, non-root users, dropped capabilities, resource limits and no host mounts beyond the project workspace.
