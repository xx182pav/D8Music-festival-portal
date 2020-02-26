from django.shortcuts import redirect
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView, FormView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.contrib.auth.models import User
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy

from collections import OrderedDict

from users.models import UserProfile
from festival import models, forms


class Index(TemplateView):
    template_name = 'index.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context["username"] = self.request.user.username
            if self.request.user.groups.filter(name='Кураторы').exists():
                context["userrole"] = "куратор"
            else:
                context["userrole"] = "музыкант"
        slots = models.SceneSlot.objects.all().order_by('timeslot__day', 'timeslot__time', 'scene')
        schedule = OrderedDict()
        for slot in slots:
            day = slot.timeslot.get_day_display()
            time = slot.timeslot.get_time_display()
            scene = slot.scene.name
            items_list = slot.request_set.all()
            if not schedule.get(day, False):
                schedule[day] = OrderedDict()
            if not schedule[day].get(time, False):
                schedule[day][time] = OrderedDict()
            if not schedule[day][time].get(scene, False):
                schedule[day][time][scene] = OrderedDict()
            schedule[day][time][scene] = slot.request_set.all()
        context['schedule'] = schedule
        
        return context


class ManageRequests(ListView):
    template_name = 'manage-requests.html'
    model = models.Request

    def dispatch(self, request, *args, **kwargs):  
        if self.request.user.is_anonymous:  
            return HttpResponseRedirect(reverse_lazy('users:login'))  
        if not self.request.user.has_perm('festival.change_request'):
            return HttpResponseRedirect(reverse_lazy('festival:request'))
        return super(ManageRequests, self).dispatch(request, *args, **kwargs)  

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['username'] = self.request.user.username
        if self.request.user.groups.filter(name='Кураторы').exists():
            context["userrole"] = "куратор"
        else:
            context["userrole"] = "музыкант"
        requests_db_entries = models.Request.objects.all()
        requests = []
        for r in requests_db_entries:
            censor_voices = []
            for v in r.voice_set.all():
                censor_voices.append(v.censor.user.first_name + " " + v.censor.user.last_name + " (" + v.censor.user.username + ") - " + v.get_voice_display())
            scene = ""
            timeslot = ""
            if r.scene_slot:
                scene = r.scene_slot.scene
                timeslot = r.scene_slot.timeslot
            censors_count = User.objects.filter(groups__name='Кураторы').count()
            all_voices = r.voice_set.count()
            approve_voices = r.voice_set.filter(voice='YES').count()
            reject_voices = r.voice_set.filter(voice='NO').count()
            if (approve_voices - reject_voices > 2) or (all_voices == censors_count and approve_voices > reject_voices):
                allow_approve_button = True
            else:
                allow_approve_button = False
            if (reject_voices > 4) or (all_voices == censors_count and approve_voices <= reject_voices):
                allow_reject_button = True
            else:
                allow_reject_button = False
            requests.append({
                'status': r.status,
                'name': r.name,
                'format': r.get_format_display(),
                'scene': scene, 
                'timeslot': timeslot, 
                'owner': r.owner.user.first_name + " " + r.owner.user.last_name + " (" + r.owner.user.username + ")",
                'desired_scene': r.desired_scene,
                'desired_timeslot': r.desired_timeslot,
                'censor_voices': censor_voices,
                'id': r.id,
                'allow_reject_button': allow_reject_button,
                'allow_approve_button': allow_approve_button,
            })
        context['requests'] = requests
        scene_slots = models.SceneSlot.objects.all()
        avalable_time_slots = []
        for ss in scene_slots:
            if ss.count - models.Request.objects.filter(scene_slot=ss).count():
                avalable_time_slots.append({
                    'id': ss.id,
                    'scene': ss.scene.name, 
                    'timeslot': ss.timeslot.get_day_display() + ' - ' + ss.timeslot.get_time_display(), 
                    'count': ss.count - models.Request.objects.filter(scene_slot=ss).count()
                })
        context['avalable_time_slots'] = avalable_time_slots
        return context


