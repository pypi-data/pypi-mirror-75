from hitchbuild import HitchBuild
from path import Path
from pathquery import pathquery
from strictyaml import load, MapPattern, Str, Seq, Map, Bool, Optional
import jinja2
from copy import copy
from slugify import slugify
from dirtemplate import exceptions
from functools import partial


def render(template_file, functions, render_vars, base_templates):
    try:
        templates = base_templates if base_templates is not None else {}
        templates['template_to_render'] = template_file.text()
        environment = jinja2.Environment(
            loader=jinja2.DictLoader(templates)
        )
        environment.globals.update(functions)
        rendered = environment.get_template(
            'template_to_render'
        ).render(**render_vars)
    except jinja2.exceptions.TemplateSyntaxError as error:
        raise exceptions.TemplateLineError(
            template_file.abspath(),
            "Syntax error",
            error.lineno,
            error.message,
            error.source,
        )
    except jinja2.exceptions.UndefinedError as error:
        raise exceptions.TemplateError(
            template_file.abspath(),
            "Undefined var",
            error.message,
        )
    return rendered


def base_templates(src_path, template_folder):
    templates = {}
    if template_folder is not None:
        for filename in src_path.joinpath(template_folder).listdir():
            relpath = filename.relpath(src_path.joinpath(template_folder))
            templates[str(relpath)] = filename.text()
    return templates


class DirTemplate(HitchBuild):
    def __init__(self, src, dest):
        self._build_path = Path(dest).abspath()
        self._dest = self._build_path
        self.fingerprint_path = self._build_path / "fingerprint.txt"
        self._src_path = Path(src).abspath()
        self._vars = None
        self._functions = {}
        self._files = {}
        self._ignore_files = {}
        assert self._src_path.exists(), "{0} does not exist.".format(self._src_path)

    def with_vars(self, **variables):
        new_dirt = copy(self)
        new_dirt._vars = self.variable("variables", variables)
        return new_dirt

    def with_functions(self, **functions):
        def subdir(dest_path, subpath):
            return pathquery(dest_path.joinpath(subpath))

        new_dirt = copy(self)
        new_dirt._functions = {
            "subdir": partial(subdir, self._dest),
        }
        new_dirt._functions.update(functions)
        return new_dirt

    def with_files(self, **files):
        new_dirt = copy(self)
        new_dirt._files = files
        return new_dirt

    def ignore_files(self, *files):
        new_dirt = copy(self)
        new_dirt._ignore_files = [str(name) for name in files]
        return new_dirt

    @property
    def _render_vars(self):
        if self._vars is not None:
            return copy(self._vars.value)
        else:
            return {}

    def build(self):
        if self._build_path.exists():
            self._build_path.rmtree()
        self._build_path.mkdir()

        if self._src_path.joinpath("dirtemplate.yml").exists():
            config = load(
                self._src_path.joinpath("dirtemplate.yml").text(),
                Map({
                    Optional("base templates"): Str(),
                    "templated": Seq(
                        MapPattern(Str(), Map({
                            Optional("content"): Bool(),
                            Optional("filename"): Bool(),
                        }))
                    ),
                })
            ).data
        else:
            config = {"templated": []}

        src_paths = list(pathquery(self._src_path))

        templated_filenames = [
            list(template.keys())[0] for template in config['templated']
        ]

        if "base templates" in config:
            templated_filenames.extend(
                pathquery(
                    self._src_path.joinpath(config['base templates'])
                )
            )

        non_templated = []

        for srcpath in src_paths:
            relpath = srcpath.relpath(self._src_path)
            add = True

            if relpath in templated_filenames:
                add = False

            if relpath == "dirtemplate.yml":
                add = False

            if srcpath.isdir():
                add = False

            if "base templates" in config:
                if relpath.startswith(config['base templates']):
                    add = False

            if add:
                non_templated.append(relpath)

        for relpath in non_templated:
            dest_path = self._dest.joinpath(relpath)

            if not dest_path.dirname().exists():
                dest_path.dirname().makedirs()

            if str(relpath) not in self._ignore_files:
                self._src_path.joinpath(relpath).copy(dest_path)

        for template_configuration in config['templated']:
            for src_path in src_paths:
                if not src_path.isdir():
                    relpath = src_path.relpath(self._src_path)

                    if relpath in template_configuration.keys():
                        if 'filename' in template_configuration[relpath]:
                            slug = slugify(relpath, separator=u'_')

                            if slug in self._files.keys():
                                for filename, variables in self._files[slug].items():
                                    dest_path = self._dest.joinpath(filename)

                                    if not dest_path.dirname().exists():
                                        dest_path.dirname().makedirs()

                                    render_vars = {}

                                    for name, var in self._render_vars.items():
                                        render_vars[name] = var

                                    for name, filevar in variables.items():
                                        render_vars[name] = filevar

                                    render_vars['thisdir'] = pathquery(dest_path.dirname())

                                    dest_path.write_text(
                                        render(
                                            src_path,
                                            self._functions,
                                            render_vars,
                                            base_templates(
                                                self._src_path,
                                                config.get("base templates")
                                            )
                                        )
                                    )
                            else:
                                raise Exception((
                                    "{0} templated filename exists but not "
                                    "specified with with_files".format(relpath)
                                ))
                        else:
                            dest_path = self._dest.joinpath(relpath)

                            if not dest_path.dirname().exists():
                                dest_path.dirname().makedirs()

                            render_vars = copy(self._render_vars)
                            render_vars['thisdir'] = pathquery(dest_path.dirname())

                            if template_configuration[relpath]['content']:
                                dest_path.write_text(
                                    render(
                                        src_path,
                                        self._functions,
                                        render_vars,
                                        base_templates(
                                            self._src_path,
                                            config.get("base templates")
                                        ),
                                    )
                                )
        self.refingerprint()
