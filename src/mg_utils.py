#    Copyright (c) 2019-2023 IDEMIA
#    Author: IDEMIA (Philippe Fremy, Florent Oulieres)
# 
#     Licensed under the Apache License, Version 2.0 (the "License");
#     you may not use this file except in compliance with the License.
#     You may obtain a copy of the License at
# 
#         http://www.apache.org/licenses/LICENSE-2.0
# 
#     Unless required by applicable law or agreed to in writing, software
#     distributed under the License is distributed on an "AS IS" BASIS,
#     WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#     See the License for the specific language governing permissions and
#     limitations under the License.
#


from typing import cast, Match, Any, Iterable, Sequence, Union, List, Iterator
import html, os, pathlib, re, shutil, stat, logging

from PySide6.QtWidgets import QTreeWidget, QTreeWidgetItem

from src.mg_const import MSG_BIG_DIFF, GIT_AUTH_FAILURE_MARKER

logger = logging.getLogger('mg_utils')
dbg = logger.debug
warn = logger.warning

HTML_HEADER='''<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.0//EN" "http://www.w3.org/TR/REC-html40/strict.dtd">
<html><head><meta name="qrichtext" content="1" /><style type="text/css">
p, li { white-space: pre-wrap;font-family:'Courier New'; font-size:8pt; font-weight:600; 
        font-style:normal; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; 
        -qt-block-indent:0; text-indent:0px; }
</style></head>
<body style="font-family:'Courier New'; font-size:8pt; font-weight:400; font-style:normal">'''
HTML_FOOTER='</body></html>'
TAG_BLUE_OPEN   = '<span style="background-color:#aaffff;">'
TAG_YELLOW_OPEN = '<span style="background-color:#ffff7f ">'
TAG_GREEN_OPEN  = '<span style="background-color:#ccffcc;">'
TAG_RED_OPEN    = '<span style="background-color:#ffdddd;">'
TAG_GREY_OPEN   = '<span style="background-color:#f5f5f5;">'
TAG_BLUE_CLOSE  = '</span>'
TAG_GREEN_CLOSE = '</span>'
TAG_YELLOW_CLOSE= '</span>'
TAG_RED_CLOSE   = '</span>'
TAG_GREY_CLOSE  = '</span>'
# TAG_YELLOW_OPEN = '<span style="color:#800000;background-color:#ffff7f ">'
TAG_NL = '<br/>'
re_highlight = re.compile(r'^(---|\+\+\+|diff|index).*')
re_hunk_header = re.compile('^(@@.+?@@)(.*)')
re_line_added = re.compile(r'^\+.*')
re_line_removed = re.compile(r'^-.*')
re_stat_line = re.compile(r'( .* \|.* \d+ )(\+*)(-*)(.*)')


def htmlize_diff(s: str, maxLines: int = -1) -> str:
    '''Transform a diff multi-line string into a html colorized
    string suitable for QTextEdit rich-text mode.

    If maxLines is not -1, this defines a maximum number of lines
    which will be contained in the html output.
    '''
    out = [HTML_HEADER]
    in_stat_data = True
    lines = s.split('\n')
    if maxLines != -1 and len(lines) > maxLines:
        lines = lines[:maxLines]
        lines.extend( [ '[...]', MSG_BIG_DIFF ] )

    for l in lines:
        lesc = html.escape(l)
        if in_stat_data and len(l) and l[0] == ' ':
            if re_stat_line.match(l):
                mo = cast(Match[str], re_stat_line.match(l))
                lout = mo.group(1)
                if len(mo.group(2)):
                    lout += TAG_GREEN_OPEN + mo.group(2) + TAG_GREEN_CLOSE
                if len(mo.group(3)):
                    lout += TAG_RED_OPEN + mo.group(3) + TAG_RED_CLOSE
                out.append(mo.group(4) + lout + TAG_NL)
            else:
                out.append(l + TAG_NL)
            continue
        else:
            in_stat_data = False

        if re_highlight.match(l):
            out.append(TAG_YELLOW_OPEN + l + TAG_YELLOW_CLOSE + TAG_NL)
            continue

        if re_hunk_header.match(l):
            mo = cast(Match[str], re_hunk_header.match(l))
            out.append(TAG_BLUE_OPEN + mo.group(1) + TAG_BLUE_CLOSE + mo.group(2) + TAG_NL)
            continue

        if re_line_added.match(l):
            out.append(TAG_GREEN_OPEN + lesc + TAG_GREEN_CLOSE + TAG_NL)
            continue

        if re_line_removed.match(l):
            out.append(TAG_RED_OPEN + lesc + TAG_RED_CLOSE + TAG_NL)
            continue

        out.append(lesc + TAG_NL)

    out.append(HTML_FOOTER)

    return '\n'.join(out)


