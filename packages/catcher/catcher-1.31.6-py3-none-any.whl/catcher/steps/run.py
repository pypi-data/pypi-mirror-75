from catcher.steps.step import Step, update_variables, SkipException
from catcher.utils.logger import error, info, debug
from catcher.utils.misc import merge_two_dicts, fill_template_str, try_get_object
from catcher.steps.stop import StopException
from catcher.utils import logger


class Run(Step):
    """
    Run include on demand

    :Input:

    :include: include name. If contains dot - everything after dot will be considered as tag. In case of multiple dots
      the last one will be considered as tag.
    :variables: Variables to override. *Optional*

    :Examples:

    Use short form to run `sign_up`
    ::

        include:
            file: register_user.yaml
            as: sign_up
        steps:
            # .... some steps
            - run: sign_up
            # .... some steps

    Run `sign_up` with username overridden
    ::

        include:
            file: register_user.yaml
            as: sign_up
        steps:
            # .... some steps
            - run:
                include: sign_up
                variables:
                    username: test
            # .... some steps

    Include `sign_up` and run all steps with tag `register` from it. Use dot notation.
    ::

        include:
            file: register_and_login.yaml
            as: sign_up
        steps:
            - run:
                include: sign_up.register

    Include one.yaml from main and run only before tag of it. one.before includes two.yaml and runs only run_me tag.
    ::

        include:
            file: one.yaml
            as: one
        steps:
            - run: 'one.before'

        include:
            file: two.yaml
            as: run_me
        steps:
            - run:
                include: two.run_me
                tag: before
            - echo: {from: '{{ bar }}', to: after.output, tag: after}

        steps:
            - echo: {from: '1', to: foo.output, tag: run_me}
            - echo: {from: '2', to: baz.output, tag: two}
            - echo: {from: '3', to: bar.output, tag: three}
    """

    def __init__(self, ignore_errors=False, _body=None, run=None, include=None, tag=None, variables=None, **kwargs):
        super().__init__(**kwargs)
        self.variables = {} if variables is None else variables
        self.ignore_errors = ignore_errors
        self.include = include
        self.tag = tag
        if self.include is None:
            if run and isinstance(run, str):
                self.include = run
            else:
                self.include = _body

    @update_variables
    def action(self, includes: dict, variables: dict) -> dict:
        filled_vars = dict([(k, fill_template_str(v, variables)) for (k, v) in self.variables.items()])
        out = fill_template_str(self.include, variables)
        test, tag = get_tag(out)
        if test not in includes:
            error('No include registered for name ' + test)
            raise Exception('No include registered for name ' + test)
        include = includes[test]
        variables = merge_two_dicts(include.variables, merge_two_dicts(variables, filled_vars))
        include.variables = try_get_object(fill_template_str(variables, variables))
        try:
            info('Running {}.{}'.format(test, '' if tag is None else tag))
            logger.log_storage.nested_test_in()
            variables = include.run(tag=tag, raise_stop=True)
            logger.log_storage.nested_test_out()
        except SkipException:
            logger.log_storage.nested_test_out()
            debug('Include ignored')
            return variables
        except StopException as e:
            logger.log_storage.nested_test_out()
            raise e
        except Exception as e:
            logger.log_storage.nested_test_out()
            if not self.ignore_errors:
                raise Exception('Step run ' + test + ' failed: ' + str(e))
        return variables


def get_tag(include: str) -> str or None:
    if '.' in include:
        splitted = include.split('.')
        return '.'.join(include.split('.')[:-1]), splitted[-1:][0]
    else:
        return include, None
