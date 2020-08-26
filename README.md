# md-to-adapt

This script can transform your MkDocs pages into components compatible with the AdaptLearning framework.

Usage:
`python main.py <md_dir> <adapt_dir> <co_names>`

- `md_dir`: Path to the MkDocs directory that includes an `mkdocs.yml` file at the root of the directory.
- `adapt_dir`: Path to the directory that contains the course created by the AdaptLearning framework.
- `co_names`: A list of names of all the different components (chapters) you need to include in the course. The names have to correspond to the different MkDocs pages configured in the `mkdocs.yml` file.
One can also select to include nested pages only.
 
