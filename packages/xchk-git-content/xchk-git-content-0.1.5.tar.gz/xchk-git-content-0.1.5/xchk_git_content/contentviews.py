from xchk_core.contentviews import ContentView
from xchk_core.strats import *
from xchk_regex_strategies import RegexCheck

class WhatIsGitView(ContentView):
     
    _accepting = ConjunctiveCheck([FileExistsCheck(),RegexCheck()])
    uid = 'what_is_git_1'
    template = 'xchk_git_content/what_is_git.html'
    strat = Strategy(refusing_check=DisjunctiveCheck([
                                      Negation(FileExistsCheck()),
                                      RegexCheck(model_name='incorrect_lang'),
                                      Negation(RegexCheck())]),
                     accepting_check=_accepting)

class GitInitView(ContentView):

    uid = 'start_git_init_1'
    template = 'xchk_git_content/start_git_init.html'
    strat = Strategy(refusing_check=TrueCheck(),accepting_check=Negation(TrueCheck()))

class GitStagesView(ContentView):

    uid = 'git_stages_1'
    template = 'xchk_git_content/git_stages.html'
    strat = Strategy(refusing_check=TrueCheck(),accepting_check=Negation(TrueCheck()))

class GitStageChangesView(ContentView):

    uid = 'git_stage_changes_1'
    template = 'xchk_git_content/git_stage_changes.html'
    strat = Strategy(refusing_check=TrueCheck(),accepting_check=Negation(TrueCheck()))

class GitRemotesConceptView(ContentView):

    uid = 'git_remotes_concept_1'
    template = 'xchk_git_content/git_remotes_concept.html'
    strat = Strategy(refusing_check=TrueCheck(),accepting_check=Negation(TrueCheck()))

class GitIgnoreConceptView(ContentView):

    uid = 'gitignore_concept_1'
    template = 'xchk_git_content/gitignore_concept.html'
    strat = Strategy(refusing_check=TrueCheck(),accepting_check=Negation(TrueCheck()))

class GitStatusView(ContentView):

    uid = 'git_status_1'
    template = 'xchk_git_content/git_status.html'
    strat = Strategy(refusing_check=TrueCheck(),accepting_check=Negation(TrueCheck()))

class GitPushView(ContentView):

    uid = 'git_push_1'
    template = 'xchk_git_content/git_push.html'
    strat = Strategy(refusing_check=TrueCheck(),accepting_check=Negation(TrueCheck()))

class GitAddRemoteView(ContentView):

    uid = 'git_add_remote_1'
    template = 'xchk_git_content/git_add_remote.html'
    strat = Strategy(refusing_check=TrueCheck(),accepting_check=Negation(TrueCheck()))

class GitStatusAndGitIgnoreView(ContentView):

    uid = 'git_status_and_gitignore_1'
    template = 'xchk_git_content/git_status_and_gitignore.html'
    strat = Strategy(refusing_check=TrueCheck(),accepting_check=Negation(TrueCheck()))
    
class GitCloneView(ContentView):

    uid = 'git_clone_1'
    template = 'xchk_git_content/git_clone.html'
    strat = Strategy(refusing_check=TrueCheck(),accepting_check=Negation(TrueCheck()))

class GitPullBasicsView(ContentView):

    uid = 'git_pull_basics_1'
    template = 'xchk_git_content/git_pull.html'
    strat = Strategy(refusing_check=TrueCheck(),accepting_check=Negation(TrueCheck()))
    
class GitLogView(ContentView):

    uid = 'git_log_1'
    template = 'xchk_git_content/git_log.html'
    strat = Strategy(refusing_check=TrueCheck(),accepting_check=Negation(TrueCheck()))
