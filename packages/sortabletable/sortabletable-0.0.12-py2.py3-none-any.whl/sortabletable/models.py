import csv
from io import StringIO

from django.db import models
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _
from django.utils.formats import number_format
from django.contrib.postgres.fields import JSONField
from django.contrib.humanize.templatetags.humanize import intword

try:
    from cms.models.pluginmodel import CMSPlugin
except ImportError:
    CMSPlugin = None


class SortableTable(models.Model):
    title = models.CharField(_('title'), max_length=255)

    csv_data = models.TextField(_('CSV data'))
    settings = JSONField(_('settings'), default=dict, blank=True)

    class Meta:
        abstract = True
        verbose_name = _('Sortable Table')
        verbose_name_plural = _('Sortable Tables')

    def __str__(self):
        return self.title

    def save(self, **kwargs):
        if not self.settings and self.csv_data:
            reader = self.get_dict_reader()
            header_row = next(reader)
            self.settings = {'columns': [{'name': n} for n in header_row]}
        super().save(**kwargs)

    def get_dict_reader(self):
        return csv.reader(StringIO(self.csv_data))

    def get_table_context(self):
        reader = self.get_dict_reader()
        header_row = next(reader)
        header = self.get_header(header_row)
        footer = list(self.get_footer(reader))
        rows = (self.get_column(row) for row in reader)
        return {
            'header': header,
            'footer': footer,
            'rows': rows
        }

    def get_header(self, header_row):
        for i, col_name in enumerate(header_row):
            col_settings = self.get_col_settings(i)
            if col_settings.get('hide'):
                continue
            yield {
                'index': i,
                'name': mark_safe(col_settings.get('name', col_name)),
                'attrs': self.get_header_attrs(col_settings)
            }

    def get_footer(self, reader):
        footer_rows = self.settings.get('footer', 0)
        for i in range(0, footer_rows):
            yield self.get_column(next(reader))

    def get_header_attrs(self, col_settings):
        attrs = []
        if (not col_settings.get('text', False) and
                not col_settings.get('html', False)):
            attrs.append('data-sort-method="number"')
        if col_settings.get('default'):
            attrs.append('class="sort-default"')
        return mark_safe(' '.join(attrs))

    def get_col_settings(self, col_index):
        try:
            return self.settings['columns'][col_index]
        except IndexError:
            return {}

    def get_column(self, row):
        for i, col in enumerate(row):
            col_settings = self.get_col_settings(i)
            if col_settings.get('hide'):
                continue
            is_number = not (
                col_settings.get('html', False) or
                col_settings.get('text', False)
            )
            yield {
                'value': col or 0 if is_number else col,
                'is_number': is_number,
                'text': self.get_cell_text(col, col_settings)
            }

    def get_cell_text(self, col, col_settings):
        if col:
            return self.get_cell(col, col_settings)
        return ''

    def get_cell(self, value, col_settings):
        if col_settings.get('html', False):
            return mark_safe(value)
        if col_settings.get('text', False):
            return value
        try:
            value = float(value)
            if 'precision' in col_settings:
                value = round(value, col_settings['precision'])
            if col_settings.get('number_word'):
                formatted_value = intword(value)
            elif col_settings.get('number_format', True):
                formatted_value = number_format(
                    value,
                    decimal_pos=col_settings.get('decimals', None),
                    force_grouping=True
                )
            else:
                formatted_value = str(int(value))
            return mark_safe(u'{prefix}{value}{postfix}'.format(
                prefix=col_settings.get('prefix', ''),
                value=formatted_value,
                postfix=col_settings.get('postfix', '')
            ).strip())
        except ValueError:
            return value


if CMSPlugin is not None:
    class SortableTablePlugin(CMSPlugin, SortableTable):
        """
        CMS Plugin of SortableTable model
        """