class RequestView(CreateView):
    model = models.Request
    template_name = 'request.html'
    success_url = '/'
    fields = ['name', 'text', 'format', 'desired_scene', 'desired_timeslot', 'comment']

    def dispatch(self, request, *args, **kwargs):  
        if self.request.user.is_anonymous:  
            return HttpResponseRedirect(reverse_lazy('users:login'))  
        r = models.Request.objects.filter(owner=UserProfile.objects.filter(user=self.request.user).first()).first()
        if r:
            return HttpResponseRedirect(reverse_lazy('festival:request_status', args=[r.id]))
        return super(RequestView, self).dispatch(request, *args, **kwargs)  

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context["username"] = self.request.user.username
            if self.request.user.groups.filter(name='Кураторы').exists():
                context["userrole"] = "куратор"
            else:
                context["userrole"] = "музыкант"
        return context

    def form_valid(self, form):  
        instance = form.save(commit=False)  
        instance.owner = UserProfile.objects.get(user=self.request.user)  
        instance.save()  
        return super(RequestView, self).form_valid(form)


class RequestStatus(PermissionRequiredMixin, DetailView):
    model = models.Request
    template_name = 'request-status.html'

    def has_permission(self):
        r = models.Request.objects.values('id').filter(owner=UserProfile.objects.get(user=self.request.user)).first()
        if r['id'] == self.kwargs['pk']:
            return True
        return False

    def dispatch(self, request, *args, **kwargs):  
        if self.request.user.is_anonymous:  
            return HttpResponseRedirect(reverse_lazy('users:login'))  
        return super(RequestStatus, self).dispatch(request, *args, **kwargs)  

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context["username"] = self.request.user.username
            if self.request.user.groups.filter(name='Кураторы').exists():
                context["userrole"] = "куратор"
            else:
                context["userrole"] = "музыкант"
        return context


class VoteView(PermissionRequiredMixin, FormView):
    permission_required = 'festival.change_request'
    template_name = 'voice-form.html'
    # form_class = forms.VoteForm
    success_url = '/requests'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context['username'] = self.request.user.username
            context['request'] = models.Request.objects.get(pk=self.kwargs['request_id'])
            if self.request.user.groups.filter(name='Кураторы').exists():
                context["userrole"] = "куратор"
            else:
                context["userrole"] = "музыкант"
        return context
    
    def get_form(self, form_class=forms.VoteForm):
        
        try:
            voice = models.Voice.objects.get(censor__user=self.request.user, request__pk=self.kwargs['request_id'])
            return form_class(instance=voice, **self.get_form_kwargs())
        except models.Voice.DoesNotExist:
            return form_class(**self.get_form_kwargs())
    
    def form_valid(self, form):
        form.instance.censor = UserProfile.objects.get(user=self.request.user)
        form.instance.request = models.Request.objects.get(pk=self.kwargs['request_id'])
        form.instance.voice = form.cleaned_data.get("voice")
        form.save()
        return super(VoteView, self).form_valid(form)


def change_status(request):
    if request.method == 'POST':
        request_id = request.POST['id']
        status = request.POST['status']
        scene_slot_id = request.POST.get('timeslot', False)
        if not (request.user.has_perm('festival.change_request') and request_id and status):
            return redirect('/requests')
        else:
            r = models.Request.objects.get(id=request_id)
            if not r:
                return redirect('/requests')
            else:
                censors_count = User.objects.filter(groups__name='Кураторы').count()
                all_voices = r.voice_set.count()
                approve_voices = r.voice_set.filter(voice='YES').count()
                reject_voices = r.voice_set.filter(voice='NO').count()
                if (approve_voices - reject_voices > 2) or (all_voices == censors_count and approve_voices > reject_voices):
                    if scene_slot_id:
                        r.scene_slot = models.SceneSlot.objects.get(id=scene_slot_id)
                        r.status = status
                        r.save()
                if (reject_voices > 4) or (all_voices == censors_count and approve_voices <= reject_voices):
                    r.scene_slot = None
                    r.status = status
                    r.save()
    return redirect('/requests')