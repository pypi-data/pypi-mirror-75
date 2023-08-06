# ghupdatesecret

A command-line utility to update GitHub repository secrets.

## Usage

`ghupdatesecret --user USER --password PASSWORD repository secret_name`

Update the secret with `secret_name` in the repository `repository` (in
`owner/name` format) to the contents of STDIN. Named arguments `--user`
and `--password` are required to authenticate to the GitHub API.
