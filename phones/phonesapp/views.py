import pandas
from django.http import HttpResponse
import datetime
import xlwt
from .models import Numbers, Attachments, Files, Providers, Parser, SubscriptionFee
from django.core.paginator import Paginator
from .filters.filters import NumbersFilter, ReportFilter
from django.shortcuts import render, redirect
from .forms import NumbersForm, AddFiles
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required, permission_required
import pandas as pd


class LoginUser(LoginView):

    form_class = AuthenticationForm
    template_name = 'login/login.html'


def logout_user(request):

    logout(request)
    return redirect('/login')


@login_required(login_url='login/')
@permission_required('phonesapp.view_numbers')
def home(request):

    number = Numbers.objects.exclude(is_enabled=False)
    attachment = Attachments.objects.all()
    my_filter = NumbersFilter(request.GET, queryset=number)
    number = my_filter.qs

    m = []
    k = 0
    for i in number:
        k += 1
        m.append(k)

    numbers_sum = len(m)
    numbers_cf = len(Numbers.objects.exclude(cf=False))
    numbers_hide = len(Numbers.objects.exclude(is_enabled=True))

    paginator = Paginator(number, 15)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    paginator_obj = Paginator(m, 15).get_page(page_number)

    context = {
               'number': number,
               'page_obj': page_obj,
               'paginator_obj': paginator_obj,
               'numbers_sum': numbers_sum,
               'numbers_cf': numbers_cf,
               'numbers_hide': numbers_hide,
               'attachment': attachment,
               }

    return render(request, 'home/home.html', context)


@login_required(login_url='login/')
@permission_required('phonesapp.change_numbers')
def edit_number(request, pk):

    numbers = Numbers.objects.get(id=pk)
    form = NumbersForm(instance=numbers)

    if request.method == 'POST':
        form = NumbersForm(request.POST, instance=numbers)
        if form.is_valid():
            form.save()
            return redirect('/')

    context = {'form': form}
    return render(request, 'edit/edit.html', context)


@login_required(login_url='login/')
@permission_required('phonesapp.add_parser')
def parser_rostelecom(request):

    files = Files.objects.all()
    providers = Providers.objects.get(id=1)

    if request.method == 'POST':
        form = AddFiles(request.POST, request.FILES)
        if form.is_valid():

            i = Files(**form.cleaned_data)
            i.save()

            last_file = (Files.objects.order_by('id').last()).id
            excel_file = Files.objects.get(pk=last_file)
            excel_file_str = str(excel_file)

            file = pandas.read_excel('media/' + excel_file_str)
            number_summ = file[['Телефон А', 'Сумма']]
            result = number_summ.groupby('Телефон А').sum()

            temp = []
            sub_fee = float(str(SubscriptionFee.objects.get(pk=1)))

            base_cf = str(Numbers.objects.filter(cf=True))
            base_no_cf = str(Numbers.objects.filter(cf=False))

            for index, row in result.iterrows():
                str_index = str(index).lstrip("'3822")

                if str_index in base_cf:
                    str_index_number = Numbers.objects.get(number=str_index)
                    str_index_attach = str_index_number.attachment
                    Parser(number=str_index,
                           attachment=str_index_attach,
                           provider=providers,
                           file=Files.objects.order_by('id').last(),
                           payment=row['Сумма'],
                           result_pay=row['Сумма']).save()
                elif str_index in base_no_cf:
                    str_index_number = Numbers.objects.get(number=str_index)
                    str_index_attach = str_index_number.attachment
                    Parser(number=str_index,
                           attachment=str_index_attach,
                           provider=providers,
                           file=Files.objects.order_by('id').last(),
                           payment=row['Сумма'],
                           result_pay=row['Сумма'] + sub_fee).save()
                elif str_index not in str(Numbers.objects.all()):
                    temp.append(str_index)
                    Parser(number=str_index,
                           attachment=None,
                           provider=providers,
                           file=Files.objects.order_by('id').last(),
                           payment=row['Сумма'],
                           result_pay=row['Сумма']).save()

            return render(request, 'files/rostelecom.html', {'alert_flag': True, 'temp': temp})

    else:
        form = AddFiles()

    context = {'form': form, 'providers': providers, 'files': files}

    return render(request, 'files/rostelecom.html', context)


