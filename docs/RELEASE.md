# Release

## Step 1 - Bump the current version

This will automate the process of updating the version strings in the source files as well as create a new tag.

    poetry run bumpver update --major

## Step 2 - Publish to PyPI

    poetry build
    poetry publish -u [USERNAME] -p [PASSWORD]

## Step 3 - Create a new release in Github
