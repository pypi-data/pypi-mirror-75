# -*- coding: utf-8 -*-

from plone import api
from plone.registry import field
from plone.registry import Record
from plone.registry.interfaces import IRegistry
from zope.component import getUtility


def reload_content_types(context):
    """ Reload content types """
    portal_setup = api.portal.get_tool("portal_setup")
    portal_setup.runImportStepFromProfile("profile-ideabox.policy:default", "typeinfo")


def fix_comments_1001(context):
    from plone.app.discussion.interfaces import IConversation

    brains = api.content.find(
        context=api.portal.get(),
        total_comments={"query": [1, 1000], "range": "min:max"},
    )
    for brain in brains:
        obj = brain.getObject()
        conversation = IConversation(obj, None)
        for thread in conversation.getThreads():
            comment = thread["comment"]
            if comment.author_name == comment.author_email:
                user = api.user.get(username=comment.author_username)
                infos = [user.getProperty("first_name"), user.getProperty("last_name")]
                comment.author_name = " ".join([i for i in infos if i])


def to_1002(context):
    """
    Fix project_district index
    """
    catalog = api.portal.get_tool("portal_catalog")
    catalog.delIndex("project_district")
    portal_setup = api.portal.get_tool("portal_setup")
    portal_setup.runImportStepFromProfile("profile-ideabox.policy:default", "catalog")

    for brain in api.content.find(portal_type="Project"):
        brain.getObject().reindexObject(idxs=["project_district"])


def to_1003(context):
    portal_setup = api.portal.get_tool("portal_setup")
    portal_setup.runImportStepFromProfile("profile-ideabox.policy:default", "viewlets")


def to_1005(context):
    """ Add new tiles for priority action """
    registry = getUtility(IRegistry)
    records = registry.records

    tiles = {
        "plone.app.mosaic.app_tiles.priorityactions": {
            "name": "ideabox.policy.priority_actions",
            "label": "Latest priority actions",
            "category": "advanced",
            "tile_type": "app",
            "default_value": "",
            "read_only": False,
            "settings": True,
            "favorite": False,
            "rich_text": False,
            "weight": 10,
        },
        "plone.app.mosaic.app_tiles.random_priorityactions": {
            "name": "ideabox.policy.random_priority_actions",
            "label": "Random priority actions",
            "category": "advanced",
            "tile_type": "app",
            "default_value": "",
            "read_only": False,
            "settings": True,
            "favorite": False,
            "rich_text": False,
            "weight": 10,
        },
    }
    types = {
        "name": (field.TextLine, "Name"),
        "label": (field.TextLine, "Label"),
        "category": (field.TextLine, "Category"),
        "tile_type": (field.TextLine, "Type"),
        "default_value": (field.TextLine, "Default value"),
        "read_only": (field.Bool, "Read only"),
        "settings": (field.Bool, "Settings"),
        "favorite": (field.Bool, "Favorite"),
        "rich_text": (field.Bool, "Rich Text"),
        "weight": (field.Int, "Weight"),
    }

    for name, values in tiles.items():
        for key, value in values.items():
            r_key = "{0}.{1}".format(name, key)
            field_type, title = types[key]
            required = True
            if key == "default_value":
                required = False
            if r_key in records:
                continue
            record = Record(field_type(title=title, required=required), value=value)
            records[r_key] = record