def handle_cr_in_text(s: str) -> str:
    '''Handle CR in output text: the line after the CR overwrite the previous line'''
    lines = s.split('\n')
    out_lines = []
    for l in lines:
        if '\r' in l:
            if l[-1] == '\r':
                l = l[:-1]

            sublines = l.split('\r')
            l = sublines[-1]
        out_lines.append(l)

    return '\n'.join(out_lines)


def anonymise_git_url(url: str) -> str:
    # clear username from url
    if not url:
        return url

    if '://' in url:
        if url.startswith('ssh') or url.startswith('git'):
            # for ssh, neutralize username
            url = set_username_on_git_url('username', url or '')
        else:
            # for http, file: and direct clones, strip username
            url = set_username_on_git_url('', url or '')
    else:
        # scp-like ssh url syntax, see man git-clone, section url
        # quote: "the url is recognized if there is no / before the fist colon"
        # example: user@host.xz:path/to/repo.git/
        if ':' in url and (url.find('/') == -1 or url.find('/') > url.find(':')):
            url = set_username_on_git_url('username', url)

    return url


reWinPath = re.compile('^[a-zA-Z]:\\.*')

def set_username_on_git_url(username: str, url: str) -> str:
    '''Take a git url and add or substitute the username part. Returns the new url.

    When url refers to the filesystem, nothing is done on it

    If username is empty, strips the username from the url.
    '''
    if url.lower().startswith('file://'):
        return url

    if '://' in url:
        server_start = url.index('://')+3

    else:
        if url.startswith('/'):
            # linux absolute path
            return url

        if reWinPath.match(url):
            # windows absolute path
            return url

        if not ':' in url:
            # this can not be a scp like syntax, this is a path
            return url

        # scp-like ssh url syntax, see man git-clone, section url
        # quote: "the url is recognized if there is no / before the fist colon"
        # example: user@host.xz:path/to/repo.git/
        if url.find('/') < url.find(':'):
            # this is not a url, this is still a path containing a ':'
            return url

        # ok, this is a scp-like url
        server_start = 0


    try:
        server_end   = url.index('/', server_start)
    except ValueError:
        # unlikely but possible
        server_end = len(url)

    server = url[server_start:server_end]
    if '@' in server:
        server = server.split('@', 1)[1]

    if len(username):
        server = username + '@' + server

    return url[:server_start] + server + url[server_end:]


def deleteDirList(dirList: Iterable[str], ignoreDirDoesNotExist: bool = True) -> str:
    '''Try hard to delete directories listed in input.

    Returns:
        * empty string when everything goes fine.
        * error description when something fails
    '''
    errMsg = ''


    for folder in dirList:
        if not os.path.exists(folder) and ignoreDirDoesNotExist:
            continue

        result = deleteDir(folder)
        if result:
            errMsgHeader = 'Error while deleting: %s\n' % folder
            newErrMsg = errMsgHeader + result + '\n'
            warn(newErrMsg)
            errMsg += newErrMsg

    return errMsg


def deleteDir(folder: str) -> str:
    '''Try hard to delete the input directory.

    When files in the directory are read-only, the initial deletion will fail but this
    function will retry after setting the files as writeable.

    Returns:
        * empty string when everything goes fine.
        * error description when something fails
    '''
    pth = pathlib.Path(folder)

    # check if .git directory is present and unhide it to help deletion
    try:
        _dirContent = list(pth.iterdir())
    except PermissionError:
        # nothing we can do with this directory
        return 'Permission error\n'

    local_error = []

    def rmtree_onerror(_function: Any, path: Any, _excinfo: Any) -> None:
        try:
            # deletion errors are usually because a file is readonly
            os.chmod(path, stat.S_IWRITE)
            os.unlink(path)
        except Exception as exc:
            # exception again !
            local_error.append('''On path %s
    %s''' % (str(path), str(exc)))
            warn(local_error[-1])

    dbg('deleteDirList() - Calling rmtree on %s' % str(pth))
    shutil.rmtree(pth, onerror=rmtree_onerror)

    if len(local_error) > 2:
        local_error = local_error[:2] + ['And more errors...\n']

    return '\n'.join(local_error)


