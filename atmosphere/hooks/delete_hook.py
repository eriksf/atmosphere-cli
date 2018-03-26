import logging
from six.moves import input

from cliff.hooks import CommandHook


class DeleteHook(CommandHook):
    """
    This hook prompts the user to confirm whether or not they
    want to perform the delete action. A boolean flag called
    'delete' is added to the parsed_args Namespace which can
    be checked in the command's 'take_action' method.
    """

    log = logging.getLogger(__name__)

    def get_parser(self, parser):
        pass

    def after(self, parsed_args, return_code):
        pass

    def query_yes_no(self, question, default="no"):
        valid = {"yes": True,
                 "y": True,
                 "no": False,
                 "n": False}
        if default is None:
            prompt = " [y/n] "
        elif default == "yes":
            prompt = " [Y/n] "
        elif default == "no":
            prompt = " [y/N] "
        else:
            raise ValueError("invalid default answer: '%s'" % default)

        while True:
            self.cmd.app.stdout.write(question + prompt)
            choice = input().lower()
            if default is not None and choice == '':
                return valid[default]
            elif choice in valid:
                return valid[choice]
            else:
                self.cmd.app.stdout.write("Please respond with 'yes' or 'no' ('y' or 'n').\n")

    def get_epilog(self):
        return 'User will be prompted to confirm delete action unless passing --force option.'

    def before(self, parsed_args):
        if not parsed_args.force:
            confirm = self.query_yes_no("Are you sure you want to delete this item?")
            if confirm:
                parsed_args.delete = True
            else:
                parsed_args.delete = False
        else:
            parsed_args.delete = True
