Title: First entry
Summary: Just as an example explaining how to write new posts.
Date: 2020-03-09 11:11 UTC
Tags: example
Comments: No
Private: No


Write in the directory `posts`  your posts in Markdown format with the
matadata header.

Example file:

```

    Title: Post title
    Summary: A _small_ summary for this *PynFact* entry. This summary
             is way two lines long, but it doesn't matter.
    Category: Miscellaneous
    Tags: tag1, tagtwo, tag three, Four
    Date: 2020-03-09 21:55
    Comments: No
    Private: No


    Here begins the *post*, in Markdown until the end of the file.
    Since the level-1 header `h1` is reserved for the title, all
    subsequent headers should begin in the second level.

    Second level header
    -------------------

    Or use the short version (`## Second level header`). It's also a
    valid Markdown syntax.

    There is **at least** one blank line between the metadata and the
    post entry, although for the sake of readabiliy, two blank lines are
    encouraged.

    Notes:

      * Only the "Title" and the "Date" are requiered fileds.

      * If you don't want comments for any post, turn off the comments
        engine by setting `comments: "no"` in the `config.yml` file.

      * The extension of each post **must** be `.md`, or else the file
        will be ignored.

      * A post set as "Private" still will be generated, but will not
        be referenced by any link.

      * Read the full documentation for more information.
```

Feel free to report bugs to <https://github.com/jacorbal/pynfact>.

