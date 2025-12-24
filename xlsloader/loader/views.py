import pandas as pd

from django.contrib import messages
from django.db.models import Prefetch
from django.urls import reverse_lazy
from django.views.generic import FormView, ListView

from .models import Group, MainCategory, SecondCategory
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

    @staticmethod
    def _update_or_create(model, row, prefix: str, extra_defaults=None):
        if extra_defaults is None:
            extra_defaults = {}

        data = {
            'articul': row.get(f'{prefix}articul'),
            'title': row.get(f'{prefix}title'),
            'description': row.get(f'{prefix}description', '') or '',
            **extra_defaults,
        }
        obj, created = model.objects.update_or_create(
            articul=data['articul'],
            defaults=data,
        )
        return obj, created
    
    def form_valid(self, form):
        # Group.objects.all().delete()
        # MainCategory.objects.all().delete()
        # SecondCategory.objects.all().delete()
        excel_file = form.cleaned_data['excel_file']
        df = pd.read_excel(excel_file)
        created_groups = created_maincats = created_secondcats = 0
        for _, row in df.iterrows():
            group, created = self._update_or_create(
                model=Group,
                prefix='group_',
                row=row
            )
            if created:
                created_groups += 1

            # загрузка maincategory
            if (not row.get('maincategory_articul')) or \
                    (not row.get('maincategory_title')):
                continue
            maincategory, created = self._update_or_create(
                model=MainCategory,
                row=row,
                prefix='maincategory_',
                extra_defaults={'group': group}
            )
            if created:
                created_maincats += 1

            # загрузка secondcategory
            if (not row.get('secondcategory_articul')) or \
                    (not row.get('secondcategory_title')):
                continue
            secondcategory, created = self._update_or_create(
                model=SecondCategory,
                row=row,
                prefix='secondcategory_',
                extra_defaults={'maincategory': maincategory}
            )
            if created:
                created_secondcats += 1
        messages.success(
            self.request, f'Загружено новых групп: {created_groups}, '
                          f'основных категорий: {created_maincats}, '
                          f'категорий 2-го уровня: {created_secondcats}, '
        )
        return super().form_valid(form)
