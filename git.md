# git code snippet

## Fix a bad commit infos

This trick works when you are alone on your repo. It can be dangerous when many peoples works on the same repo.

Do:

```bash
git reset --soft HEAD^
```

Until before the bad commit.

Then do:

```bash
git push --force origin master
```

The commit is now removed from github.

Next, move on top again to have bad commit in your repo:

```bash
git reset --soft HEAD
```

Then do:

```bash
git filter-branch --commit-filter 'if [ "$GIT_AUTHOR_EMAIL" = "bad.address@mail.com" ];
  then export GIT_AUTHOR_EMAIL=good.address@mail.com; export GIT_COMMITTER_NAME="$GIT_AUTHOR_NAME"; export GIT_COMMITTER_EMAIL="$GIT_AUTHOR_EMAIL";
  fi; git commit-tree "$@"'
```

This forks the branch with proper commits.

If you got an error:

```
A previous backup already exists in refs/original/
```

You can do:


```bash
git update-ref -d refs/original/refs/heads/master
```

And try the `git filter-branch` again.

Once your master has proper commits, you can do:

```bash
git push --force origin master
```

To put everything nice in github.

Another option can be found [here](https://stackoverflow.com/questions/750172/change-the-author-and-committer-name-and-e-mail-of-multiple-commits-in-git).
