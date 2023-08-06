"""
Target selection methods determines which target should be used in
the event that multiple targets are generated within a logic adapter.
"""
import logging

logger = logging.getLogger(__name__)


def get_most_frequent_target(input_document, target_list, storage=None):
    """
    :param input_document: A document, that closely matches an input to the chat bot.
    :type input_document: Statement

    :param target_list: A list of document options to choose a target from.
    :type target_list: list

    :param storage: An instance of a storage adapter to allow the target selection
                    method to access other documents if needed.
    :type storage: StorageAdapter

    :return: The target document with the greatest number of occurrences.
    :rtype: Statement
    """
    matching_target = None
    occurrence_count = -1

    logger.info('Selecting target with greatest number of occurrences.')

    for document in target_list:
        count = len(list(storage.filter(
            text=document.text,
            in_target_to=input_document.text)
        ))

        # Keep the more common document
        if count >= occurrence_count:
            matching_target = document
            occurrence_count = count

    # Choose the most commonly occuring matching target
    return matching_target


def get_first_target(input_document, target_list, storage=None):
    """
    :param input_document: A document, that closely matches an input to the chat bot.
    :type input_document: Statement

    :param target_list: A list of document options to choose a target from.
    :type target_list: list

    :param storage: An instance of a storage adapter to allow the target selection
                    method to access other documents if needed.
    :type storage: StorageAdapter

    :return: Return the first document in the target list.
    :rtype: Statement
    """
    logger = logging.getLogger(__name__)
    logger.info('Selecting first target from list of {} options.'.format(
        len(target_list)
    ))
    return target_list[0]


def get_random_target(input_document, target_list, storage=None):
    """
    :param input_document: A document, that closely matches an input to the chat bot.
    :type input_document: Statement

    :param target_list: A list of document options to choose a target from.
    :type target_list: list

    :param storage: An instance of a storage adapter to allow the target selection
                    method to access other documents if needed.
    :type storage: StorageAdapter

    :return: Choose a random target from the selection.
    :rtype: Statement
    """
    from random import choice
    logger = logging.getLogger(__name__)
    logger.info('Selecting a target from list of {} options.'.format(
        len(target_list)
    ))
    return choice(target_list)
