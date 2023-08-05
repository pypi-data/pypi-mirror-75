from xchk import contentviews as basecv
from xchk.courses import Course
from .contentviews import *

course = Course('git',
                'Git',
                [(GitIgnoreConceptView,[GitStageChangesView]),
                 (GitStatusView,[GitStageChangesView]),
                 (GitPushView,[GitStageChangesView,GitRemotesConceptView]),
                 (GitAddRemoteView,[GitRemotesConceptView]),
                 (GitStatusAndGitIgnoreView,[GitStatusView,GitIgnoreConceptView]),
                 (GitPullBasicsView,[GitPushView]),
                 (GitLogView,[GitStageChangesView]),
                 (GitStageChangesView,[GitStagesView]),
                 (GitRemotesConceptView,[GitStagesView]),
                 (GitStagesView,[GitInitView]),
                 (GitInitView,[WhatIsGitView]),
                 (WhatIsGitView,[])],
                "git@github.com:v-nys/git-modeloplossingen.git")
