# LazyCodr 🚀

A CLI tool designed to help lazy coders get their work done with AI! LazyCodr automates tasks such as generating pull requests, and more, using our beloved AI models.

## Features 💡

- Generate pull request descriptions
- Automate commit messages (incoming ...)
- Easy configuration
- Works with GitHub API
- Powered by LLMs (for now only OpenAI)

## Installation 💻

```bash
pip install lazycodr
```

## Requirements 🔑

Before you can use LazyCodr, you'll need to create an OpenAI API key and a GitHub token. Here's how to do both:

### OpenAI API Key

1. Sign up for an account on the [OpenAI website](https://beta.openai.com/signup/) if you don't have one already.
2. Once logged in, go to the [API Keys page](https://beta.openai.com/account/api-keys).
3. Click on "Create an API key" and copy the generated key.

### GitHub Token

1. Log in to your GitHub account and go to the [Personal Access Tokens page](https://github.com/settings/tokens).
2. Click on "Generate new token" in the top right corner.j
3. Give your token a descriptive name and select the required scopes (for LazyCodr, you'll need `repo` and `user` scopes.
4. Click "Generate token" at the bottom of the page and copy the generated token.

After you have both your OpenAI API key and GitHub token, you can configure LazyCodr by running the following command:

```bash
lazycodr config
```

This command will prompt you to enter your API key and GitHub token, which will be securely stored for future use.

Now you're all set to use LazyCodr! 🚀


## Usage 📚

1. Configure LazyCodr with your OpenAI API key and GitHub token:

```bash
lazycodr config
```

2. Use LazyCodr to generate a pull request description:

```bash
lazycodr pr generate <repo_name> <pr_number>
```

## Roadmap 🗺️

> "A lazy programmer is a great programmer"

We're on a mission to make all of us even lazier 😅!
There is no clear roadmap, but here are some ideas for LazyCodr's future:

🚀 **Commit Message Generation**: <br />
Automatically generate meaningful commit messages based on your code changes, so you can save time and focus on coding.

🚀 **Codebase Conversations**: <br />
Chat with your codebase to get AI-powered recommendations and insights about your code, helping you make informed decisions as you work.

🚀 **AI-driven Guidance**: <br />
Receive step-by-step guidance from AI on how to write new features or implement specific functionality, making it easier to tackle challenging tasks.

🚀 **README Generation**: <br />
Automatically generate well-structured and informative README files for your projects, ensuring that your documentation is always up to date.

🚀🚀 ... replace yourself entirely so you can take 10 jobs in parallel 🤑🤑🤑

Remember, even though I'm aiming to make you the laziest 😜 programmer possible, I still appreciate your help.
If you have any ideas, suggestions, or improvements, feel free to contribute and help make LazyCodr even better for your fellow lazy programmers.

Together, we can redefine the art of lazy programming! 😎

## Contributing 🤝

Contributions are welcome! Feel free to submit a pull request or open an issue.

## License 📄

This project is licensed under the [MIT License](LICENSE).

Happy coding! 🎉
