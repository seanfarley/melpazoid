import configparser
    recipe: str,  # e.g. of the form (my-package :repo ...)
    for ii, file in enumerate(files):
        target = os.path.basename(file) if file.endswith('.el') else file
        target = os.path.join('_elisp', target)
        os.makedirs(os.path.join('_elisp', os.path.dirname(file)), exist_ok=True)
        subprocess.check_output(['mv', os.path.join(elisp_dir, file), target])
        files[ii] = target
    print_related_packages(recipe)
    print_packaging(recipe, files, pr_data, clone_address)
    """Return (and optionally set) the current return code.
    """Validate whether the recipe looks correct.
    >>> validate_recipe('(abc :repo "xyz" :fetcher github) ; abc recipe!')
    tokenized_recipe = _tokenize_expression(recipe)
def check_containerized_build(package_name: str):
    files = run_build_script(
        f"""
        (require 'package-build)
        (send-string-to-terminal
          (let* ((package-build-working-dir "{os.path.dirname(elisp_dir)}")
                 (rcp {_recipe_struct_elisp(recipe)}))
            (mapconcat (lambda (x) (format "%s" x))
                       (package-build--expand-source-file-list rcp) "\n")))
        """
    ).split('\n')
    return [file for file in files if os.path.exists(os.path.join(elisp_dir, file))]
@functools.lru_cache()
def _tokenize_expression(expression: str) -> list:
    """Hacky function to turn an elisp expression into a list of tokens.
    >>> _tokenize_expression('(shx :repo "riscy/xyz" :fetcher github) ; comment')
        with open(os.path.join(tmpdir, 'scratch'), 'w') as scratch:
            scratch.write(expression)
        parsed_expression = run_build_script(
            f"""
            (send-string-to-terminal
              (format "%S" (with-temp-buffer (insert-file-contents "{scratch.name}")
                                             (read (current-buffer)))))
            """
        )
    parsed_expression = parsed_expression.replace('(', ' ( ')
    parsed_expression = parsed_expression.replace(')', ' ) ')
    tokenized_expression: list = parsed_expression.split()
    return tokenized_expression
    """Return the package's name, based on the recipe.
    return _tokenize_expression(recipe)[1]
