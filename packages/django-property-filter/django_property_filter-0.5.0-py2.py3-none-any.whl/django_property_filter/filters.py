"""Filters to extend Django-FIlter filters to support property filtering."""

import datetime
import logging

from django.utils import timezone

from django_filters.filters import (
    AllValuesFilter,
    AllValuesMultipleFilter,
    BooleanFilter,
    CharFilter,
    ChoiceFilter,
    DateFilter,
    DateFromToRangeFilter,
    DateRangeFilter,
    DateTimeFilter,
    DateTimeFromToRangeFilter,
    DurationFilter,
    IsoDateTimeFilter,
    IsoDateTimeFromToRangeFilter,
    LookupChoiceFilter,
    MultipleChoiceFilter,
    NumberFilter,
    RangeFilter,
    TimeFilter,
    TimeRangeFilter,
    TypedChoiceFilter,
    TypedMultipleChoiceFilter,
    UUIDFilter,
)

from django_property_filter.utils import (
    get_value_for_db_field,
    compare_by_lookup_expression
)

logger = logging.getLogger(__name__)


class PropertyBaseFilterMixin():
    """Mixin for Property Filters."""

    supported_lookups = [
        'exact', 'iexact', 'contains', 'icontains', 'gt', 'gte',
        'lt', 'lte', 'startswith', 'istartswith', 'endswith', 'iendswith',
    ]

    def __init__(self, *args, **kwargs):
        """Shared Constructor for Property Filters."""
        label = kwargs.get('label')
        lookup_expr = kwargs.get('lookup_expr')

        # Use a different field name for properties to avoid conflicts with property_filter implementation
        self.property_fld_name = kwargs.get('field_name')
        kwargs['field_name'] = None

        # Set the default lookup if none is specified
        if lookup_expr is None:
            lookup_expr = self.supported_lookups[0]
            kwargs['lookup_expr'] = lookup_expr

        # Set the Label
        if label is None:
            label = F'{self.property_fld_name} [{lookup_expr}]'
            kwargs['label'] = label

        super().__init__(*args, **kwargs)

        # Verify lookup after initializing since django-filter can set it as well
        self.verify_lookup(lookup_expr)

    def filter(self, queryset, value):
        """Filter the queryset by property."""
        # Carefull, a filter value of 0 will be Valid so can't just do 'if value:'
        if value is not None and value != '':
            wanted_ids = set()
            for obj in queryset:
                property_value = get_value_for_db_field(obj, self.property_fld_name)
                if self._compare_lookup_with_qs_entry(self.lookup_expr, value, property_value):
                    wanted_ids.add(obj.pk)
            return queryset.filter(pk__in=wanted_ids)

        return queryset

    def verify_lookup(self, lookup_expr):
        """Check if lookup_expr is supported."""
        if lookup_expr not in self.supported_lookups:
            raise ValueError(F'Lookup "{lookup_expr}" not supported"')

    def _compare_lookup_with_qs_entry(self, lookup_expr, lookup_value, property_value):  # pylint: disable=no-self-use
        """Compare the lookup value with the property value."""
        result = False

        # Convert any of the Lookups, e.g. for Range with only 1 value
        lookup_expr, lookup_value, property_value = self._lookup_convertion(
            lookup_expr, lookup_value, property_value)

        try:
            result = compare_by_lookup_expression(lookup_expr, lookup_value, property_value)
        except (TypeError) as error:
            logging.info(F'Error during comparing property value "{property_value}" with'
                         F'filter value "{lookup_value}" with error: "{error}"')

        return result

    def _lookup_convertion(self, lookup_expr, lookup_value, property_value):  # pylint: disable=no-self-use
        return lookup_expr, lookup_value, property_value


class ChoiceConvertionMixin():  # pylint: disable=too-few-public-methods
    """Provide Comparison Convertion for Choice Filters."""

    def _compare_lookup_with_qs_entry(self, lookup_expr, lookup_value, property_value):

        new_lookup_value = lookup_value
        new_property_value = property_value

        if type(lookup_value) != type(property_value):  # pylint: disable=unidiomatic-typecheck
            try:
                convert_lookup_value = type(property_value)(lookup_value)
            except (ValueError, TypeError):
                pass
            else:
                new_lookup_value = convert_lookup_value

        return super()._compare_lookup_with_qs_entry(lookup_expr, new_lookup_value, new_property_value)


class MultipleChoiceFilterMixin():  # pylint: disable=too-few-public-methods
    """Provide filtering for multiple choice FIlter."""

    def filter(self, queryset, value):
        """Filter Multiple Choice Property Values."""
        # If no or empty qs there is nothing to filter, leave the qs untouched
        if not queryset or not value:
            return queryset

        result_qs = None

        for sub_value in value:
            sub_result_qs = super().filter(queryset, sub_value)

            if self.conjoined:
                if result_qs is None:
                    # For 'AND' start from the first qs found
                    result_qs = sub_result_qs

                if sub_result_qs:
                    result_qs = result_qs & sub_result_qs
                else:  # Result QS empty, 'AND' will always be False, return empty qs
                    result_qs = sub_result_qs
            else:
                if result_qs is None:
                    # For 'OR' start from an empty qs
                    result_qs = self.model.objects.none()  # pylint: disable=no-member

                result_qs = result_qs | sub_result_qs

        return result_qs if result_qs is not None else self.model.objects.none()


