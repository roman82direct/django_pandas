import pandas as pd

from django.contrib import messages
from django.db.models import Prefetch
from django.urls import reverse_lazy
from django.views.generic import FormView, ListView

from .models import Group, MainCategory
from .forms import ExcelImportForm


class IndexView(ListView):
    template_name = 'loader/index.html'

    def get_queryset(self):
        return Group.objects.prefetch_related(
            Prefetch('maincategories',
                     queryset=MainCategory.objects
                     .prefetch_related('secondcategories')
                     .order_by('articul'),
                     to_attr='main_cats')
        ).order_by('articul')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['groups'] = self.get_queryset()
        return context


class ExcelImportView(FormView):
    form_class = ExcelImportForm
    template_name = 'loader/load_form.html'
    success_url = reverse_lazy('loader:import_excel')

    def form_valid(self, form):
        Group.objects.all().delete()
        excel_file = form.cleaned_data['excel_file']
        df = pd.read_excel(excel_file)
        imported_count = 0
        for _, row in df.iterrows():
            group_data = {
                'articul': row.get('group_articul'),
                'title': row.get('group_title'),
                'description': row.get('group_description', ''),
            }
            group, created = Group.objects.update_or_create(
                articul=group_data['articul'],
                defaults=group_data
            )
            if created:
                imported_count += 1
        messages.success(
            self.request, f'Загружено новых групп: {imported_count}. '
        )
        return super().form_valid(form)
