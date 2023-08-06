from django.urls import path

from . import contentviews

urlpatterns = [
    path('what_is_git_1', contentviews.WhatIsGitView.as_view(), name=f'{contentviews.WhatIsGitView.uid}_view'),
    path('start_git_init_1', contentviews.GitInitView.as_view(), name=f'{contentviews.GitInitView.uid}_view'),
    path('git_stages_1', contentviews.GitStagesView.as_view(), name=f'{contentviews.GitStagesView.uid}_view'),
    path('git_stage_changes_1', contentviews.GitStageChangesView.as_view(), name=f'{contentviews.GitStageChangesView.uid}_view'),
    path('git_remotes_concept_1', contentviews.GitRemotesConceptView.as_view(), name=f'{contentviews.GitRemotesConceptView.uid}_view'),
    path('gitignore_concept_1', contentviews.GitIgnoreConceptView.as_view(), name=f'{contentviews.GitIgnoreConceptView.uid}_view'),
    path('git_status_1', contentviews.GitStatusView.as_view(), name=f'{contentviews.GitStatusView.uid}_view'),
    path('git_push_1', contentviews.GitPushView.as_view(), name=f'{contentviews.GitPushView.uid}_view'),
    path('git_add_remote_1', contentviews.GitAddRemoteView.as_view(), name=f'{contentviews.GitAddRemoteView.uid}_view'),
    path('git_status_and_gitignore_1', contentviews.GitStatusAndGitIgnoreView.as_view(), name=f'{contentviews.GitStatusAndGitIgnoreView.uid}_view'),
    path('git_clone_1', contentviews.GitCloneView.as_view(), name=f'{contentviews.GitCloneView.uid}_view'),
    path('git_pull_basics_1', contentviews.GitPullBasicsView.as_view(), name=f'{contentviews.GitPullBasicsView.uid}_view'),
    path('git_log_1', contentviews.GitLogView.as_view(), name=f'{contentviews.GitLogView.uid}_view'),
]