class RangeFilterFilteringMixin():  # pylint: disable=too-few-public-methods
    """Provide filtering for Range Filters."""

    def _lookup_convertion(self, lookup_expr, lookup_value, property_value):  # pylint: disable=no-self-use

        if lookup_expr == 'range':
            if lookup_value.start is None:
                lookup_expr = 'lte'
                lookup_value = lookup_value.stop
            elif lookup_value.stop is None:
                lookup_expr = 'gte'
                lookup_value = lookup_value.start

        return lookup_expr, lookup_value, property_value


class PropertyAllValuesFilter(ChoiceConvertionMixin, PropertyBaseFilterMixin, AllValuesFilter):
    """Adding Property Support to AllValuesFilter."""

    @property
    def field(self):
        """Filed Property to setup default choices."""
        queryset = self.model._default_manager.distinct()  # pylint: disable=no-member,protected-access

        value_list = []
        for obj in queryset:
            property_value = get_value_for_db_field(obj, self.property_fld_name)
            value_list.append(property_value)

        value_list = sorted(value_list, key=lambda x: (x is None, x))

        self.extra['choices'] = [(prop, str(prop)) for prop in value_list]

        # Need to Call parent's Parent since our Parent uses DB fields directly
        return super(AllValuesFilter, self).field


class PropertyAllValuesMultipleFilter(
        ChoiceConvertionMixin, MultipleChoiceFilterMixin, PropertyBaseFilterMixin, AllValuesMultipleFilter):
    """Adding Property Support to AllValuesFilter."""

    @property
    def field(self):
        """Filed Property to setup default choices."""
        queryset = self.model._default_manager.distinct()  # pylint: disable=no-member,protected-access

        value_list = []
        for obj in queryset:
            property_value = get_value_for_db_field(obj, self.property_fld_name)
            value_list.append(property_value)

        value_list = sorted(set(value_list), key=lambda x: (x is None, x))

        self.extra['choices'] = [(prop, str(prop)) for prop in value_list]

        # Need to Call parent's Parent since our Parent uses DB fields directly
        return super(AllValuesMultipleFilter, self).field


class PropertyBooleanFilter(PropertyBaseFilterMixin, BooleanFilter):
    """Adding Property Support to BooleanFilter."""

    supported_lookups = ['exact', 'isnull']


class PropertyCharFilter(PropertyBaseFilterMixin, CharFilter):
    """Adding Property Support to BooleanFilter."""


class PropertyChoiceFilter(ChoiceConvertionMixin, PropertyBaseFilterMixin, ChoiceFilter):
    """Adding Property Support to ChoiceFilter."""


class PropertyDateFilter(PropertyBaseFilterMixin, DateFilter):
    """Adding Property Support to DateFilter."""

    supported_lookups = ['exact', 'gt', 'gte', 'lt', 'lte']


class PropertyDateFromToRangeFilter(RangeFilterFilteringMixin, PropertyBaseFilterMixin, DateFromToRangeFilter):
    """Adding Property Support to DateFromToRangeFilter."""

    supported_lookups = ['range']

    def _compare_lookup_with_qs_entry(self, lookup_expr, lookup_value, property_value):
        """Convert all datetime to date and then compare."""
        # Convert the Lookup Value if needed
        new_lookup_value = lookup_value
        if lookup_value:
            start = lookup_value.start
            stop = lookup_value.stop

            if start and isinstance(start, datetime.datetime):
                start = start.date()
            if stop and isinstance(stop, datetime.datetime):
                stop = stop.date()

            new_lookup_value = slice(start, stop)

        # Convert the Property Value if needed
        new_property_value = property_value
        if new_property_value and isinstance(new_property_value, datetime.datetime):
            new_property_value = new_property_value.date()

        return super()._compare_lookup_with_qs_entry(lookup_expr, new_lookup_value, new_property_value)


