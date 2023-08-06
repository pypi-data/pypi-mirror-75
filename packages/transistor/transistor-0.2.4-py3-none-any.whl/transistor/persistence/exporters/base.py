# -*- coding: utf-8 -*-
"""
transistor.persistence.exporters.base
~~~~~~~~~~~~
This module implements classes that extract (serialize) the data inside
a BaseWorker from a SplashScraper.

Most of this module is heavily inspired or else copied from Scrapy.

:copyright: Original scrapy.exporters from scrapy==1.5.1 is
Copyright by it's authors and further changes or contributions here are
Copyright (C) 2018 by BOM Quote Limited.
:license: Original scrapy.exporters from scrapy==1.5.1 license is found at
https://github.com/scrapy/scrapy/archive/1.5.1.zip
and further changes or contributions here are licensed under The MIT
License, see LICENSE for more details.
~~~~~~
"""
from transistor.persistence.loader import ItemLoader

__all__ = ['BaseItemExporter']


class BaseItemExporter:
    """
    This is the base class for all Item Exporters. It provides
    support for common features used by all (concrete) Item Exporters,
    such as defining what fields to export, whether to export empty fields,
    or which encoding to use.

    These features can be configured through the constructor arguments
    which populate their respective instance attributes: fields_to_export,
    export_empty_fields, encoding, indent.

    Further, in Transistor, currently the Scrapy equivalent to
    `Item Loader` is built into this `BaseItemExporter`
    class, in the `write` method.

    An Item Exporter is BaseWorker tool to export the data from the
    SplashScraper object and pass the data into a new object which
    inherits from class:Item, called 'items' here.

    A spider which has completed a scrape job goes in. A container object
    encapsulating all the relevant data we want to further manipulate or
    save from the scrape job, comes out.

    So Transistor's BaseItemExporter.write() is roughly equivalent to
    Scrapy's ItemLoader.load_item() method.

    Transistor does not yet have an equivalent to Scrapy's concept of
    `Item Pipeline`, which uses multiple `Item Exporters` to group scraped
    items to different files according to the value of one of their fields.
    """

    def __init__(self, **kwargs):
        """
        Create an instance.
        :param kwargs: fields_to_export::list(): A list with the name
        of the fields that will be exported, or None if you want to export
        all fields. Defaults to None. Some exporters (like CsvItemExporter)
        respect the order of the fields defined in this attribute. Some
        exporters may require fields_to_export list in order to export
        the data properly when spiders return dicts (not Item instances).
        :param kwargs: export_empty_fields: Whether to include
        empty/unpopulated item fields in the exported data. Defaults to
        False. Some exporters (like CsvItemExporter) ignore this attribute
        and always export all empty fields. This option is ignored for
        dict items.
        :param kwargs: encoding: defaults to 'utf-8'. The encoding that
        will be used to encode unicode values. This only affects unicode
        values (which are always serialized to str using this encoding).
        Other value types are passed unchanged to the specific serialization
        library.
        :param kwargs: ident: Amount of spaces used to indent the output on
        each level. Defaults to 0. `indent=None` selects the most compact
        representation, all items in the same line with no indentation
        `indent<=0` each item on its own line, no indentation
        `indent>0` each item on its own line, indented with the provided
        numeric value
        """
        self._configure(kwargs)

    def _configure(self, options, dont_fail=False):
        """
        Configure the exporter by poping options from the ``options`` dict.
        If dont_fail is set, it won't raise an exception on unexpected options
        (useful for using with keyword arguments in subclasses constructors)
        :return:
        """
        self.encoding = options.pop('encoding', None)
        self.fields_to_export = options.pop('fields_to_export', None)
        self.export_empty_fields = options.pop('export_empty_fields', False)
        self.indent = options.pop('indent', None)
        if not dont_fail and options:
            raise TypeError("Unexpected options: %s" % ', '.join(options.keys()))

    def export_item(self, item):
        """
        Exports the given item. This method must be implemented in subclasses.
        :param item:
        """
        pass

    def serialize_field(self, field, name:str, value):
        """
        Return the serialized value for the given field. You can override
        this method (in your custom Item Exporters) if you want to control
        how a particular field or value will be serialized/exported.

        By default, this method looks for a serializer declared in the
        item field and returns the result of applying that serializer to
        the value. If no serializer is found, it returns the value unchanged.
        :param field:  (Field object or an empty dict) – the field being
        serialized. If a raw dict is being exported (not Item) field
        value is an empty dict.
        :param name:  the name of the field being serialized
        :param value: the value being serialized
        """
        return ItemLoader.serialize_field(field, name, value)

    def start_exporting(self):
        """
        Signal the beginning of the exporting process. Some exporters may
        use this to generate some required header (for example, the
        XmlItemExporter).
        :return:
        """
        pass

    def finish_exporting(self):
        """
        Signal the end of the exporting process. Some exporters may use
        this to generate some required footer (for example, the XmlItemExporter).
        :return:
        """
        pass

    def _get_serialized_fields(self, item, default_value=None, include_empty=None):
        """Return the fields to export as an iterable of tuples
        (name, serialized_value)
        """
        if include_empty is None:
            include_empty = self.export_empty_fields
        if self.fields_to_export is None:
            if include_empty and not isinstance(item, dict):
                field_iter = item.fields.keys()
            else:
                field_iter = item.keys()
        else:
            if include_empty:
                field_iter = self.fields_to_export
            else:
                field_iter = (x for x in self.fields_to_export if x in item)

        for field_name in field_iter:
            if field_name in item:
                field = {} if isinstance(item, dict) else item.fields[field_name]
                value = self.serialize_field(field, field_name, item[field_name])
            else:
                value = default_value

            yield field_name, value
