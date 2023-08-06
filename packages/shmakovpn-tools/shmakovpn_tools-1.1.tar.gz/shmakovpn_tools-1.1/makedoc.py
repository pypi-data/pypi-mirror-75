import os
SCRIPT_DIR: str = os.path.dirname(os.path.abspath(__file__))


def run_sphinx():
    docs_dir: str = os.path.join(SCRIPT_DIR, 'docs')
    docs_source_dir: str = os.path.join(docs_dir, 'source')
    build_dir: str = os.path.join(docs_dir, 'build')
    html_dir: str = os.path.join(build_dir, 'html')
    os.system('sphinx-build -b html "%s" "%s"' % (docs_source_dir, html_dir))
    print('__END__')


if __name__ == '__main__':
    run_sphinx()