class PropertyDateRangeFilter(PropertyBaseFilterMixin, DateRangeFilter):
    """Adding Property Support to DateRangeFilter."""

    supported_lookups = ['exact']

    def _compare_lookup_with_qs_entry(self, lookup_expr, lookup_value, property_value):

        new_lookup_exp = lookup_expr
        new_lookup_value = lookup_value
        new_property_value = property_value

        # Convert DateTime values to Date only
        if property_value and isinstance(property_value, datetime.datetime):
            new_property_value = property_value.date()

        # Convert our Custom Expression and Value to Supported the Hardcoded Expressions
        today_datetime = timezone.now()

        if lookup_value == 'today':
            new_lookup_value = today_datetime.date()
        elif lookup_value == 'yesterday':
            new_lookup_value = today_datetime.date() - datetime.timedelta(days=1)
        elif lookup_value == 'week':
            new_lookup_exp = 'range'
            new_lookup_value = slice(
                today_datetime.date() - datetime.timedelta(days=7),
                today_datetime.date()
            )
        elif lookup_value == 'month':
            new_lookup_exp = 'exact'
            new_lookup_value = today_datetime.date().month
            new_property_value = property_value.month
        elif lookup_value == 'year':
            new_lookup_exp = 'exact'
            new_lookup_value = today_datetime.date().year
            new_property_value = property_value.year

        return super()._compare_lookup_with_qs_entry(new_lookup_exp, new_lookup_value, new_property_value)


class PropertyDateTimeFilter(PropertyBaseFilterMixin, DateTimeFilter):
    """Adding Property Support to DateTimeFilter."""

    supported_lookups = ['exact', 'gt', 'gte', 'lt', 'lte']


class PropertyDateTimeFromToRangeFilter(RangeFilterFilteringMixin, PropertyBaseFilterMixin, DateTimeFromToRangeFilter):
    """Adding Property Support to DateTimeFromToRangeFilter."""

    supported_lookups = ['range']


class PropertyDurationFilter(PropertyBaseFilterMixin, DurationFilter):
    """Adding Property Support to DurationFilter."""

    supported_lookups = ['exact', 'gt', 'gte', 'lt', 'lte']


class PropertyIsoDateTimeFilter(PropertyBaseFilterMixin, IsoDateTimeFilter):
    """Adding Property Support to IsoDateTimeFilter."""

    supported_lookups = ['exact', 'gt', 'gte', 'lt', 'lte']


class PropertyIsoDateTimeFromToRangeFilter(
        RangeFilterFilteringMixin, PropertyBaseFilterMixin, IsoDateTimeFromToRangeFilter):
    """Adding Property Support to IsoDateTimeFromToRangeFilter."""

    supported_lookups = ['range']


class PropertyLookupChoiceFilter(ChoiceConvertionMixin, PropertyBaseFilterMixin, LookupChoiceFilter):
    """Adding Property Support to LookupChoiceFilter."""

    def get_lookup_choices(self):
        """Get th Lookup choices in the correct format."""
        lookups = self.lookup_choices
        if lookups is None:
            lookups = self.supported_lookups

        lookup_tup_list = [self.normalize_lookup(lookup) for lookup in lookups]

        for lookup_expr, _ in lookup_tup_list:
            self.verify_lookup(lookup_expr)

        return lookup_tup_list

    def filter(self, queryset, value):
        """Perform the custom filtering."""
        if not value:
            return super().filter(queryset, None)

        self.lookup_expr = value.lookup_expr
        return super().filter(queryset, value.value)


class PropertyMultipleChoiceFilter(
        ChoiceConvertionMixin, MultipleChoiceFilterMixin, PropertyBaseFilterMixin, MultipleChoiceFilter):
    """Adding Property Support to MultipleChoiceFilter."""


class PropertyNumberFilter(PropertyBaseFilterMixin, NumberFilter):
    """Adding Property Support to NumberFilter."""

    supported_lookups = [
        'exact', 'contains', 'gt', 'gte', 'lt', 'lte', 'startswith', 'endswith']


class PropertyRangeFilter(RangeFilterFilteringMixin, PropertyBaseFilterMixin, RangeFilter):
    """Adding Property Support to RangeFilter."""

    supported_lookups = ['range']


class PropertyTimeFilter(PropertyBaseFilterMixin, TimeFilter):
    """Adding Property Support to TimeFilter."""

    supported_lookups = ['exact', 'gt', 'gte', 'lt', 'lte']


class PropertyTimeRangeFilter(RangeFilterFilteringMixin, PropertyBaseFilterMixin, TimeRangeFilter):
    """Adding Property Support to TimeRangeFilter."""

    supported_lookups = ['range']


class PropertyTypedChoiceFilter(ChoiceConvertionMixin, PropertyBaseFilterMixin, TypedChoiceFilter):
    """Adding Property Support to TypedChoiceFilter."""


class PropertyTypedMultipleChoiceFilter(
        ChoiceConvertionMixin, MultipleChoiceFilterMixin, PropertyBaseFilterMixin, TypedMultipleChoiceFilter):
    """Adding Property Support to TypedMultipleChoiceFilter."""


class PropertyUUIDFilter(PropertyBaseFilterMixin, UUIDFilter):
    """Adding Property Support to UUIDFilter."""

    supported_lookups = ['exact']


EXPLICIT_ONLY_FILTERS = [
    PropertyChoiceFilter,
    PropertyLookupChoiceFilter,
    PropertyMultipleChoiceFilter,
    PropertyTypedChoiceFilter,
    PropertyTypedMultipleChoiceFilter,
]
