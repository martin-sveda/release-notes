# Release notes generator

The script takes git logs for two given tags and generates the release notes in the following form:


PR22456 {message}
 - {Id as link} {Type} {Name}
 - {Id as link} {Type} {Name}
 - {Id as link} {Type} {Name}
 - {Id as link} {Type} {Name}

PR 22457 {message}
- {Id as link} {Type} {Name}
 - {Id as link} {Type} {Name}
 - {Id as link} {Type} {Name}

PR 22457 {message}
 - {Id as link} {Type} {Name}
 - {Id as link} {Type} {Name}
 - {Id as link} {Type} {Name}
 - {Id as link} {Type} {Name}


# Things to consider

1. Make a FileWriter class so it can output to stdout or specific file
2. Consider filtering PR just from specified branch (to list only the PR done by specific team)