def _main_file(files: list, recipe: str) -> str:
    """Figure out the 'main' file of the recipe, per MELPA convention.
            for el in sorted(files)
def _write_requirements(files: list, recipe: str):
        for req in _requirements(files, recipe):
            if req == 'org':
                # TODO: is there a cleaner way to install a recent version of org?!
                requirements_el.write(
                    "(package-install (cadr (assq 'org package-archive-contents)))"
                )
            elif req != 'emacs':
def _requirements(files: list, recipe: str = None, with_versions: bool = False) -> set:
        main_file = _main_file(files, recipe)
            files = [main_file]
    for filename in files:
    """Hacky function to pull the requirements out of a -pkg.el file.
    reqs = ' '.join(_tokenize_expression(reqs))
    """Hacky function to pull the requirements out of an elisp file.
def check_license(files: list, elisp_dir: str, clone_address: str = None):
        repo_licensed = _check_repo_for_license(elisp_dir)
    individual_files_licensed = _check_files_for_license_boilerplate(files)
    """Use the GitHub API to check for a license."""
def _check_repo_for_license(elisp_dir: str) -> bool:
    _fail('- Please add a LICENSE or COPYING file to the repository')
def _check_files_for_license_boilerplate(files: list) -> bool:
    """Check a list of elisp files for license boilerplate."""
    for file in files:
        if not file.endswith('.el') or file.endswith('-pkg.el'):
        license_ = _check_file_for_license_boilerplate(file)
        basename = os.path.basename(file)
            _fail(f"- {basename} has no detectable license boilerplate")
def _check_file_for_license_boilerplate(file: str) -> str:
    """Check an elisp file for some license boilerplate."""
    licenses = [
        ('GPL', r'GNU.* General Public License'),
        ('ISC', r'Permission to use, copy, modify, and/or'),
        ('MIT', r'Permission is hereby granted, free of charge, to any person'),
        ('MIT', r'SPDX-License-Identifier: MIT'),
        ('WTFPL', r'SPDX-License-Identifier: WTFPL'),
        ('GPL', r'SPDX-License-Identifier: GPL-3.0-'),  # <-or-later, -only>
        ('Unlicense', 'This is free and unencumbered software released into'),
        ('Apache 2.0', 'Licensed under the Apache License, Version 2.0'),
        ('BSD 3-Clause', 'Redistribution and use in source and binary forms'),
    ]
    for license_key, license_txt in licenses:
            subprocess.check_output(['grep', '-i', license_txt, file])
def print_packaging(
    recipe: str, files: list, pr_data: dict = None, clone_address: str = None
):
    _note('\n### Package details ###\n', CLR_INFO)
    _print_recipe(files, recipe)
    _print_requirements(files, recipe)
    if pr_data and clone_address:
        print(f"- PR by {pr_data['user']['login']}: {clone_address}")
        if pr_data['user']['login'].lower() not in clone_address.lower():
            _note("  - NOTE: Repo and recipe owner don't match", CLR_WARN)
    _print_package_files(files)


def _print_recipe(files: list, recipe: str):
    print(f"```elisp\n{recipe}\n```")
    if ':files' in recipe and ':defaults' not in recipe:
        _note('- Prefer the default recipe, especially for small packages', CLR_WARN)
    if ':branch' in recipe:
        _note('- Only specify :branch in unusual cases', CLR_WARN)
    if not _main_file(files, recipe):
        _fail(f"- No .el file matches the name '{_package_name(recipe)}'!")


def _print_requirements(files: list, recipe: str):
    """Print the list of Package-Requires from the 'main' file.
    Report on any mismatches between this file and other files, since the ones
    in the other files will be ignored.
    """
    main_requirements = _requirements(files, recipe, with_versions=True)
    print(', '.join(req for req in main_requirements) if main_requirements else 'n/a')
    for file in files:
        file_requirements = set(_requirements([file], with_versions=True))
        if file_requirements and file_requirements != main_requirements:
            _fail(
                f"  - Package-Requires mismatch between {os.path.basename(file)} and "
                f"{os.path.basename(_main_file(files, recipe))}!"
            )


def _print_package_files(files: list):
    for file in files:
        if os.path.isdir(file):
            print(f"- {CLR_ULINE}{file}{CLR_OFF} -- directory")
        with open(file) as stream:
            f"- {CLR_ULINE}{file}{CLR_OFF}"
            f" ({_check_file_for_license_boilerplate(file) or 'unknown license'})"
            + (f" -- {header}" if header else "")
        if file.endswith('-pkg.el'):
    """Print list of potentially related packages."""
    package_name = _package_name(recipe)
    shorter_name = package_name[:-5] if package_name.endswith('-mode') else package_name
    known_packages = _known_packages()
    known_names = [name for name in known_packages if shorter_name in name]
    if not known_names:
        return
    _note('\n### Similarly named packages ###\n', CLR_INFO)
    for name in known_names[:10]:
        print(f"- {name} {known_packages[name]}")
    if package_name in known_packages:
        _fail(f"- {package_name} {known_packages[package_name]} is in direct conflict")
def _known_packages() -> dict:
    melpa_packages = {
        package: f"https://melpa.org/#/{package}"
    epkgs = 'https://raw.githubusercontent.com/emacsmirror/epkgs/master/.gitmodules'
    epkgs_parser = configparser.ConfigParser()
    epkgs_parser.read_string(requests.get(epkgs).text)
    epkgs_packages = {
        epkg.split('"')[1]: epkgs_parser[epkg]['url']
        for epkg in epkgs_parser
        if epkg != 'DEFAULT'
    }
    return {**epkgs_packages, **melpa_packages}
    return_code(0)
        # package-build prefers the directory to be named after the package:
        elisp_dir = os.path.join(elisp_dir, _package_name(recipe))
        clone_address = _clone_address(recipe)
        if _clone(clone_address, into=elisp_dir, branch=_branch(recipe), scm=scm):
            run_checks(recipe, elisp_dir, clone_address)
def _clone(repo: str, into: str, branch: str = None, scm: str = 'git') -> bool:
    """Try to clone the repository; return whether we succeeded."""
    print(f"Checking out {repo}")
        _fail(f"Unable to locate {repo}")
        return False
    if scm == 'git':
        # If a package's repository doesn't use the master branch, then the
        # MELPA recipe must specify the branch using the :branch keyword
        # https://github.com/melpa/melpa/pull/6712
        options = ['--branch', branch if branch else 'master']
        options += ['--depth', '1', '--single-branch']
    elif scm == 'hg':
        options = ['--branch', branch] if branch else []
        _fail(f"Unrecognized SCM: {scm}")
        return False
    git_command = [scm, 'clone', *options, repo, into]
    result = subprocess.run(git_command, stderr=subprocess.STDOUT)
    if result.returncode != 0:
        _fail('Unable to clone this (prefer "master" as the default branch)')
        return False
    return True
    """Determine the source code manager used (mercurial or git).
    tokenized_recipe = _tokenize_expression(recipe)
    """Return the recipe's branch if available, else the empty string.
    tokenized_recipe = _tokenize_expression(recipe)
    return_code(0)
        _fail(f"{pr_url} does not appear to be a MELPA PR")
    filename, recipe = _filename_and_recipe(pr_data['diff_url'])
    if filename != _package_name(recipe):
        _fail(f"Filename '{filename}' does not match '{_package_name(recipe)}'")
        return
    clone_address: str = _clone_address(recipe)
        # package-build prefers the directory to be named after the package:
        elisp_dir = os.path.join(elisp_dir, _package_name(recipe))
        if _clone(clone_address, into=elisp_dir, branch=_branch(recipe)):
            run_checks(recipe, elisp_dir, clone_address, pr_data)
def _filename_and_recipe(pr_data_diff_url: str) -> Tuple[str, str]:
    diff_text = requests.get(pr_data_diff_url).text
    if (
        'new file mode' not in diff_text
        or 'a/recipes' not in diff_text
        or 'b/recipes' not in diff_text
    ):
        _note('This does not appear to add a new recipe', CLR_WARN)
        return '', ''
        with subprocess.Popen(
            ['patch', '-s', '-o', os.path.join(tmpdir, 'patch')], stdin=subprocess.PIPE,
        ) as process:
            process.stdin.write(diff_text.encode())
        with open(os.path.join(tmpdir, 'patch')) as patch_file:
            basename = diff_text.split('\n')[0].split('/')[-1]
            return basename, patch_file.read().strip()


def _clone_address(recipe: str) -> str:
    """Fetch the upstream repository URL for the recipe.
    >>> _clone_address('(shx :repo "riscy/shx-for-emacs" :fetcher github)')
    >>> _clone_address('(pmdm :fetcher hg :url "https://hg.serna.eu/emacs/pmdm")')
    return run_build_script(
        f"""
        (require 'package-recipe)
        (send-string-to-terminal
          (package-recipe--upstream-url {_recipe_struct_elisp(recipe)}))
        """
    )


