The file format is a json dictionnary with the followng fields :

*   fileFormatVersion : a string decribing this format. v1.0 is the current format
*   description : a description of the global project or of this multigit file
*   repositories : a list of dictionnary, each one describing a repository
        Each repository is composed of several fields
        * url : the url to clone from. The user name should be stripped from the URL normally
        * head : where to point the head after the checkout. This could be either a tag, a branch or a commit
        * destination : a relative path with \ as path separators, to point where to put this repo relative to the base path
        * description : obsolete, no longer used field
        * head_type : either one of the strings "tag", "branch" or "commit". This field is non mandatory and ignored by the tool, it is purely for human convenience.


Example

{
    "fileFormatVersion" : "1.0",
    "description": "Multigit file for project development",
    "repositories": [
        {
            "url":"https://repo_url.company.com/repositories/proj1/Dev.git",
            "head":"master",
            "head_type":"branch",
            "destination":"Dev",
        },
        {
            "url":"https://repo_url.company.com/repositories/proj1/component1.git",
            "head":"TAG_VERSION1",
            "head_type":"tag",
            "destination":"Dev\components\component1",
        }
    ]
}