@login_required(login_url='login/')
@permission_required('phonesapp.add_parser')
def parser_avantel(request):

    files = Files.objects.all()
    providers = Providers.objects.get(id=2)

    if request.method == 'POST':
        form = AddFiles(request.POST, request.FILES)
        if form.is_valid():

            i = Files(**form.cleaned_data)
            i.save()

            last_file = (Files.objects.order_by('id').last()).id
            excel_file = Files.objects.get(pk=last_file)
            excel_file_str = str(excel_file)

            file = pandas.read_excel('media/' + excel_file_str, skiprows=1)
            number_summ = file[['Номер звонящего', 'Стоимость']]
            result = number_summ.groupby('Номер звонящего').sum()

            temp = []
            sub_fee = float(str(SubscriptionFee.objects.get(pk=1)))

            base_cf = str(Numbers.objects.filter(cf=True))
            base_no_cf = str(Numbers.objects.filter(cf=False))

            for index, row in result.iterrows():
                str_index = str(index).lstrip("'3822")

                if str_index in base_cf:
                    str_index_number = Numbers.objects.get(number=str_index)
                    str_index_attachment = str_index_number.attachment
                    Parser(number=str_index,
                           attachment=str_index_attachment,
                           provider=providers,
                           file=Files.objects.order_by('id').last(),
                           payment=row['Стоимость'],
                           result_pay=row['Стоимость'] + sub_fee).save()
                elif str_index in base_no_cf:
                    str_index_number = Numbers.objects.get(number=str_index)
                    str_index_attachment = str_index_number.attachment
                    Parser(number=str_index,
                           attachment=str_index_attachment,
                           provider=providers,
                           file=Files.objects.order_by('id').last(),
                           payment=row['Стоимость'],
                           result_pay=row['Стоимость']).save()
                if str_index not in str(Numbers.objects.all()):
                    temp.append(str_index)
                    Parser(number=str_index,
                           attachment=None,
                           provider=providers,
                           file=Files.objects.order_by('id').last(),
                           payment=row['Стоимость'],
                           result_pay=row['Стоимость']).save()

            return render(request, 'files/avantel.html', {'alert_flag': True, 'temp': temp})

    else:
        form = AddFiles()

        context = {'form': form, 'providers': providers, 'files': files}

        return render(request, 'files/avantel.html', context)


@login_required(login_url='login/')
def report(request):

    numbers_pars = Parser.objects.all()
    attachments = Attachments.objects.all()
    myFilter = ReportFilter(request.GET, queryset=numbers_pars)
    numbers_pars = myFilter.qs
    context = {'numbers_pars': numbers_pars, 'ReportFilter': myFilter, 'attachments': attachments}

    return render(request, 'report/report.html', context)


def export_excel(request):

    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = ("attachment; filename=Numbers_" + str(datetime.datetime.now().strftime("%d/%m/%y")) + '.xls')
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Numbers', cell_overwrite_ok=True)
    row_num = 0
    font_style = xlwt.XFStyle()
    font_style.font.bold = True
    columns = ['Отдел',
               'Номер',
               'К оплате']

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)

    font_style = xlwt.XFStyle()
    rows = ReportFilter(request.GET,
                        queryset=Parser.objects.all().values_list(
                            'attachment__attachment',
                            'number',
                            'result_pay')).qs

    res = pd.DataFrame(ReportFilter(request.GET, queryset=Parser.objects.annotate().values_list('result_pay')).qs)
    res_sum = res.sum()
    itog = float(res_sum.to_numpy())

    for row in rows:
        row_num += 1

        for col_num in range(len(row)):

            if isinstance(row[col_num], datetime.datetime):
                date_time = row[col_num].astimezone(datetime.timezone(datetime.timedelta(hours=7))).strftime('%d/%m/%Y %H:%M')
                ws.write(row_num, col_num, date_time, font_style)
                ws.write_merge(1, row_num, 0, 0, f'{str(row[0])}')

            else:
                ws.write(row_num, col_num, row[col_num], font_style)
                ws.write_merge(1, row_num, 0, 0, f'{str(row[0])}')
                ws.write(row_num+1, 1, 'Итог:')
                ws.write(row_num + 1, 2, itog)
    wb.save(response)

    return response