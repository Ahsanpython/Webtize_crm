from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.db.models import Sum
from datetime import date
from .models import Expense
from .forms import ExpenseForm


class ExpenseListView(ListView):
    model = Expense
    template_name = "expenses/list.html"
    context_object_name = "expenses"
    paginate_by = 20

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        # month filter ?month=YYYY-MM
        m = self.request.GET.get('month')
        qs = self.get_queryset()
        if m:
            y, mm = m.split('-')
            qs = qs.filter(date__year=int(y), date__month=int(mm))
        ctx['total_month'] = qs.aggregate(s=Sum('amount'))['s'] or 0
        ctx['selected_month'] = m
        return ctx

class ExpenseCreateView(CreateView):
    model = Expense
    form_class = ExpenseForm
    template_name = "expenses/form.html"
    success_url = reverse_lazy('expense_list')

class ExpenseUpdateView(UpdateView):
    model = Expense
    form_class = ExpenseForm
    template_name = "expenses/form.html"
    success_url = reverse_lazy('expense_list')



class ExpenseDeleteView(DeleteView):
    model = Expense
    template_name = "expenses/confirm_delete.html"
    success_url = reverse_lazy('expense_list')
