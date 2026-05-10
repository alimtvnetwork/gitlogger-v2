# Gitlogs App

## Menu

### Profile

- UserName
- Email
- GeneratedKeyApi
- Token

### Roles

- Admin
- Editor

### AccessToRoles

- Admin

	- App-Create
	- App-View
	- App-Modify
	- App-Delete

### GitProfile

- format:hide

	- githbub.com/$user/repo
	- github.com/$org/repo

- Profiles
- Add Profile

	- profile

		- githbub.com/$user/
		- github.com/$org/

	- Acceptance

		- Accept all repos
		- Accept selected repo only

			- if we select a repo

				- https://github.com/alimtvnetwork/macro-ahk-v23

		- Accept selected repo in all version

			- https://github.com/alimtvnetwork/macro-ahk
			- https://github.com/alimtvnetwork/macro-ahk-v23
			- https://github.com/alimtvnetwork/macro-ahk-v5

	- IsRestrictInBranch
	- StrictBranch

### Repo

- List
- History

### RepoVersion

### History

### Action

## endpoint

### /append-log

- RepoUrl
- RootRepo
- Branch
- TempToken

	- ...random

- Token
- PipelineName
- GitSha256

	- Hash

- Logs

	- []

		- lines

- ErrorLogs

	- []

		- lines

- FilePaths

	- []

- HasError

### /fixed-log

- RepoUrl
- Branch
- TempToken

	- ...random

- RootRepo
- Token
- PipelineName

### /clear-log

- RepoUrl
- Branch
- TempToken

	- ...random

- RootRepo
- Token
- PipelineName

### /clear-log-all

- RepoUrl
- Branch
- TempToken

	- ...random

- RootRepo
- Token

### /get-logs

- RepoUrl
- GitSha256

	- Hash

### /get-logs?q=github.com/$org/$repo

- GitSha256

	- Hash

		- Receive

### /get-pipeline-logs

- RepoUrl
- GitSha256

	- Hash

- PipelineName

### /get-pipeline-logs?q=github.com/$org/$repo

- GitSha256

	- Hash

		- Receive

- PipelineName

### /get-error-logs

- RepoUrl
- GitSha256

	- Hash

### /get-pipeline-error-logs

- RepoUrl
- GitSha256

	- Hash

- PipelineName

## Transaction