def add_suffix_if_missing(fname: str, ext: str) -> str:
    '''Add the suffix if not already present in the string, and return it'''
    if fname.endswith(ext):
        return fname

    return fname + ext


def extractInt(s: str, intAtBeginning: bool = True) -> int:
    '''Parse the string s which begins by an integer and is followed by some other characters
    extract the integer part and convert it to integer

    If string is empty or contains no integer, just return 0

    This allows natural order sorting.
    '''
    idxStart = 0
    if not intAtBeginning:
        while idxStart < len(s) and not s[idxStart].isdigit():
            idxStart += 1

    idxEnd = idxStart
    while idxEnd < len(s) and s[idxEnd].isdigit():
        idxEnd += 1
    intPart = s[idxStart:idxEnd]
    if len(intPart) == 0:
        return 0
    return int(intPart)


def istrcmp(s1: str, s2: str) -> bool:
    '''Case-insensitive string compare'''
    return s1.lower() < s2.lower()


reGitAuthFailure = re.compile('^' + GIT_AUTH_FAILURE_MARKER, re.MULTILINE)
def hasGitAuthFailureMsg(gitlog: str) -> bool:
    '''Return true if logs contains a git authentication failure message'''
    return bool(reGitAuthFailure.search(gitlog))


GIT_CMD_WITH_NETWORK_AUTH = [ 'fetch', 'pull', 'push', 'ls-remote', 'clone']

def isGitCommandRequiringAuth(cmdline: Sequence[str]) -> bool:
    '''Return True if the git command line uses a command requiring network authentication'''
    if len(cmdline) < 2:
        return False

    git_cmd = cmdline[1]
    if cmdline[1] == '-C' and len(cmdline) >= 3:
        git_cmd = cmdline[3]

    if git_cmd in GIT_CMD_WITH_NETWORK_AUTH:
        return True

    return False



def treeWidgetFlatIterator(item_or_tree: Union[QTreeWidget, QTreeWidgetItem]) -> List[QTreeWidgetItem]:
    '''Iterates through either the QTreeWidget top-level items or through the items of the Item.

    This allows to use the same recursive function on a tree or an item.
    '''
    if isinstance(item_or_tree, QTreeWidget):
        return [cast(QTreeWidgetItem, item_or_tree.topLevelItem(idx)) for idx in range(item_or_tree.topLevelItemCount())]

    return [item_or_tree.child(idx) for idx in range(item_or_tree.childCount())]


def treeWidgetDeepIterator(treeWidget: QTreeWidget) -> Iterator[QTreeWidgetItem]:
    '''Returns all QTreeWidgetItems in a depth-first-search.
    '''
    def yieldChild(item: QTreeWidgetItem) -> Iterator[QTreeWidgetItem]:
        for itemChildIdx in range(item.childCount()):
            itemChild = item.child(itemChildIdx)
            yield itemChild
            yield from yieldChild(itemChild)

    for topItemIdx in range(treeWidget.topLevelItemCount()):
        topItem = treeWidget.topLevelItem(topItemIdx)
        assert topItem
        yield topItem
        yield from yieldChild(topItem)
def ignoreCppObjectDeletedError(method: Any) -> Any:
    '''Avoids triggering RuntimeError when accessing a method of a QTreeWigetItem

    The QTreeWidgetItem instance must also have a field `ignoreUpdates`

    '''

    def protected_method(self: Any, *args: Any, **kwargs: Any) -> Any:
        if self.ignoreUpdates:
            return

        try:
            self.text(0)
        except RuntimeError:
            warn('Trying to update an python item whose C++ object has already been deleted!')
            return
        return method(self, *args, **kwargs)

    return protected_method



