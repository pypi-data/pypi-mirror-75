# -*- coding: utf-8 -*-
'''
diacamma.pro models package

@author: Laurent GAY
@organization: sd-libre.fr
@contact: info@sd-libre.fr
@copyright: 2019 sd-libre.fr
@license: This file is part of Lucterios.

Lucterios is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

Lucterios is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with Lucterios.  If not, see <http://www.gnu.org/licenses/>.
'''

from __future__ import unicode_literals
from datetime import date, timedelta

from django.db import models
from django.db.models import Q
from django.utils.translation import ugettext_lazy as _
from django.core.validators import MaxValueValidator, MinValueValidator

from lucterios.framework.models import LucteriosModel
from lucterios.framework.model_fields import LucteriosDecimalField, get_value_if_choices, LucteriosVirtualField
from lucterios.framework.tools import same_day_months_after
from lucterios.framework.signal_and_lock import Signal
from lucterios.CORE.models import Parameter, LucteriosGroup
from lucterios.CORE.parameters import Params

from diacamma.accounting.tools import format_with_devise
from diacamma.accounting.models import EntryLineAccount


class SocialDeclaration(LucteriosModel):
    year = models.IntegerField(verbose_name=_('year'), null=False, unique_for_year=True)
    quarter = models.IntegerField(verbose_name=_('quarter'), choices=((1, _('1st quarter')), (2, _('2nd quarter')), (3, _('3rd quarter')), (4, _('4st quarter'))), default=1, null=False)
    amount_service = LucteriosDecimalField(verbose_name=_('amount service'), max_digits=10, decimal_places=3,
                                           default=0.0, validators=[MinValueValidator(0.0), MaxValueValidator(9999999.999)], format_string=lambda: format_with_devise(5))
    amount_sell = LucteriosDecimalField(verbose_name=_('amount sell'), max_digits=10, decimal_places=3,
                                        default=0.0, validators=[MinValueValidator(0.0), MaxValueValidator(9999999.999)], format_string=lambda: format_with_devise(5))
    amount_other = LucteriosDecimalField(verbose_name=_('amount other'), max_digits=10, decimal_places=3,
                                         default=0.0, validators=[MinValueValidator(0.0), MaxValueValidator(9999999.999)], format_string=lambda: format_with_devise(5))

    date_begin = LucteriosVirtualField(verbose_name=_('date begin'), compute_from='get_date_begin', format_string='D')
    date_end = LucteriosVirtualField(verbose_name=_('date end'), compute_from='get_date_end', format_string='D')

    def __str__(self):
        quarter = get_value_if_choices(self.quarter, self.get_field_by_name('quarter'))
        return _("%(quarter)s of %(year)d") % {'quarter': quarter, 'year': self.year}

    def get_date_begin(self):
        return date(int(self.year), (self.quarter - 1) * 3 + 1, 1)

    def get_date_end(self):
        return same_day_months_after(self.date_begin, months=3) - timedelta(days=1)

    @classmethod
    def get_default_fields(cls):
        fields = ["year", "quarter", "amount_service", "amount_sell", "amount_other"]
        return fields

    @classmethod
    def get_show_fields(cls):
        fields = [("year", "quarter"), ("date_begin", "date_end"), "amount_service", "amount_sell", "amount_other"]
        return fields

    def calcul(self):
        periode = Q(entry__date_value__gte=self.date_begin) & Q(entry__date_value__lte=self.date_end)
        amount_sell = 0
        for line in EntryLineAccount.objects.filter(periode & Q(account__code__in=Params.getvalue("microbusiness-sellaccount").split(';'))):
            amount_sell += float(line.amount)
        amount_service = 0
        for line in EntryLineAccount.objects.filter(periode & Q(account__code__in=Params.getvalue("microbusiness-serviceaccount").split(';'))):
            amount_service += float(line.amount)
        amount_total = 0
        for line in EntryLineAccount.objects.filter(periode & Q(account__type_of_account=3)):
            amount_total += float(line.amount)
        self.amount_service = max(0, round(amount_service, 0))
        self.amount_sell = max(0, round(amount_sell, 0))
        self.amount_other = max(0, round(amount_total - amount_service - amount_sell, 0))
        self.save()

    class Meta(object):
        verbose_name = _('social declaration')
        verbose_name_plural = _('social declarations')
        ordering = ['year', 'quarter']
        default_permissions = ['change']


@Signal.decorate('checkparam')
def microbusiness_checkparam():
    Parameter.check_and_create(name="microbusiness-sellaccount", typeparam=0, title=_("microbusiness-sellaccount"), args="{'Multi':True}", value='',
                               meta='("accounting","ChartsAccount","import diacamma.accounting.tools;django.db.models.Q(code__regex=diacamma.accounting.tools.current_system_account().get_revenue_mask()) & django.db.models.Q(year__is_actif=True)", "code", True)')
    Parameter.check_and_create(name="microbusiness-serviceaccount", typeparam=0, title=_("microbusiness-serviceaccount"), args="{'Multi':True}", value='',
                               meta='("accounting","ChartsAccount","import diacamma.accounting.tools;django.db.models.Q(code__regex=diacamma.accounting.tools.current_system_account().get_revenue_mask()) & django.db.models.Q(year__is_actif=True)", "code", True)')

    LucteriosGroup.redefine_generic(_("# micro-business (editor)"), SocialDeclaration.get_permission(True, True, True))
