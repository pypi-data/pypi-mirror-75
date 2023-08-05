from azure.common import AzureMissingResourceHttpError, AzureConflictHttpError
from contextlib import redirect_stderr


def retry(max_retries=3, recalculate_length=True):
    def retry(f):
        """
        """
        def wrapper(*args, **kwargs):
            instance = args[0]
            result = None

            for i in range(max_retries):

                try:
                    result = f(*args, **kwargs)
                    break

                except AzureConflictHttpError as e:
                    if recalculate_length:
                        instance._update_length()
                except AzureMissingResourceHttpError as e:
                    with redirect_stderr(None) as err:
                        instance.create()

                except Exception as e:
                    raise e

            return result

        return wrapper

    return retry



def ensure_length(f):
    """
    """
    def wrapper(*args, **kwargs):
        instance = args[0]

        if instance._stored_len is None:
            instance._update_length()

        return f(*args, **kwargs)

    return wrapper
