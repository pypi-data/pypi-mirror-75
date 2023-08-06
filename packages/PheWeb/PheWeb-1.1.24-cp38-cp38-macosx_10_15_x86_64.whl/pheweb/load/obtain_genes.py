# This module finds gene data (wherever it must) and gets a copy in `generated-by-pheweb/`.

import argparse

allowed_genes = ['hg19', 'hg38']


def get_build(build_name):
    # TODO:
    #     our goal is to make generated-by-pheweb/sites/genes/genes.tsv or whatever
    #     first, try to cp from ~/.pheweb/cache/
    #      - gencode-29.gtf.gz is an alias for gencode-hg19-v29.gtf.gz
    #     then, try to download from ftp://share.sph.umich.edu/pheweb/ (and cp to ~/.pheweb/cache/ and also to generated-by-pheweb/sites
    #     then try downloading & parsing from the original source
    pass


def run(argv):
    parser = argparse.ArgumentParser(description="Download gene information to annotate variants")
    parser.add_argument('build', choices=allowed_genes,
                        help='Which build to get (downloads all if not specified)')
    args = parser.parse_args(argv)

    print(args.build)
