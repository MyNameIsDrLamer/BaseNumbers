import django_filters
from django_filters import FilterSet, DateFilter
from phonesapp.models import Numbers, Parser


class NumbersFilter(FilterSet):
    class Meta:
        model = Numbers
        fields = ('id', 'number', 'attachment', 'cf')


class ReportFilter(django_filters.FilterSet):
    start_date = DateFilter(field_name='date_upload', lookup_expr="gte")
    end_date = DateFilter(field_name='date_upload', lookup_expr="lte")

    class Meta:
        model = Parser
        fields = ('attachment', 'number')