@functools.lru_cache()
def _recipe_struct_elisp(recipe: str) -> str:
    """Turn the recipe into a serialized 'package-recipe' object."""
    name = _package_name(recipe)
        with open(os.path.join(tmpdir, name), 'w') as file:
            file.write(recipe)
        return run_build_script(
            f"""
            (require 'package-recipe)
            (let ((package-build-recipes-dir "{tmpdir}"))
              (send-string-to-terminal (format "%S" (package-recipe-lookup "{name}"))))
            """
        )


def run_build_script(script: str) -> str:
    """Run an elisp script in a package-build context.
    >>> run_build_script('(send-string-to-terminal "Hello world")')
    'Hello world'
    """
    stderr = subprocess.STDERR if DEBUG else subprocess.DEVNULL
    with tempfile.TemporaryDirectory() as tmpdir:
        for filename, content in _package_build_files().items():
            with open(os.path.join(tmpdir, filename), 'w') as file:
                file.write(content)
        script = f"""(progn (add-to-list 'load-path "{tmpdir}") {script})"""
        result = subprocess.check_output(
            ['emacs', '--batch', '--eval', script], stderr=stderr
        )
        return result.decode().strip()


@functools.lru_cache()
def _package_build_files() -> dict:
    """Grab the required package-build files from the MELPA repo."""
    return {
        filename: requests.get(
            'https://raw.githubusercontent.com/melpa/melpa/master/'
            f'package-build/{filename}'
        ).text
        for filename in [
            'package-build-badges.el',
            'package-build.el',
            'package-recipe-mode.el',
            'package-recipe.el',
        ]
    }
        if return_code() != 0:
            _fail('*** This PR failed')
        with open(os.environ['RECIPE_FILE'], 'r') as file:
            check_recipe(file.read())