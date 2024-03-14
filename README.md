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



