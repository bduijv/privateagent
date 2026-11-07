from graph import build_graph

def main():
    app = build_graph()

    result = app.invoke(
        {
            "messages": (
                "user"
                """
Use the execute_command tool to run `python --version` in the workspace root.

Use this exact command: ["python", "--version"]
Use "." as the working directory.

Do not use list_files. Report the command output and exit code.
                """
            )
        },
        config={
            "recursion_limit": 10
        },
    )

    #Display tool execution results:
    for message in result["messages"]:
        print(f"\nMessage type: {message.type}")
        print(f"Message content: {message.content}")

        if message.type == "tool":
            print(f"Tool executed: {message.name}")

    #Display the final model response:
    print("\nAgent response:")
    print(result["messages"][-1].content)

if __name__ == "__main__":
    main()
